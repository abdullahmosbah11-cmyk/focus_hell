#!/usr/bin/env python3

import json
import signal
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from shared import config

running = True

def handle_stop(signum, frame):
    global running
    print(f"[focusd] Received signal {signum}, shutting down...", flush=True)
    running = False

def ensure_directories():
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.RUN_DIR.mkdir(parents=True, exist_ok=True)

def save_state(state):
    with open(config.STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(state, file, indent=2)

def load_state():
    if not config.STATE_FILE.exists():
        return None
    try:
        with open(config.STATE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None

def clear_state():
    if config.STATE_FILE.exists():
        config.STATE_FILE.unlink()

def start_test_session(duration_seconds=300):
    state = {
        "active": True,
        "mode": config.MODE_INFERNO,
        "end_time": time.time() + duration_seconds,
    }    
    save_state(state)
    print(f"[focusd] Test session started ({duration_seconds}s).", flush=True)

def run_daemon():
    signal.signal(signal.SIGTERM, handle_stop)
    signal.signal(signal.SIGINT, handle_stop)
    ensure_directories()

    print("[focusd] Daemon started.", flush=True)

    while running:
        state = load_state()

        if state and state.get("active"):
            remaining = int(state["end_time"] - time.time())

            if remaining <= 0:
                print("[focusd] Session complete! Clearing lock.", flush=True)
                clear_state()

            else:
                mode = state.get("mode", config.MODE_EMBER)
                print(f"[focusd] Active ({mode}) | {remaining}s left", flush=True)

        time.sleep(config.TICK_INTERVAL_SECONDS)

    print("[focusd] Daemon stopped cleanly.", flush=True)

if __name__ == "__main__":
    if "--test" in sys.argv:
        ensure_directories()
        start_test_session()
    run_daemon()