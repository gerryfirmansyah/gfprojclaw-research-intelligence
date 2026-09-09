import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from context import list_context

ROOT = Path(__file__).resolve().parents[1]

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(ROOT / path.lstrip("/"))

    def do_GET(self):
        if self.path == "/api/context":
            rows = list_context()
            body = json.dumps(rows, default=str).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
