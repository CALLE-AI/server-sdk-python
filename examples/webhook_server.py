import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

port = int(os.environ.get("PORT", "3000"))
processed_event_ids: set[str] = set()


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/calle/webhook":
            self._send_json(404, {"error": "not_found"})
            return

        raw_body = self.rfile.read(int(self.headers.get("content-length", "0")))

        try:
            parsed: Any = json.loads(raw_body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_json(400, {"error": "invalid_json"})
            return
        if not isinstance(parsed, dict):
            self._send_json(400, {"error": "invalid_event"})
            return
        event: dict[str, Any] = parsed

        event_id = self.headers.get("CALL-E-Event-Id")
        if not event_id or event.get("id") != event_id:
            self._send_json(400, {"error": "invalid_event_id"})
            return
        event_type = event.get("type")
        call = event.get("data")
        if (
            not isinstance(event_type, str)
            or not isinstance(call, dict)
            or not isinstance(call.get("id"), str)
        ):
            self._send_json(400, {"error": "invalid_event"})
            return
        call_id = call["id"]

        if event_id in processed_event_ids:
            self._send_json(200, {"received": True, "duplicate": True})
            return

        # Use durable storage in production and persist the id before side effects.
        processed_event_ids.add(event_id)

        if event_type == "call.completed":
            print(
                "Call completed",
                {
                    "call_id": call_id,
                    "result": call.get("structured_result"),
                    "summary": call.get("summary"),
                    "task_completed": call.get("task_completed"),
                    "completion_confidence": call.get("completion_confidence"),
                    "evidence": call.get("evidence"),
                },
            )
        else:
            print(
                "CALL-E webhook event",
                {
                    "id": event["id"],
                    "type": event_type,
                    "call_id": call_id,
                },
            )

        self._send_json(200, {"received": True})

    def _send_json(self, status_code: int, body: dict[str, Any]) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status_code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    server = HTTPServer(("127.0.0.1", port), WebhookHandler)
    print(f"CALL-E webhook server listening on http://localhost:{port}/calle/webhook")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping CALL-E webhook server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
