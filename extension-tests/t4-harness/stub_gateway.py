#!/usr/bin/env python3
"""T4 stub model gateway: chat, embeddings and health, with a request journal.

Implements the parts of the existing gateway API the runtime calls:
  POST /v1/inference/chat        fixed answer; the request (including the system
                                 prompt carrying the retrieved context) is journalled
  POST /v1/inference/embeddings  embeddings from embedding.embed(); the request
                                 (profile, inputs, attributes) is journalled
  GET  /v1/health                UP
Harness endpoints:
  GET  /__journal                every journalled request, oldest first
  POST /__reset                  clears the journal

Usage: stub_gateway.py <port>
"""
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from embedding import embed  # noqa: E402

JOURNAL, LOCK = [], threading.Lock()
CHAT_RESPONSE = {"content": "Answer drawn from the retrieved context.", "provider": "stub",
                 "model": "stub-model", "finishReason": "STOP",
                 "usage": {"inputTokens": 120, "outputTokens": 14, "cachedInputTokens": 0},
                 "cost": {"inputCost": "0.00012000", "outputCost": "0.00002800", "currency": "USD"}}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, body):
        data = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/v1/health":
            self.reply(200, {"status": "UP", "providers": {"stub": "UP"}})
        elif self.path == "/__journal":
            with LOCK:
                self.reply(200, list(JOURNAL))
        else:
            self.reply(404, {"error": "not found"})

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        if self.path == "/__reset":
            with LOCK:
                JOURNAL.clear()
            self.reply(200, {"reset": True})
            return
        with LOCK:
            JOURNAL.append({"path": self.path, "body": body})
        if self.path == "/v1/inference/chat":
            self.reply(200, CHAT_RESPONSE)
        elif self.path == "/v1/inference/embeddings":
            inputs = body.get("inputs") or []
            self.reply(200, {"embeddings": [embed(text) for text in inputs], "provider": "stub",
                             "model": "stub-embedding",
                             "usage": {"inputTokens": len(inputs), "outputTokens": 0, "cachedInputTokens": 0},
                             "cost": {"inputCost": "0", "outputCost": "0", "currency": "USD"}})
        else:
            self.reply(404, {"error": "not found"})


if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
