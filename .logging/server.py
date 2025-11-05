#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""
Simple HTTP server for API Request Viewer

Serves the .logging directory with CORS headers enabled and automatically
opens the viewer in your default browser.

Usage:
    uv run .logging/server.py [port]
    python .logging/server.py [port]

Default port: 8000
"""

import sys
import json
import re
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, quote


def to_kebab_case(text):
    """Convert text to kebab-case format.
    
    Examples:
        'Fase 1 started' -> 'fase-1-started'
        'Test Session #3' -> 'test-session-3'
        'My_Test-Title' -> 'my-test-title'
    """
    if not text or not text.strip():
        return None
    
    # Lowercase
    text = text.lower().strip()
    
    # Replace any sequence of non-alphanumeric chars with a single hyphen
    import re
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    return text if text else None


def sanitize_title(title):
    """Sanitize title to kebab-case format with length limit."""
    if not title or not title.strip():
        return None
    
    # Limit length before conversion
    title = title.strip()
    if len(title) > 100:
        title = title[:100]
    
    # Convert to kebab-case
    return to_kebab_case(title)


def parse_session_filename(filename):
    """Parse session filename to extract timestamp and title.
    
    Handles both new and old formats:
    - New: {timestamp}-{kebab-title}.json
    - Old: {timestamp}-{session_id}--{title}.json (backwards compatibility)
    
    Returns:
        dict with 'timestamp' and 'title', or None if invalid
        Note: session_id is NOT in new filenames, must be loaded from JSON
    """
    name = filename.replace(".json", "")
    
    # Check for old format with '--' separator
    if "--" in name:
        base_part, title_part = name.split("--", 1)
        # Convert title back from kebab-case (replace - with spaces)
        title = title_part.replace("-", " ")
    else:
        # New format: timestamp-title (no -- separator)
        base_part = name
        title = None
    
    # Extract timestamp (always first part: YYYY-MM-DD_HH-MM-SS)
    match = re.match(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})-(.+)$", base_part)
    if match:
        timestamp_str, title_or_id = match.groups()
        
        # If no title was found from '--' separator, use the part after timestamp
        if title is None:
            # This is the kebab-case title (or session ID for untitled sessions)
            title = title_or_id
        
        return {"timestamp": timestamp_str, "title": title}
    
    return None


def build_session_filename(timestamp, session_id, title=None):
    """Build session filename in format: {timestamp}-{kebab-title}.json
    
    Args:
        timestamp: Timestamp string in YYYY-MM-DD_HH-MM-SS format
        session_id: Session UUID (used as default title if no custom title)
        title: Optional custom title (will be kebab-cased)
    
    Returns:
        Filename like '2025-10-30_01-13-48-fase-1-started.json' (with title)
        or '2025-10-30_01-13-48-afd0b49e-1f92-456d-a6ff-afba8ef9a39f.json' (untitled)
    """
    if title:
        sanitized = sanitize_title(title)
        if sanitized:
            return f"{timestamp}-{sanitized}.json"
    
    # Use session_id as default title (already in kebab-case format)
    return f"{timestamp}-{session_id}.json"


class CORSRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers enabled."""

    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        """Handle GET requests, including API endpoints."""
        # API endpoint to list JSON files
        if self.path == '/api/files':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Get all JSON files from requests/ folder
            requests_dir = Path('requests')
            if requests_dir.exists():
                files = []
                for json_file in sorted(requests_dir.glob('*.json'), reverse=True):
                    stat = json_file.stat()

                    # Parse filename to extract timestamp and title
                    parsed = parse_session_filename(json_file.name)
                    if parsed:
                        timestamp_str = parsed['timestamp']
                        year, month, day = timestamp_str.split('_')[0].split('-')
                        time_part = timestamp_str.split('_')[1]
                        hour, minute, second = time_part.split('-')
                        timestamp = f"{year}-{month}-{day}T{hour}:{minute}:{second}"
                        
                        # Extract session ID from JSON content
                        session_id = None
                        try:
                            with json_file.open('r', encoding='utf-8') as f:
                                data = json.load(f)
                                # Get session.id from first request
                                if data and len(data) > 0:
                                    first_item = data[0]
                                    if 'request' in first_item and first_item['request']:
                                        session_id = first_item['request'].get('session.id')
                        except Exception:
                            # If we can't read the file, use title as fallback
                            session_id = parsed['title']

                        files.append({
                            'filename': json_file.name,
                            'timestamp': timestamp,
                            'sessionId': session_id,
                            'title': parsed['title'],
                            'size': stat.st_size
                        })

                self.wfile.write(json.dumps(files).encode())
            else:
                self.wfile.write(b'[]')
            return

        # Default file serving
        super().do_GET()

    def do_PUT(self):
        """Handle PUT requests for API endpoints."""
        # API endpoint to rename session file
        if self.path == '/api/sessions/rename':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                current_filename = data.get('currentFilename')
                new_title = data.get('newTitle')

                if not current_filename:
                    self.send_error(400, 'Missing currentFilename')
                    return

                if not new_title or not new_title.strip():
                    self.send_error(400, 'Missing or empty newTitle')
                    return

                # Strip 'requests/' prefix if present (frontend sends full path)
                if current_filename.startswith('requests/'):
                    current_filename = current_filename[9:]  # Remove 'requests/'

                # Parse current filename
                parsed = parse_session_filename(current_filename)
                if not parsed:
                    self.send_error(400, 'Invalid filename format')
                    return

                # Build new filename (session_id=None since we have a title)
                new_filename = build_session_filename(
                    parsed['timestamp'],
                    None,  # Session ID not needed when we have a custom title
                    new_title
                )

                # Rename the file
                requests_dir = Path('requests')
                old_path = requests_dir / current_filename
                new_path = requests_dir / new_filename

                if not old_path.exists():
                    self.send_error(404, 'File not found')
                    return

                if new_path.exists() and new_path != old_path:
                    self.send_error(409, 'File with that name already exists')
                    return

                old_path.rename(new_path)

                # Return success with new filename
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': True,
                    'newFilename': new_filename,
                    'title': new_title
                }
                self.wfile.write(json.dumps(response).encode())

            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
            except Exception as e:
                self.send_error(500, str(e))
            return

        # Unknown endpoint
        self.send_error(404, 'Not found')


    def do_DELETE(self):
        """Handle DELETE requests for API endpoints."""
        # API endpoint to delete session file
        if self.path == '/api/sessions/delete':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                filename = data.get('filename')

                if not filename:
                    self.send_error(400, 'Missing filename')
                    return

                # Strip 'requests/' prefix if present (frontend sends full path)
                if filename.startswith('requests/'):
                    filename = filename[9:]  # Remove 'requests/'

                # Validate filename
                requests_dir = Path('requests')
                file_path = requests_dir / filename

                # Security check: ensure file is within requests directory
                try:
                    file_path = file_path.resolve()
                    if not str(file_path).startswith(str(requests_dir.resolve())):
                        self.send_error(400, 'Invalid file path')
                        return
                except Exception:
                    self.send_error(400, 'Invalid file path')
                    return

                if not file_path.exists():
                    self.send_error(404, 'File not found')
                    return

                # Delete the file
                file_path.unlink()

                # Return success
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    'success': True,
                    'message': 'Session deleted successfully'
                }
                self.wfile.write(json.dumps(response).encode())

            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
            except Exception as e:
                self.send_error(500, str(e))
            return

        # Unknown endpoint
        self.send_error(404, 'Not found')


    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight."""
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """Customize log messages to be more concise."""
        if args[1] == '200':
            # Only log non-200 responses to reduce noise
            return
        super().log_message(format, *args)


def main():
    # Fix encoding for Windows console
    import io
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    # Parse port from command line args
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            print("Usage: python server.py [port]")
            sys.exit(1)

    # Change to .logging directory
    script_dir = Path(__file__).parent
    import os
    os.chdir(script_dir)

    # Create server
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)

    # Print startup message
    url = f'http://localhost:{port}/api-viewer.html'
    print('='*60)
    print('🚀 API Request Viewer Server')
    print('='*60)
    print(f'Server running at: http://localhost:{port}')
    print(f'Viewer URL: {url}')
    print('\nPress Ctrl+C to stop the server')
    print('='*60)

    # Open browser
    print('\n📱 Opening browser...')
    webbrowser.open(url)

    # Run server
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n\n👋 Shutting down server...')
        httpd.shutdown()
        print('✅ Server stopped')


if __name__ == '__main__':
    main()
