import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from context import create_human_decision, get_project_coverage, list_context, list_project_assessments, list_project_decisions, list_project_evidence, list_project_gaps, list_project_papers

ROOT = Path(__file__).resolve().parents[1]


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return str(ROOT / path.lstrip("/"))

    def send_json(self, payload, status=200):
        body = json.dumps(payload, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/context":
            self.send_json(list_context())
            return
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "papers":
            try:
                self.send_json(list_project_papers(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "evidence":
            try:
                self.send_json(list_project_evidence(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "coverage":
            try:
                self.send_json(get_project_coverage(parts[2]) or {})
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "gaps":
            try:
                self.send_json(list_project_gaps(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "assessments":
            try:
                self.send_json(list_project_assessments(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "decisions":
            try:
                self.send_json(list_project_decisions(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return

        super().do_GET()


    def do_POST(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "decisions":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length) or b"{}")
                row = create_human_decision(parts[2], payload.get("object_id"), payload.get("decision_type"), payload.get("rationale"), payload.get("actor"))
                self.send_json(row, status=201)
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        self.send_json({"error": "Not found"}, status=404)


ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
