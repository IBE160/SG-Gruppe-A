#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["ijson>=3.2.3","watchfiles>=0.21"]
# ///
"""
Gemini telemetry watcher using ijson (streaming, multi-value) + watchfiles.

- Input: .logging/log.jsonl  (actually pretty-printed JSON objects, back-to-back)
- Output per session:
    .logging/sessions/<YYYY-MM-DD_HH-mm-ss>/
        prompts.log
        responses.log
        tools.log

Session rollover triggers:
- File truncation/rotation (size shrank → next record opens new folder)
- Session id changes (attributes["session.id"] or similar)

This script NEVER launches Gemini. Start Gemini yourself.
"""

from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple

import ijson
from watchfiles import awatch, Change

BASE = Path(".")
LOG_FILE = BASE / ".logging" / "log.jsonl"
SESS_BASE = BASE / ".logging" / "sessions"
STATE_FILE = BASE / ".logging" / ".state.json"
SESS_BASE.mkdir(parents=True, exist_ok=True)

# ---------- helpers ----------
def ts_folder(val) -> str:
    """Return 'YYYY-MM-DD_HH-mm-ss' from ISO string or epoch (ms/sec)."""
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val/1000 if val > 1e12 else val).strftime("%Y-%m-%d_%H-%M-%S")
    if isinstance(val, str):
        try:
            dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d_%H-%M-%S")
        except Exception:
            pass
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def g(obj, *path, default=None):
    cur = obj
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur

def normalize(rec: dict) -> dict:
    """Extract common fields from the OTLP-ish record."""
    attrs = rec.get("attributes", {}) if isinstance(rec.get("attributes", {}), dict) else {}
    event = attrs.get("event.name") or rec.get("event") or rec.get("name") or ""
    t = attrs.get("event.timestamp") or rec.get("time") or None
    sid = attrs.get("session.id") or rec.get("sessionId") or rec.get("session_id") or "unknown"
    model = attrs.get("model", "")
    in_tok = attrs.get("input_token_count", "")
    out_tok = attrs.get("output_token_count", "")
    prompt = attrs.get("prompt", "") or ""
    resp = attrs.get("response_text", "") or ""
    tool_name = attrs.get("function_name", "") or ""
    tool_args = attrs.get("function_args", {}) or {}
    tool_ok = attrs.get("success", "")
    tool_dur = attrs.get("duration_ms", "")
    return {
        "event": event,
        "time": t,
        "sid": sid,
        "model": model,
        "in_tok": in_tok,
        "out_tok": out_tok,
        "prompt": prompt,
        "resp": resp,
        "tool_name": tool_name,
        "tool_args": tool_args,
        "tool_ok": tool_ok,
        "tool_dur": tool_dur,
    }

def open_session_folder(first_info: dict, suffix_bump: int = 0) -> Path:
    """Create a timestamped session folder; bump suffix if same-second collision."""
    stamp = ts_folder(first_info["time"])
    folder = SESS_BASE / (f"{stamp}__{suffix_bump}" if suffix_bump else stamp)
    i = suffix_bump
    while folder.exists():
        i += 1
        folder = SESS_BASE / f"{stamp}__{i}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def write_prompt(folder: Path, info: dict):
    with (folder / "prompts.log").open("a", encoding="utf-8") as f:
        f.write(f"[{ts_folder(info['time'])}] session={info['sid']}\n{info['prompt'].rstrip()}\n---\n")

def write_resp(folder: Path, info: dict):
    with (folder / "responses.log").open("a", encoding="utf-8") as f:
        f.write(
            f"[{ts_folder(info['time'])}] session={info['sid']} model={info['model']} "
            f"tokens(in={info['in_tok']},out={info['out_tok']})\n{info['resp'].rstrip()}\n---\n"
        )

def write_tool(folder: Path, info: dict):
    try:
        args_s = json.dumps(info["tool_args"], ensure_ascii=False)
    except Exception:
        args_s = str(info["tool_args"])
    with (folder / "tools.log").open("a", encoding="utf-8") as f:
        f.write(
            f"[{ts_folder(info['time'])}] session={info['sid']} tool={info['tool_name']} "
            f"success={info['tool_ok']} duration_ms={info['tool_dur']}\nargs={args_s}\n---\n"
        )

# ---------- state handling ----------
def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"processed_count": 0, "last_size": 0, "current_sid": None, "session_folder": None}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# ---------- processing ----------
def process_all(state: dict) -> dict:
    """
    Re-parse the file and process only NEW objects by skipping first N=processed_count.
    This avoids partial-object issues and keeps the code simple.
    """
    if not LOG_FILE.exists():
        return state

    size = LOG_FILE.stat().st_size
    # Detect truncation/rotation
    if size < state.get("last_size", 0):
        state["processed_count"] = 0
        state["current_sid"] = None
        state["session_folder"] = None

    processed = 0
    new_objs = 0
    session_folder: Optional[Path] = Path(state["session_folder"]) if state.get("session_folder") else None
    current_sid = state.get("current_sid")

    with LOG_FILE.open("rb") as f:
        try:
            # ijson will iterate over multiple concatenated JSON values
            records = ijson.items(f, "", multiple_values=True)
            for rec in records:
                processed += 1
                if processed <= state.get("processed_count", 0):
                    continue  # already handled in a previous run

                info = normalize(rec)

                # rotate session folder on session id change or if none yet
                if info["sid"] != current_sid or session_folder is None:
                    # new folder based on this record's timestamp
                    session_folder = open_session_folder(info)
                    current_sid = info["sid"]

                # route by event
                ev = info["event"]
                if ev == "gemini_cli.user_prompt":
                    write_prompt(session_folder, info)
                elif ev == "gemini_cli.api_response":
                    write_resp(session_folder, info)
                elif ev == "gemini_cli.tool_call":
                    write_tool(session_folder, info)
                # else ignore other events (config, metrics, etc.)

                new_objs += 1

        except Exception:
            # Likely trailing incomplete JSON while Gemini is writing; ignore for now.
            print("Failed to parse line:", rec)
            pass

    # update state
    state["processed_count"] = processed
    state["last_size"] = size
    state["current_sid"] = current_sid
    state["session_folder"] = str(session_folder) if session_folder else None
    if new_objs:
        save_state(state)
    return state

# ---------- watcher main ----------
async def main():
    # Ensure folder exists; don’t create/clear the log (user controls it)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Prime once (in case the file already has content)
    state = load_state()
    state = process_all(state)

    # React to changes
    async for changes in awatch(LOG_FILE.parent, debounce=150):
        # only act if our file changed
        if not any(str(p) == str(LOG_FILE) and (chg in (Change.modified, Change.added) or Change.deleted)
                   for chg, p in changes):
            continue
        # if deleted, just reset counters and wait for re-creation
        if any(chg == Change.deleted and str(p) == str(LOG_FILE) for chg, p in changes):
            state = {"processed_count": 0, "last_size": 0, "current_sid": None, "session_folder": None}
            save_state(state)
            continue
        # modified/added → (re)process
        state = process_all(state)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
