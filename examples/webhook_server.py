import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from calle import CalleClient, CalleWebhookSignatureError


client = CalleClient(api_key=os.environ.get("CALLE_API_KEY", "calle_dev_example"))
webhook_secret = os.environ.get("CALLE_WEBHOOK_SECRET", "whsec_dev_example")
port = int(os.environ.get("PORT", "3000"))


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/calle/webhook":
            self._send_json(404, {"error": "not_found"})
            return

        raw_body = self.rfile.read(int(self.headers.get("content-length", "0")))

        try:
            event = client.webhooks.unwrap(
                raw_body=raw_body,
                headers=dict(self.headers.items()),
                secret=webhook_secret,
            )
        except CalleWebhookSignatureError:
            self._send_json(400, {"error": "invalid_signature"})
            return

        if event["type"] == "call.completed":
            print(
                "Call completed",
                {
                    "call_id": event["data"]["id"],
                    "result": event["data"].get("structured_result"),
                },
            )
        else:
            print(
                "CALL-E webhook event",
                {
                    "id": event["id"],
                    "type": event["type"],
                    "call_id": event["data"]["id"],
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
