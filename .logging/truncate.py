#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
from pathlib import Path
import json

base = Path(".")
logdir = base / ".logging"
logdir.mkdir(parents=True, exist_ok=True)

# truncate (create if missing)
(logdir / "log.jsonl").write_text("", encoding="utf-8")

# reset watcher state so next record starts a new session folder
state = {"processed_count": 0, "last_size": 0, "current_sid": None, "session_folder": None}
(logdir / ".state.json").write_text(json.dumps(state), encoding="utf-8")

print("New session: truncated .logging/log.jsonl and reset watcher state.")
