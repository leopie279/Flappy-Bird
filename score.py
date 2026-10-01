from http.server import BaseHTTPRequestHandler
import json

# Catatan: penyimpanan in-memory (bersifat sementara di serverless Vercel)
DATA = {"best": 0}


class handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send(200, {"ok": True})

    def do_GET(self):
        self._send(200, {"best": DATA["best"]})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            body = json.loads(raw.decode("utf-8"))
            score = int(body.get("score", 0))
        except Exception:
            self._send(400, {"error": "Data tidak valid"})
            return

        if 0 <= score <= 100000 and score > DATA["best"]:
            DATA["best"] = score
        self._send(200, {"best": DATA["best"]})
