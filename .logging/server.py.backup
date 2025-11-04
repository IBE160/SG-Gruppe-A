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


class CORSRequestHandler(SimpleHTTPRequestHandler):
    """HTTP request handler with CORS headers enabled."""

    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
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
                    timestamp = None

                    # Match session-based format: YYYY-MM-DD_HH-MM-SS-{session-id}.json
                    match = re.match(r'(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})-(.+)\.json', json_file.name)
                    if match:
                        year, month, day, hour, minute, second, session_id = match.groups()
                        timestamp = f"{year}-{month}-{day}T{hour}:{minute}:{second}"

                    files.append({
                        'filename': json_file.name,
                        'timestamp': timestamp,
                        'size': stat.st_size
                    })

                self.wfile.write(json.dumps(files).encode())
            else:
                self.wfile.write(b'[]')
            return

        # Default file serving
        super().do_GET()

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
