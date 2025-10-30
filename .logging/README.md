# Gemini CLI Telemetry Processing Scripts

This directory contains scripts for processing and analyzing Gemini CLI telemetry logs.

## Scripts

### `process-api-requests.py`

Extracts API request, response, and error events from the telemetry log file and outputs them as structured JSON grouped by `prompt_id`.

**Features:**
- ✅ File locking to prevent concurrent access
- ✅ Groups request/response/error events by `prompt_id`
- ✅ Outputs timestamped JSON files
- ✅ Progress feedback during processing
- ✅ Automatic log file clearing after successful processing
- ✅ Handles incomplete JSON gracefully

### `watcher.py`

Real-time watcher that monitors telemetry logs and organizes them into session folders. See script header for details.

## File Structure

The logging directory is organized as follows:

```
.logging/
├── process-api-requests.py  # Main processing script
├── watcher.py               # Real-time telemetry watcher
├── server.py                # HTTP server for viewer
├── api-viewer.html          # Interactive web viewer
├── requests/                # Generated API request files
│   └── api-requests-*.json  # Individual request/response logs
├── log.jsonl                # Raw telemetry log file
└── README.md                # This file
```

## Quick Start

### 1. Process Telemetry Logs

No setup required! Just run:

```bash
uv run .logging/process-api-requests.py
```

The `uv` tool automatically handles dependencies defined in the script header. Output files are saved to `.logging/requests/`.

### 2. View Results in Browser

Start the viewer server:

```bash
uv run .logging/server.py
```

The server will automatically open the API Request Viewer in your browser at `http://localhost:8000/api-viewer.html`. See the [API Request Viewer](#api-request-viewer) section below for details on all features.

### Options

```bash
# Don't clear the log file after processing
uv run .logging/process-api-requests.py --no-clear

# Specify custom output directory
uv run .logging/process-api-requests.py --output-dir ./my-output

# Enable verbose debug output
uv run .logging/process-api-requests.py --verbose

# Keep JSON strings raw (don't parse into objects)
uv run .logging/process-api-requests.py --raw

# Combine options
uv run .logging/process-api-requests.py --no-clear --verbose --output-dir ./output

# Show help
uv run .logging/process-api-requests.py --help
```

## Setting Up for Debugging in VSCode

### 1. Create a Virtual Environment (Optional)

If you want to debug in VSCode with breakpoints:

```bash
# Create virtual environment
python -m venv .logging/.venv

# Activate it (Windows Git Bash)
source .logging/.venv/Scripts/activate

# Or on Linux/Mac
source .logging/.venv/bin/activate

# Install dependencies
pip install -r .logging/requirements.txt
```

### 2. Configure VSCode Debugger

A debug configuration has been added to `.vscode/launch.json`. To use it:

1. Open the script in VSCode: `.logging/process-api-requests.py`
2. Set breakpoints by clicking in the gutter
3. Press `F5` or go to **Run > Start Debugging**
4. Select **"Python: Process API Requests"** from the dropdown

### 3. Debug Configuration Options

The debug config includes several launch configurations:

- **Process API Requests (Default)**: Normal run with log clearing
- **Process API Requests (No Clear)**: Run without clearing the log
- **Process API Requests (Verbose)**: Run with verbose debug output

## JSON Parsing Feature

By default, the script **automatically parses JSON strings** embedded in telemetry fields into proper JSON objects. This makes the output much more readable and easier to work with.

### What Gets Parsed

The following fields are automatically parsed from strings to objects:
- `request_text` - The API request payload
- `response_text` - The API response data
- `function_args` - Tool function arguments

### Example

**Without parsing (--raw flag):**
```json
{
  "request_text": "[{\"role\":\"user\",\"parts\":[{\"text\":\"Hello\"}]}]"
}
```

**With parsing (default):**
```json
{
  "request_text": [
    {
      "role": "user",
      "parts": [
        {"text": "Hello"}
      ]
    }
  ]
}
```

### Disabling Parsing

If you need the original string format (for compatibility or debugging), use the `--raw` flag:
```bash
uv run .logging/process-api-requests.py --raw
```

## Output Format

The script generates files in `.logging/requests/` named `api-requests-YYYY-MM-DD_HH-mm-ss.json` with this structure:

```json
[
  {
    "prompt_id": "abc123",
    "request": {
      "model": "gemini-2.0-flash-exp",
      "prompt_id": "abc123",
      "request_text": "What is 2+2?"
    },
    "response": {
      "model": "gemini-2.0-flash-exp",
      "status_code": 200,
      "duration_ms": 1234,
      "input_token_count": 10,
      "output_token_count": 5,
      "total_token_count": 15,
      "response_text": "2+2 equals 4",
      "prompt_id": "abc123",
      "auth_type": "api_key"
    },
    "error": null
  },
  {
    "prompt_id": "def456",
    "request": {
      "model": "gemini-2.0-flash-exp",
      "prompt_id": "def456"
    },
    "response": null,
    "error": {
      "model": "gemini-2.0-flash-exp",
      "error": "Rate limit exceeded",
      "error_type": "rate_limit",
      "status_code": 429,
      "duration_ms": 500,
      "prompt_id": "def456",
      "auth_type": "api_key"
    }
  }
]
```

## Event Types

The script extracts these telemetry events:

- **`gemini_cli.api_request`**: API request attributes (model, prompt_id, request_text)
- **`gemini_cli.api_response`**: API response attributes (status, tokens, response_text)
- **`gemini_cli.api_error`**: API error attributes (error message, error_type, status_code)

Events are matched by their `prompt_id` attribute.

## File Locking

The script uses `filelock` to ensure exclusive access to the log file during processing. If another process is using the log file, you'll see:

```
❌ Error: Could not acquire file lock (timeout after 10s)
   Another process may be using the log file.
   Please try again later or check for running processes.
```

## Telemetry Configuration

Make sure telemetry is enabled in `.gemini/settings.json`:

```json
{
  "telemetry": {
    "enabled": true,
    "target": "local",
    "outfile": ".logging/log.jsonl",
    "logPrompts": true
  }
}
```

## Troubleshooting

### Script won't run
- Make sure `uv` is installed: `pip install uv`
- Check that Python 3.10+ is available

### No events found
- Verify telemetry is enabled in `.gemini/settings.json`
- Check that `.logging/log.jsonl` exists and has content
- Run Gemini CLI with some prompts to generate telemetry

### File lock timeout
- Stop any running `watcher.py` instances
- Close any text editors that may have the log file open
- Wait a few seconds and try again

### Incomplete JSON errors
- This is normal if Gemini is currently writing to the log
- The script handles this gracefully and processes complete records
- Run the script again after Gemini finishes

## Dependencies

- **ijson** (>=3.2.3): Streaming JSON parser for handling large log files efficiently
- **filelock** (>=3.12.0): Cross-platform file locking to prevent concurrent access
- **watchfiles** (>=0.21): Only needed for `watcher.py`

## API Request Viewer

An interactive HTML viewer is available to browse and analyze processed API request logs. The viewer provides a continuous chat experience that intelligently displays conversation history without duplication.

### Opening the Viewer

Both scripts (`process-api-requests.py` and `server.py`) are standalone uv scripts and can be run directly:

```bash
uv run .logging/server.py
```

Or using standard Python:
```bash
python .logging/server.py
```

The server will:
- ✅ Start a local HTTP server on port 8000
- ✅ Automatically open the viewer in your default browser
- ✅ Serve files with proper CORS headers
- ✅ Dynamically list all available request files via API endpoint

Press `Ctrl+C` to stop the server when you're done.

**Custom Port:**
```bash
uv run .logging/server.py 9000  # Use port 9000 instead
python .logging/server.py 9000  # Or with standard Python
```

**Note:** `server.py` has no external dependencies (uses only Python standard library), so both methods work identically.

### Key Features

#### 💬 Continuous Chat Display
- **Smart Differential Rendering**: Automatically handles cumulative conversation history from the Gemini API
- **No Duplication**: Uses intelligent algorithms to show only new messages, avoiding repetition of historical context
- **Session-Based Files**: Organizes logs by session ID format: `YYYY-MM-DD_HH-MM-SS-{session-id}.json`
- **Merged Messages**: Consecutive messages from the same role are automatically merged into single cards for better readability
- **Concatenated Text**: Multi-part text responses are seamlessly concatenated as continuous strings

#### 🎨 Visual Design
- **Color-Coded Messages**:
  - 🟦 Blue cards for user messages
  - 🟩 Green cards for model responses
  - Clear visual distinction for easy conversation flow
- **Collapsible Sidebar**: Burger menu (☰) to hide/show file browser
  - Collapses to icon-only view for maximum content space
  - Smooth transitions and animations
  - Aligned headers regardless of sidebar state
- **Responsive Layout**: Optimized for all screen sizes

#### 📋 Message Management
- **Copy Buttons**: Every message card has a subtle copy button (📋) in the top-right corner
  - Copies full message text including truncated content
  - Visual feedback with checkmark (✓) on success
  - Handles function calls and responses correctly
- **Text Truncation**: Long messages are automatically truncated with "Double-click to expand/collapse" functionality

#### 📁 File Browser
- Left sidebar lists all session files sorted by timestamp (newest first)
- One-click file switching
- Session ID display at the top of each conversation
- Clear visual indication of selected file

#### 📊 Rich Content Display
- **Function Calls**: Formatted JSON with syntax highlighting
- **Function Responses**: Expandable/collapsible output display
- **Token Metrics**: Real-time display of:
  - Input tokens
  - Output tokens (including thoughts tokens)
  - Cached content tokens
  - Total token count
- **Performance Data**: Request duration in milliseconds
- **Model Information**: Model name badges and version info

### What's Displayed

For each conversation session:

**Session Header:**
- Session ID for tracking
- Timestamp information

**User Messages:**
- Blue cards with "user" role label
- Text content with proper formatting
- Function call requests (when applicable)

**Model Responses:**
- Green cards with "model" role label
- Generated text responses
- Function execution results
- Thought processes (when included by model)

**Metadata:**
- HTTP status codes
- Request/response duration
- Token usage breakdown
- Error information (when applicable)

### File Format

The viewer expects JSON files with this session-based structure:

```json
[
  {
    "request": {
      "session.id": "uuid-here",
      "model": "gemini-2.5-flash",
      "request_text": [
        {
          "role": "user",
          "parts": [{"text": "Hello"}]
        }
      ],
      "prompt_id": "session-id########1"
    },
    "response": {
      "session.id": "uuid-here",
      "model": "gemini-2.5-flash",
      "status_code": 200,
      "duration_ms": 1234,
      "input_token_count": 10,
      "output_token_count": 5,
      "total_token_count": 15,
      "response_text": [
        {
          "candidates": [
            {
              "content": {
                "role": "model",
                "parts": [{"text": "Hello! How can I help you?"}]
              }
            }
          ]
        }
      ]
    },
    "error": null
  }
]
```

### Tips & Usage

- **Auto-Load**: The most recent session file loads automatically on page open
- **File Selection**: Click any file in the sidebar to view that session
- **Copy Content**: Click the copy button (📋) on any message to copy its full text
- **Expand Text**: Double-click on truncated messages to expand/collapse
- **Hide Sidebar**: Click the burger menu (☰) to maximize reading space
- **Keyboard-Friendly**: All interactive elements are keyboard-accessible
- **No Size Limits**: Handles large conversation histories efficiently
- **Offline Support**: Works completely offline once files are loaded

### Technical Details

**Differential Rendering Algorithm:**
The viewer uses a smart differential algorithm that:
1. Tracks how many message parts have been rendered
2. Only renders NEW parts from each API request (avoiding cumulative duplication)
3. Skips model messages in request history (they're rendered from response_text)
4. Groups consecutive same-role messages into single cards
5. Concatenates text parts for continuous reading

**Session ID Extraction:**
- Primary: Uses `session.id` field when available
- Fallback: Extracts from `prompt_id` pattern (uuid########N)

**Performance:**
- Lazy loading of file content
- Efficient DOM updates
- Minimal memory footprint
- Fast switching between sessions

## License

Part of the Gemini CLI project.
