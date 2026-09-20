import json
import os, shutil, subprocess
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from context import create_human_decision, get_project_quality, get_project_coverage, get_project_corpus_layers, get_project_daily_attention, list_context, list_project_advice_critic, list_project_assessments, list_project_changes, list_project_decisions, list_project_evidence, list_project_evidence_verification, list_project_gaps, list_project_opportunities, list_project_papers, list_project_radar, list_project_research_objects, list_project_pilot_health, update_research_profile, update_research_project, update_profile_project_configuration

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

    def operational_health(self):
        def unit(name):
            p=subprocess.run(["systemctl","show",name,"-p","LoadState","-p","ActiveState","-p","SubState","-p","UnitFileState","-p","Result","--no-pager"],capture_output=True,text=True,timeout=3)
            return dict(line.split("=",1) for line in p.stdout.splitlines() if "=" in line)
        disk=shutil.disk_usage("/")
        backup_dir=Path("/opt/gfprojclaw/backups"); dumps=sorted(backup_dir.glob("gfprojclaw-*.dump"),key=lambda p:p.stat().st_mtime,reverse=True) if backup_dir.exists() else []
        latest=dumps[0] if dumps else None
        return {"generated_at":datetime.now(timezone.utc).isoformat(),"services":{"api":unit("gfprojclaw-cockpit-api.service"),"telegram_timer":unit("gfprojclaw-status-telegram.timer"),"backup_timer":unit("gfprojclaw-backup.timer"),"legacy_g6_g9":unit("gfprojclaw-g6-g9.service"),"continuous_pilot_timer":unit("gfprojclaw-continuous-pilot.timer")},"storage":{"total_bytes":disk.total,"used_bytes":disk.used,"free_bytes":disk.free,"used_percent":round(disk.used*100/disk.total,1)},"backup":{"count":len(dumps),"latest_name":latest.name if latest else None,"latest_bytes":latest.stat().st_size if latest else None,"latest_mtime":datetime.fromtimestamp(latest.stat().st_mtime,timezone.utc).isoformat() if latest else None},"scientific_decision":False}

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/admin/operational-health":
            try: self.send_json(self.operational_health())
            except Exception as exc: self.send_json({"error":str(exc)},status=500)
            return
        if path == "/api/admin/activity-audit":
            try:
                log=Path("/var/log/gfprojclaw-activity.log")
                lines=log.read_text(errors="replace").splitlines()[-80:] if log.exists() else []
                self.send_json({"entries":lines,"source":"gfprojclaw-activity.log" if log.exists() else "NOT_AVAILABLE","scientific_decision":False})
            except Exception as exc: self.send_json({"error":str(exc)},status=500)
            return
        if path == "/api/context":
            self.send_json(list_context())
            return
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "daily-attention":
            try:
                query = __import__("urllib.parse", fromlist=["parse_qs"]).parse_qs(urlparse(self.path).query)
                hours = int((query.get("hours") or [24])[0])
                self.send_json(get_project_daily_attention(parts[2], hours))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
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
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "evidence-verification":
            try:
                query = __import__("urllib.parse", fromlist=["parse_qs"]).parse_qs(urlparse(self.path).query)
                object_id = (query.get("object_id") or [None])[0]
                self.send_json(list_project_evidence_verification(parts[2], object_id))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "coverage":
            try:
                self.send_json(get_project_coverage(parts[2]) or {})
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "corpus-layers":
            try:
                self.send_json(get_project_corpus_layers(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "research-objects":
            try:
                self.send_json(list_project_research_objects(parts[2]))
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
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "changes":
            try:
                self.send_json(list_project_changes(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "opportunities":
            try:
                self.send_json(list_project_opportunities(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "advice-critic":
            try:
                self.send_json(list_project_advice_critic(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "radar":
            try:
                self.send_json(list_project_radar(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "pilot-health":
            try:
                self.send_json(list_project_pilot_health(parts[2]))
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "quality":
            try:
                query = __import__("urllib.parse", fromlist=["parse_qs"]).parse_qs(urlparse(self.path).query)
                object_id = (query.get("object_id") or [None])[0]
                row = get_project_quality(parts[2], object_id)
                self.send_json(row or {}, status=200 if row else 404)
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


    def do_PUT(self):
        path = urlparse(self.path).path; parts = path.strip("/").split("/")
        try:
            length=int(self.headers.get("Content-Length","0")); payload=json.loads(self.rfile.read(length) or b"{}")
            if parts==["api","admin","profile-project-configuration"]:
                self.send_json(update_profile_project_configuration(payload.get("profile_id"),payload.get("project_id"),payload.get("profile") or {},payload.get("project") or {},payload.get("actor"),payload.get("reason"))); return
            if len(parts)==3 and parts[:2]==["api","profiles"]:
                self.send_json(update_research_profile(parts[2],payload.get("name"),payload.get("summary"),payload.get("configuration"),payload.get("actor"))); return
            if len(parts)==3 and parts[:2]==["api","projects"]:
                self.send_json(update_research_project(parts[2],payload.get("name"),payload.get("research_intent"),payload.get("provisional_rq_text"),payload.get("configuration"),payload.get("actor"))); return
            self.send_json({"error":"Not found"},status=404)
        except Exception as exc: self.send_json({"error":str(exc)},status=400)

    def do_POST(self):
        path = urlparse(self.path).path
        parts = path.strip("/").split("/")
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "projects" and parts[3] == "decisions":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length) or b"{}")
                row = create_human_decision(parts[2], payload.get("object_id"), payload.get("decision_type"), payload.get("rationale"), payload.get("actor"), payload.get("assessment_id"))
                self.send_json(row, status=201)
            except Exception as exc:
                self.send_json({"error": str(exc)}, status=400)
            return
        self.send_json({"error": "Not found"}, status=404)


ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
