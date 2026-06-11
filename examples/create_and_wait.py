import json
import os

from calle import CalleClient


def main() -> None:
    client = CalleClient(
        api_key=os.environ.get("CALLE_API_KEY", "calle_dev_example"),
        base_url=os.environ.get("CALLE_BASE_URL", "https://api.heycall-e.com"),
    )

    call = client.calls.create_and_wait(
        task="Call each recipient and ask whether they can attend Friday lunch in San Francisco.",
        recipients=[
            {
                "phones": [os.environ.get("CALLE_EXAMPLE_PHONE", "+14155550100")],
                "region": "US",
                "locale": "en-US",
            }
        ],
        result_schema={
            "type": "object",
            "required": ["completed_count"],
            "properties": {
                "completed_count": {"type": "integer"},
            },
        },
        recipient_result_schema={
            "type": "object",
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

    print(json.dumps(call, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
