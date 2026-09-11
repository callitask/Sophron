"""
sophron_write_guard.py
======================
Concurrency-safe write layer for Sophron cognitive memory.

Solves:
  1. JSON file race conditions across concurrent AG sessions
  2. Git non-fast-forward failures when multiple sessions push simultaneously
  3. Duplicate insight card noise (dedup by content fingerprint)
  4. Multi-session detection and intelligent multitasking card generation

Usage (from any script or AG-run python block):
    from sophron_write_guard import SophronWriteGuard
    guard = SophronWriteGuard(session_uuid="e49e3776-...")
    guard.safe_write_json(path, data)
    guard.safe_git_push(commit_message)
    guard.register_session(workspace="career_agent", task_summary="Tailoring resume for Anshika")
    guard.deregister_session()
    is_multi = guard.detect_multitasking()
    guard.write_multitasking_card(sessions)
"""

import json
import os
import time
import hashlib
import socket
import subprocess
from pathlib import Path
from datetime import datetime, timezone

SOPHRON_ROOT = Path(r"F:\JOB AI AGENT\Sophron")
LOCK_FILE = SOPHRON_ROOT / ".sophron_write.lock"
SESSION_REGISTRY = SOPHRON_ROOT / "session_registry.json"
MULTITASKING_CARDS_DIR = SOPHRON_ROOT / "understanding_master" / "multitasking_cards"

LOCK_TIMEOUT_SECONDS = 45      # How long to wait for another session to release lock
LOCK_STALE_SECONDS = 90        # If lock is older than this, treat as stale and steal it
LOCK_RETRY_INTERVAL = 1.5      # Seconds between retry attempts
GIT_PUSH_MAX_RETRIES = 3       # Max attempts for git push


class LockTimeoutError(Exception):
    pass


class SophronWriteGuard:
    """
    Concurrency-safe write manager for Sophron.
    One instance per AG session. Holds the session UUID for all operations.
    """

    def __init__(self, session_uuid: str, workspace: str = "unknown", task_summary: str = ""):
        self.session_uuid = session_uuid
        self.workspace = workspace
        self.task_summary = task_summary
        self.sophron_root = SOPHRON_ROOT
        MULTITASKING_CARDS_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # FILE LOCKING
    # ------------------------------------------------------------------

    def _acquire_lock(self, timeout: float = LOCK_TIMEOUT_SECONDS) -> bool:
        """
        Acquire the Sophron-wide write lock.
        Polls until the lock is free or timeout expires.
        Steals the lock if it is stale (held for >LOCK_STALE_SECONDS).
        Returns True if acquired, raises LockTimeoutError otherwise.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            if not LOCK_FILE.exists():
                # Lock is free — take it
                self._write_lock()
                return True

            # Lock exists — read it
            try:
                lock_data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
                holder = lock_data.get("session_uuid", "unknown")
                acquired_at = lock_data.get("acquired_at_epoch", 0)
                age = time.time() - acquired_at

                # Already ours
                if holder == self.session_uuid:
                    return True

                # Stale lock — steal it
                if age > LOCK_STALE_SECONDS:
                    print(f"[WriteGuard] Stale lock from session {holder[:8]}... ({age:.0f}s old). Stealing.")
                    self._write_lock()
                    return True

                # Someone else holds it — wait
                print(f"[WriteGuard] Lock held by {holder[:8]}... ({age:.1f}s). Waiting...")
            except (json.JSONDecodeError, OSError):
                # Corrupted/empty lock file — steal it
                self._write_lock()
                return True

            time.sleep(LOCK_RETRY_INTERVAL)

        raise LockTimeoutError(
            f"[WriteGuard] Could not acquire Sophron write lock within {timeout}s. "
            f"Holder: {self._read_lock_holder()}. Your session: {self.session_uuid[:8]}..."
        )

    def _write_lock(self):
        lock_data = {
            "session_uuid": self.session_uuid,
            "acquired_at_epoch": time.time(),
            "acquired_at_iso": datetime.now().isoformat(),
            "hostname": socket.gethostname(),
            "workspace": self.workspace,
            "task_summary": self.task_summary[:80]
        }
        LOCK_FILE.write_text(json.dumps(lock_data, indent=2), encoding="utf-8")

    def _release_lock(self):
        try:
            if LOCK_FILE.exists():
                lock_data = json.loads(LOCK_FILE.read_text(encoding="utf-8"))
                if lock_data.get("session_uuid") == self.session_uuid:
                    LOCK_FILE.unlink()
        except (OSError, json.JSONDecodeError):
            pass

    def _read_lock_holder(self) -> str:
        try:
            return json.loads(LOCK_FILE.read_text(encoding="utf-8")).get("session_uuid", "?")
        except Exception:
            return "?"

    # ------------------------------------------------------------------
    # SAFE JSON WRITE
    # ------------------------------------------------------------------

    def safe_write_json(self, path: Path, data: dict, indent: int = 2) -> bool:
        """
        Write JSON to path with:
          - Write lock acquisition
          - Atomic write via temp file (no partial writes on crash)
          - Lock release on success or failure
        """
        path = Path(path)
        acquired = False
        try:
            self._acquire_lock()
            acquired = True
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")
            tmp.replace(path)  # Atomic on same filesystem
            return True
        except LockTimeoutError as e:
            print(str(e))
            return False
        finally:
            if acquired:
                self._release_lock()

    def safe_append_line(self, path: Path, line: str) -> bool:
        """
        Append a single line to a text file (e.g. macro roll-up) with locking.
        """
        path = Path(path)
        acquired = False
        try:
            self._acquire_lock()
            acquired = True
            with open(path, "a", encoding="utf-8") as f:
                f.write(line if line.endswith("\n") else line + "\n")
            return True
        except LockTimeoutError as e:
            print(str(e))
            return False
        finally:
            if acquired:
                self._release_lock()

    # ------------------------------------------------------------------
    # DEDUPLICATION
    # ------------------------------------------------------------------

    def insight_fingerprint(self, insight_id: str, user_action: str) -> str:
        """
        Generate a short hash from insight_id + user_action summary.
        Used to detect duplicate insight cards across sessions.
        """
        raw = f"{insight_id}|{user_action[:120]}"
        return hashlib.sha256(raw.encode()).hexdigest()[:12]

    def is_duplicate_insight(self, insight_id: str, user_action: str) -> bool:
        """
        Return True if an insight card with the same fingerprint already exists.
        Checks the learned_insights directory.
        """
        fp = self.insight_fingerprint(insight_id, user_action)
        insights_dir = self.sophron_root / "understanding_master" / "learned_insights"
        for f in insights_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                if data.get("_dedup_fingerprint") == fp:
                    return True
            except Exception:
                continue
        return False

    # ------------------------------------------------------------------
    # SESSION REGISTRY
    # ------------------------------------------------------------------

    def register_session(self):
        """
        Register this session as active in session_registry.json.
        Call at session start.
        """
        acquired = False
        try:
            self._acquire_lock()
            acquired = True
            registry = self._load_registry()
            registry["active_sessions"][self.session_uuid] = {
                "session_uuid": self.session_uuid,
                "workspace": self.workspace,
                "task_summary": self.task_summary,
                "registered_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat()
            }
            self._save_registry(registry)
        finally:
            if acquired:
                self._release_lock()

    def deregister_session(self):
        """
        Remove this session from session_registry.json.
        Call at session end.
        """
        acquired = False
        try:
            self._acquire_lock()
            acquired = True
            registry = self._load_registry()
            registry["active_sessions"].pop(self.session_uuid, None)
            # Archive to past_sessions
            registry.setdefault("past_sessions", []).append({
                "session_uuid": self.session_uuid,
                "workspace": self.workspace,
                "ended_at": datetime.now().isoformat()
            })
            # Keep only last 30 past sessions
            registry["past_sessions"] = registry["past_sessions"][-30:]
            self._save_registry(registry)
        finally:
            if acquired:
                self._release_lock()

    def heartbeat(self):
        """Update last_heartbeat timestamp. Call periodically during a long session."""
        acquired = False
        try:
            self._acquire_lock(timeout=10)
            acquired = True
            registry = self._load_registry()
            if self.session_uuid in registry["active_sessions"]:
                registry["active_sessions"][self.session_uuid]["last_heartbeat"] = datetime.now().isoformat()
            self._save_registry(registry)
        except LockTimeoutError:
            pass
        finally:
            if acquired:
                self._release_lock()

    def _load_registry(self) -> dict:
        if SESSION_REGISTRY.exists():
            try:
                return json.loads(SESSION_REGISTRY.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"active_sessions": {}, "past_sessions": []}

    def _save_registry(self, registry: dict):
        SESSION_REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")

    # ------------------------------------------------------------------
    # MULTI-SESSION DETECTION
    # ------------------------------------------------------------------

    def detect_multitasking(self) -> list:
        """
        Returns list of OTHER active sessions (excluding self).
        A session is considered stale if last_heartbeat > 10 minutes ago.
        Returns [] if solo session.
        """
        registry = self._load_registry()
        active = registry.get("active_sessions", {})
        now = datetime.now()
        live_others = []

        for uuid, info in active.items():
            if uuid == self.session_uuid:
                continue
            try:
                hb = datetime.fromisoformat(info.get("last_heartbeat", "2000-01-01"))
                age_minutes = (now - hb).total_seconds() / 60
                if age_minutes < 10:  # Live if heartbeat within 10 min
                    live_others.append(info)
            except Exception:
                continue

        return live_others

    # ------------------------------------------------------------------
    # MULTITASKING CARD
    # ------------------------------------------------------------------

    def write_multitasking_card(self, other_sessions: list) -> Path:
        """
        Write a structured multitasking insight card when multiple sessions
        are detected. This captures the cognitive pattern of context-switching.
        """
        ts = datetime.now().isoformat()
        date_slug = datetime.now().strftime("%Y%m%d_%H%M%S")

        all_sessions = [{
            "session_uuid": self.session_uuid,
            "workspace": self.workspace,
            "task_summary": self.task_summary,
            "role": "this_session"
        }] + [{**s, "role": "peer_session"} for s in other_sessions]

        workspaces_involved = list({s.get("workspace", "unknown") for s in all_sessions})
        tasks = [s.get("task_summary", "")[:100] for s in all_sessions]

        card = {
            "card_type": "multitasking_session",
            "card_id": f"multitask_{date_slug}_{self.session_uuid[:8]}",
            "temporal_anchor": ts,
            "detected_by_session": self.session_uuid,
            "concurrent_session_count": len(all_sessions),
            "sessions": all_sessions,
            "workspaces_involved": workspaces_involved,
            "cognitive_assessment": {
                "pattern": "parallel_context_switching",
                "cognitive_load": "high" if len(all_sessions) >= 3 else "elevated",
                "risk_level": "low" if len(workspaces_involved) == 1 else "medium",
                "interpretation": (
                    f"User is running {len(all_sessions)} concurrent AG sessions across "
                    f"{len(workspaces_involved)} workspace(s). Tasks: {'; '.join(t for t in tasks if t)}. "
                    "This indicates high output-focus mode: user is orchestrating multiple AI streams "
                    "simultaneously, treating each session as a parallel execution unit."
                )
            },
            "sophron_implications": {
                "write_strategy": "lock_serialised",
                "dedup_active": True,
                "git_strategy": "pull_rebase_before_push",
                "card_isolation": "each_session_writes_to_own_namespace_first",
                "merge_trigger": "session_deregister"
            },
            "cross_session_potential_insights": (
                "If workspaces differ, user may be context-switching between unrelated domains — "
                "monitor for cognitive spillover (applying rules from workspace A to workspace B). "
                "If workspaces are the same, user is parallelising work on one project — "
                "AG should not duplicate effort or write conflicting insight cards."
            )
        }

        out_path = MULTITASKING_CARDS_DIR / f"multitask_{date_slug}_{self.session_uuid[:8]}.json"
        out_path.write_text(json.dumps(card, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[WriteGuard] Multitasking card written: {out_path.name}")
        return out_path

    # ------------------------------------------------------------------
    # SAFE GIT PUSH
    # ------------------------------------------------------------------

    def safe_git_push(self, commit_message: str, retries: int = GIT_PUSH_MAX_RETRIES) -> bool:
        """
        Performs a concurrency-safe git push:
          1. Disables GPG signing (Windows headless bypass)
          2. Stages all changes
          3. Commits (skips if nothing to commit)
          4. Pulls with --rebase to resolve any concurrent pushes
          5. Pushes
          6. On non-fast-forward failure, retries up to etries times
        Returns True on success.
        """
        repo = self.sophron_root
        session_tag = self.session_uuid[:8]

        def git(args, check=False):
            result = subprocess.run(
                ["git"] + args,
                cwd=str(repo),
                capture_output=True,
                text=True
            )
            return result

        # Step 1 — GPG bypass
        git(["config", "commit.gpgsign", "false"])

        # Step 2 — Stage all
        r = git(["add", "-A"])
        if r.returncode != 0:
            print(f"[WriteGuard] git add failed: {r.stderr}")
            return False

        # Step 3 — Commit (OK if nothing to commit)
        full_msg = f"[{session_tag}] {commit_message}"
        r = git(["commit", "-m", full_msg])
        if r.returncode != 0 and "nothing to commit" not in r.stdout + r.stderr:
            print(f"[WriteGuard] git commit failed: {r.stderr}")
            return False

        # Step 4–6 — Push with rebase-retry loop
        for attempt in range(1, retries + 1):
            # Pull --rebase first to absorb concurrent pushes
            r = git(["pull", "--rebase", "origin", "main"])
            if r.returncode != 0:
                print(f"[WriteGuard] git pull --rebase failed (attempt {attempt}): {r.stderr}")
                # Abort rebase if in progress
                git(["rebase", "--abort"])
                time.sleep(2)
                continue

            # Push
            r = git(["push", "origin", "main"])
            if r.returncode == 0:
                print(f"[WriteGuard] Git push succeeded (attempt {attempt}): {full_msg}")
                return True
            elif "non-fast-forward" in r.stderr or "fetch first" in r.stderr:
                print(f"[WriteGuard] Non-fast-forward detected (attempt {attempt}). Retrying pull+push...")
                time.sleep(2 * attempt)
                continue
            else:
                print(f"[WriteGuard] Git push failed: {r.stderr}")
                return False

        print(f"[WriteGuard] Git push failed after {retries} attempts.")
        return False
