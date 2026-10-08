#!/usr/bin/env python3
"""Serve Fernrel's character sheet on localhost and save edits back to disk.

Run:  python3 server.py          (then open http://localhost:8000)
      python3 server.py 8123     (pick another port)

Only needs Python 3.8+ and its standard library. Every save keeps a dated
copy of the previous sheet.json in backups/ (the newest 200 are kept).
"""
import base64
import http.server
import json
import re
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKUPS = ROOT / "backups"
KEEP_BACKUPS = 200
MAX_BODY = 40 * 1024 * 1024
WRITABLE = re.compile(r"^(sheet\.json|art/[A-Za-z0-9_-]+\.(jpg|jpeg|png|webp|gif))$")


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def back_up_sheet():
    sheet = ROOT / "sheet.json"
    if not sheet.exists():
        return
    BACKUPS.mkdir(exist_ok=True)
    stamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    (BACKUPS / f"sheet_{stamp}.json").write_bytes(sheet.read_bytes())
    for old in sorted(BACKUPS.glob("sheet_*.json"))[:-KEEP_BACKUPS]:
        old.unlink()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/ping":
            return self.send_json(200, {"ok": True})
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/save":
            return self.send_json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self.send_json(413, {"error": "too large"})
        try:
            body = json.loads(self.rfile.read(length))
            text, binary, remove = body.get("text", {}), body.get("binary", {}), body.get("remove", [])
            paths = list(text) + list(binary) + list(remove)
            bad = [p for p in paths if not WRITABLE.match(p)]
            if bad:
                return self.send_json(400, {"error": f"can't write {bad}"})
            if "sheet.json" in text:
                json.loads(text["sheet.json"])  # refuse to save broken data
                back_up_sheet()
            for path, content in text.items():
                write_atomic(ROOT / path, content.encode("utf-8"))
            for path, content in binary.items():
                write_atomic(ROOT / path, base64.b64decode(content))
            for path in remove:
                (ROOT / path).unlink(missing_ok=True)
        except (ValueError, KeyError, TypeError) as e:
            return self.send_json(400, {"error": str(e)})
        return self.send_json(200, {"ok": True})

    def log_message(self, fmt, *args):
        if self.command == "POST":
            sys.stderr.write("saved %s\n" % time.strftime("%H:%M:%S"))


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}"
    print(f"Fernrel's sheet is at {url}  (Ctrl+C to stop)")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
