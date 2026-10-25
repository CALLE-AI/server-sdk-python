import argparse
import json
import os
import shlex
import sys

from calle import CalleAPIError, CalleClient, CalleConnectionError, CalleTimeoutError


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--call-id", help="Resume waiting for an existing Call without creating another.")
    args = parser.parse_args()
    if args.call_id is not None and not args.call_id.strip():
        parser.error("--call-id must not be empty")

    with CalleClient(
        api_key=os.environ.get("CALLE_API_KEY", "calle_dev_example"),
        base_url=os.environ.get("CALLE_BASE_URL", "https://api.heycall-e.com"),
    ) as client:
        try:
            if args.call_id is not None:
                call = client.calls.wait_for_result(args.call_id)
            else:
                call = client.calls.create_and_wait(
                    task="Call the recipient and ask whether they can attend Friday lunch in San Francisco.",
                    phone=os.environ.get("CALLE_EXAMPLE_PHONE", "+14155550100"),
                    region="US", locale="en-US",
                    result_schema={
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["can_attend"],
                        "properties": {
                            "can_attend": {"type": "string", "enum": ["yes", "no", "unknown"]},
                        },
                    },
                    metadata={"workflow_run_id": "example_local"},
                    idempotency_key="example_local_friday_lunch",
                    interval_seconds=2.0,
                    timeout_seconds=600.0,
                )
        except (CalleAPIError, CalleConnectionError, CalleTimeoutError) as error:
            if error.call_id is not None:
                print(
                    "Resume this Call with: uv run python examples/create_and_wait.py "
                    f"--call-id {shlex.quote(error.call_id)}",
                    file=sys.stderr,
                )
            else:
                print("No Call ID received. Retry only with the same request and idempotency key.", file=sys.stderr)
            raise

    print(json.dumps(call, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
