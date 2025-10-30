#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["ijson>=3.2.3", "filelock>=3.12.0"]
# ///
"""
Gemini CLI API Request Processor

Extracts API request/response/error events from the telemetry log file
and outputs them as a structured JSON file grouped by prompt_id.

Usage:
    uv run .logging/process-api-requests.py [options]

Options:
    --no-clear          Don't clear the log file after processing
    --output-dir PATH   Output directory (default: .logging)
    --verbose          Enable verbose debug output
    --help             Show this help message
"""

from __future__ import annotations
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

import ijson
from filelock import FileLock, Timeout

# ---------- Configuration ----------
BASE = Path(".")
LOG_FILE = BASE / ".logging" / "log.jsonl"
LOCK_FILE = BASE / ".logging" / ".process.lock"
DEFAULT_OUTPUT_DIR = BASE / ".logging" / "requests"

# Event types we care about
EVENT_REQUEST = "gemini_cli.api_request"
EVENT_RESPONSE = "gemini_cli.api_response"
EVENT_ERROR = "gemini_cli.api_error"

# ---------- Helper Functions ----------
def timestamp_now() -> str:
    """Return current timestamp in YYYY-MM-DD_HH-mm-ss format."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def get_existing_sessions(output_dir: Path) -> Dict[str, Path]:
    """
    Scan output directory for existing session files.
    Returns dict mapping session_id -> file_path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    sessions = {}

    # Pattern: YYYY-MM-DD_HH-MM-SS-{session-id}.json
    pattern = re.compile(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-(.+)\.json')

    for file_path in output_dir.glob("*.json"):
        match = pattern.match(file_path.name)
        if match:
            session_id = match.group(7)  # Group 7 captures the session ID
            sessions[session_id] = file_path

    return sessions

def load_session_file(file_path: Path) -> List[dict]:
    """Load existing session data from file."""
    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load {file_path.name}: {e}")
        return []

def extract_attributes(record: dict) -> dict:
    """Extract attributes from OTLP-style record."""
    return record.get("attributes", {}) if isinstance(record.get("attributes"), dict) else {}

def get_prompt_id(attrs: dict) -> Optional[str]:
    """Extract prompt_id from attributes."""
    return attrs.get("prompt_id")

def get_session_id(attrs: dict) -> Optional[str]:
    """Extract session.id from attributes."""
    return attrs.get("session.id")

def get_event_timestamp(record: dict) -> Optional[str]:
    """Extract timestamp from record."""
    # Try different timestamp fields
    return (record.get("timestamp") or
            record.get("event_timestamp") or
            record.get("time"))

def get_event_name(record: dict) -> Optional[str]:
    """Extract event name from record."""
    attrs = extract_attributes(record)
    return attrs.get("event.name") or record.get("event") or record.get("name")

def parse_json_fields(attrs: dict, fields: List[str], verbose: bool = False) -> dict:
    """
    Parse JSON string fields into objects for cleaner output.

    Args:
        attrs: Attribute dictionary potentially containing JSON strings
        fields: List of field names to attempt parsing
        verbose: Enable debug output

    Returns:
        New dict with parsed fields
    """
    result = attrs.copy()

    for field in fields:
        if field in result and isinstance(result[field], str):
            try:
                parsed = json.loads(result[field])
                result[field] = parsed
                if verbose:
                    print(f"   ✓ Parsed JSON field: {field}")
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                # Keep as string if parsing fails
                if verbose:
                    print(f"   ⚠ Could not parse {field}: {e}")
                pass

    return result

# Fields that commonly contain JSON strings
JSON_STRING_FIELDS = [
    "request_text",
    "response_text",
    "function_args",  # tool arguments might be JSON strings
]

# ---------- Event Processing ----------
def save_session_data(session_id: str, session_data: dict, first_timestamp: str,
                     existing_sessions: dict, output_dir: Path, verbose: bool) -> Path:
    """
    Save session data to file.
    Handles both new and existing session files.
    """
    # Convert dict to list format
    data_list = list(session_data.values())

    # Determine output file path
    if session_id in existing_sessions:
        # Update existing file
        output_file = existing_sessions[session_id]
        if verbose:
            print(f"   💾 Updating: {output_file.name}")

        # For existing files, just overwrite with updated data
        temp_file = output_file.with_suffix(".tmp")
        with temp_file.open("w", encoding="utf-8") as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        temp_file.replace(output_file)
    else:
        # Create new file
        if verbose:
            print(f"   💾 Creating new session file")
        output_file = save_session_file(data_list, session_id, first_timestamp or "", output_dir)

    return output_file

def process_log_file(log_path: Path, output_dir: Path, verbose: bool = False) -> Dict[str, any]:
    """
    Parse log file and extract API events grouped by session.
    Processes records in order and creates/updates session files as needed.

    Returns:
        Dict with processing statistics
    """
    if not log_path.exists():
        print(f"❌ Log file not found: {log_path}")
        return {}

    # Get existing sessions
    existing_sessions = get_existing_sessions(output_dir)
    print(f"📂 Found {len(existing_sessions)} existing session file(s)")

    # Stats
    stats = {
        "total_records": 0,
        "requests": 0,
        "responses": 0,
        "errors": 0,
        "skipped": 0,
        "sessions_processed": 0,
        "sessions_updated": 0,
        "sessions_created": 0
    }

    # Current session tracking
    current_session_id = None
    current_session_data = {}  # prompt_id -> {prompt_id, request, response, error}
    current_session_first_timestamp = None
    session_files_written = []

    print(f"📖 Reading log file: {log_path}")
    print(f"⏳ Processing events...")

    with log_path.open("rb") as f:
        try:
            records = ijson.items(f, "", multiple_values=True)

            for record in records:
                stats["total_records"] += 1

                # Progress indicator
                if verbose and stats["total_records"] % 100 == 0:
                    print(f"   Processed {stats['total_records']} records...")

                # Extract metadata
                event_name = get_event_name(record)
                attrs = extract_attributes(record)
                prompt_id = get_prompt_id(attrs)
                session_id = get_session_id(attrs)
                timestamp = get_event_timestamp(record)

                # Skip records without session_id or prompt_id
                if not session_id or not prompt_id:
                    stats["skipped"] += 1
                    continue

                # Check if session changed
                if current_session_id is not None and session_id != current_session_id:
                    # Save current session before switching
                    if current_session_data:
                        file_path = save_session_data(
                            current_session_id,
                            current_session_data,
                            current_session_first_timestamp,
                            existing_sessions,
                            output_dir,
                            verbose
                        )
                        session_files_written.append(file_path)
                        stats["sessions_processed"] += 1

                        if current_session_id in existing_sessions:
                            stats["sessions_updated"] += 1
                        else:
                            stats["sessions_created"] += 1

                    # Reset for new session
                    current_session_data = {}
                    current_session_first_timestamp = None

                # Set current session
                if current_session_id != session_id:
                    current_session_id = session_id
                    print(f"🔄 Processing session: {session_id}")

                    # Load existing data if session file exists
                    if session_id in existing_sessions:
                        print(f"   ↪ Appending to existing session file")
                        existing_data = load_session_file(existing_sessions[session_id])
                        # Convert list to dict keyed by prompt_id
                        for entry in existing_data:
                            # Extract prompt_id from request, response, or error attributes
                            entry_prompt_id = None
                            if entry.get("request") and "prompt_id" in entry["request"]:
                                entry_prompt_id = entry["request"]["prompt_id"]
                            elif entry.get("response") and "prompt_id" in entry["response"]:
                                entry_prompt_id = entry["response"]["prompt_id"]
                            elif entry.get("error") and "prompt_id" in entry["error"]:
                                entry_prompt_id = entry["error"]["prompt_id"]

                            if entry_prompt_id:
                                current_session_data[entry_prompt_id] = entry

                # Track first timestamp for this session
                if current_session_first_timestamp is None and timestamp:
                    current_session_first_timestamp = timestamp

                # Initialize entry if needed
                if prompt_id not in current_session_data:
                    current_session_data[prompt_id] = {
                        "request": None,
                        "response": None,
                        "error": None
                    }

                # Process based on event type (parse JSON fields before storing)
                if event_name == EVENT_REQUEST:
                    current_session_data[prompt_id]["request"] = parse_json_fields(attrs, JSON_STRING_FIELDS, verbose)
                    stats["requests"] += 1
                    if verbose:
                        print(f"   ✓ Request: {prompt_id}")

                elif event_name == EVENT_RESPONSE:
                    current_session_data[prompt_id]["response"] = parse_json_fields(attrs, JSON_STRING_FIELDS, verbose)
                    stats["responses"] += 1
                    if verbose:
                        print(f"   ✓ Response: {prompt_id}")

                elif event_name == EVENT_ERROR:
                    current_session_data[prompt_id]["error"] = parse_json_fields(attrs, JSON_STRING_FIELDS, verbose)
                    stats["errors"] += 1
                    if verbose:
                        print(f"   ✓ Error: {prompt_id}")
                else:
                    stats["skipped"] += 1

            # Save final session
            if current_session_id and current_session_data:
                file_path = save_session_data(
                    current_session_id,
                    current_session_data,
                    current_session_first_timestamp,
                    existing_sessions,
                    output_dir,
                    verbose
                )
                session_files_written.append(file_path)
                stats["sessions_processed"] += 1

                if current_session_id in existing_sessions:
                    stats["sessions_updated"] += 1
                else:
                    stats["sessions_created"] += 1

        except Exception as e:
            print(f"⚠️  Warning: Error parsing log file: {e}")
            if verbose:
                import traceback
                traceback.print_exc()

    stats["session_files"] = session_files_written
    return stats

def format_output(grouped_events: Dict[str, Dict[str, any]], parse_json: bool = True, verbose: bool = False) -> List[dict]:
    """
    Format grouped events into output array structure.
    Each entry has request, response, and error fields (may be null).

    Args:
        grouped_events: Events grouped by prompt_id
        parse_json: Whether to parse JSON string fields into objects
        verbose: Enable debug output
    """
    output = []

    for prompt_id, events in grouped_events.items():
        # Parse JSON fields if requested
        if parse_json:
            request = parse_json_fields(events.get("request") or {}, JSON_STRING_FIELDS, verbose) if events.get("request") else None
            response = parse_json_fields(events.get("response") or {}, JSON_STRING_FIELDS, verbose) if events.get("response") else None
            error = parse_json_fields(events.get("error") or {}, JSON_STRING_FIELDS, verbose) if events.get("error") else None
        else:
            request = events.get("request")
            response = events.get("response")
            error = events.get("error")

        entry = {
            "request": request,
            "response": response,
            "error": error
        }
        output.append(entry)

    return output

def save_session_file(data: List[dict], session_id: str, first_timestamp: str, output_dir: Path) -> Path:
    """
    Save session data to file.
    Filename format: {first_timestamp}-{session_id}.json
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Format timestamp for filename (YYYY-MM-DD_HH-MM-SS)
    try:
        # Parse ISO timestamp and format for filename
        dt = datetime.fromisoformat(first_timestamp.replace('Z', '+00:00'))
        timestamp_str = dt.strftime("%Y-%m-%d_%H-%M-%S")
    except:
        # Fallback to current time if parsing fails
        timestamp_str = timestamp_now()

    output_file = output_dir / f"{timestamp_str}-{session_id}.json"

    # Write to temp file first, then replace (atomic operation)
    temp_file = output_file.with_suffix(".tmp")

    with temp_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    temp_file.replace(output_file)

    return output_file

def clear_log_file(log_path: Path, verbose: bool = False):
    """Clear the log file content."""
    if verbose:
        print(f"🧹 Clearing log file: {log_path}")

    with log_path.open("w", encoding="utf-8") as f:
        f.write("")  # Truncate to empty

def print_summary(stats: dict):
    """Print processing summary."""
    print("\n" + "="*60)
    print("📊 Processing Summary")
    print("="*60)
    print(f"Total records processed:  {stats['total_records']}")
    print(f"API requests found:       {stats['requests']}")
    print(f"API responses found:      {stats['responses']}")
    print(f"API errors found:         {stats['errors']}")
    print(f"Records skipped:          {stats['skipped']}")
    print(f"\nSessions processed:       {stats['sessions_processed']}")
    print(f"  - New sessions:         {stats['sessions_created']}")
    print(f"  - Updated sessions:     {stats['sessions_updated']}")

    if stats.get('session_files'):
        print(f"\n✅ Session files:")
        for file_path in stats['session_files']:
            size = file_path.stat().st_size
            print(f"   - {file_path.name} ({size:,} bytes)")

    print("="*60)

# ---------- Main Function ----------
def main():
    # Fix encoding for Windows console
    import sys
    import io
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(
        description="Process Gemini CLI API request telemetry logs",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Don't clear the log file after processing"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose debug output"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Keep JSON strings as-is (don't parse to objects)"
    )

    args = parser.parse_args()

    print("🚀 Gemini CLI API Request Processor")
    print("="*60)

    # Check if log file exists
    if not LOG_FILE.exists():
        print(f"❌ Error: Log file not found: {LOG_FILE}")
        print(f"   Make sure Gemini CLI has run with telemetry enabled.")
        return 1

    # Check if log file is empty
    if LOG_FILE.stat().st_size == 0:
        print(f"⚠️  Warning: Log file is empty: {LOG_FILE}")
        print(f"   No data to process.")
        return 0

    # Acquire file lock
    lock = FileLock(LOCK_FILE, timeout=10)

    try:
        print(f"🔒 Acquiring file lock...")
        with lock:
            print(f"✓ Lock acquired\n")

            # Process log file
            stats = process_log_file(LOG_FILE, args.output_dir, args.verbose)

            if stats.get('sessions_processed', 0) == 0:
                print(f"\n⚠️  No sessions found in log file.")
                return 0

            # Clear log file if requested
            if not args.no_clear:
                clear_log_file(LOG_FILE, args.verbose)
                print(f"\n✓ Log file cleared")
            else:
                print(f"\n⚠️  Log file NOT cleared (--no-clear specified)")

            # Print summary
            print_summary(stats)

            return 0

    except Timeout:
        print(f"\n❌ Error: Could not acquire file lock (timeout after 10s)")
        print(f"   Another process may be using the log file.")
        print(f"   Please try again later or check for running processes.")
        return 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    finally:
        # Release lock (happens automatically with context manager)
        if lock.is_locked:
            print(f"\n🔓 Releasing file lock...")

if __name__ == "__main__":
    import sys
    sys.exit(main())
