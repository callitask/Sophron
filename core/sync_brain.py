import os
import sys
import subprocess
import time
from pathlib import Path

def log(msg):
    print(f"[Sync Brain] {msg}", flush=True)

def run_cmd(cmd_list, cwd):
    result = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Command failed: {' '.join(cmd_list)}\nError: {result.stderr}")
    return result.returncode == 0, result.stdout

def sync():
    base_dir = Path(r"f:\JOB AI AGENT\Sophron")
    
    # 1. Run the Active Learning Loop
    log("Running Master Agent Learning Loop...")
    learn_script = base_dir / "core" / "run_master_agent.py"
    subprocess.run([sys.executable, str(learn_script), "learn"], cwd=base_dir)
    
    # 2. Check Git Status
    log("Checking Git status...")
    _, status_out = run_cmd(["git", "status", "--porcelain"], cwd=base_dir)
    
    if not status_out.strip():
        log("No new cognitive updates to push. Brain is up to date.")
        return
        
    # 3. Add, Commit, Push
    log("New cognitive data detected. Syncing to secure cloud...")
    run_cmd(["git", "add", "."], cwd=base_dir)
    commit_msg = f"Cognitive Sync: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    run_cmd(["git", "commit", "-m", commit_msg], cwd=base_dir)
    
    success, push_out = run_cmd(["git", "push", "origin", "main"], cwd=base_dir)
    if success:
        log("Successfully pushed cognitive OS to private remote.")
    else:
        log("Push failed. You may need to run 'git push -u origin main' manually once to authenticate.")

if __name__ == "__main__":
    sync()
