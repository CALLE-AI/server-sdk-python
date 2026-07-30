from pathlib import Path
from typing import Any

import yaml


SPEC_PATH = Path("openapi/calle.openapi.yaml")


def assert_contract(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"OpenAPI contract check failed: {message}")


def response_schema_ref(spec: dict[str, Any], path: str, method: str, status: str = "200") -> str | None:
    endpoint = spec.get("paths", {}).get(path, {}).get(method, {})
    return (
        endpoint.get("responses", {})
        .get(status, {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
        .get("$ref")
    )


def request_schema_ref(spec: dict[str, Any], path: str, method: str) -> str | None:
    endpoint = spec.get("paths", {}).get(path, {}).get(method, {})
    return (
        endpoint.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
        .get("$ref")
    )


def parameter_refs(spec: dict[str, Any], path: str, method: str) -> list[str | None]:
    endpoint = spec.get("paths", {}).get(path, {}).get(method, {})
    return [parameter.get("$ref") for parameter in endpoint.get("parameters", [])]


def main() -> None:
    spec = yaml.safe_load(SPEC_PATH.read_text(encoding="utf-8"))

    assert_contract(spec.get("openapi") == "3.1.0", "expected OpenAPI 3.1.0")
    assert_contract(
        spec.get("info", {}).get("title") == "CALL-E Developer API",
        "unexpected title",
    )
    assert_contract(
        spec.get("info", {}).get("version") == "0.6.0",
        "unexpected API version",
    )

    required_operations = [
        {
            "path": "/v1/calls",
            "method": "post",
            "operation_id": "createCall",
            "request_schema": "#/components/schemas/CreateCallRequest",
            "response_status": "201",
            "response_schema": "#/components/schemas/CallTask",
            "error_statuses": ["400", "401", "403", "409", "422", "429", "500"],
        },
        {
            "path": "/v1/calls/{call_id}",
            "method": "get",
            "operation_id": "getCall",
            "response_schema": "#/components/schemas/CallTask",
            "error_statuses": ["401", "403", "404", "429", "500"],
        },
        {
            "path": "/v1/calls/{call_id}/events",
            "method": "get",
            "operation_id": "listCallEvents",
            "response_schema": "#/components/schemas/EventList",
            "error_statuses": ["401", "403", "404", "429", "500"],
        },
        {
            "path": "/v1/goals",
            "method": "get",
            "operation_id": "listGoals",
            "response_schema": "#/components/schemas/GoalList",
            "error_statuses": ["400", "401", "403", "409", "429", "500"],
        },
        {
            "path": "/v1/goals/{goal_id}",
            "method": "get",
            "operation_id": "getGoal",
            "response_schema": "#/components/schemas/Goal",
            "error_statuses": ["401", "403", "404", "409", "429", "500", "502", "503"],
        },
        {
            "path": "/v1/goals/{goal_id}/runs",
            "method": "post",
            "operation_id": "createGoalRun",
            "request_schema": "#/components/schemas/CreateGoalRunRequest",
            "response_status": "201",
            "response_schema": "#/components/schemas/GoalRun",
            "error_statuses": [
                "400",
                "401",
                "402",
                "403",
                "404",
                "409",
                "422",
                "429",
                "500",
                "502",
                "503",
            ],
        },
        {
            "path": "/v1/goals/{goal_id}/runs/{goal_run_id}",
            "method": "get",
            "operation_id": "getGoalRun",
            "response_schema": "#/components/schemas/GoalRun",
            "error_statuses": ["401", "403", "404", "429", "500", "502", "503"],
        },
        {
            "path": "/calle/webhook",
            "method": "post",
            "operation_id": "receiveWebhookEvent",
            "request_schema": "#/components/schemas/WebhookEvent",
            "response_schema": "#/components/schemas/WebhookAcknowledgement",
            "error_statuses": [],
        },
    ]

    for operation in required_operations:
        path = operation["path"]
        method = operation["method"]
        endpoint = spec.get("paths", {}).get(path, {}).get(method)
        label = f"{method.upper()} {path}"
        assert_contract(endpoint is not None, f"missing {label}")
        assert_contract(
            endpoint.get("operationId") == operation["operation_id"],
            f"unexpected operationId for {label}",
        )
        assert_contract(
            response_schema_ref(spec, path, method, operation.get("response_status", "200"))
            == operation["response_schema"],
            f"unexpected {operation.get('response_status', '200')} response schema for {label}",
        )

        request_schema = operation.get("request_schema")
        if request_schema is not None:
            assert_contract(
                request_schema_ref(spec, path, method) == request_schema,
                f"unexpected request schema for {label}",
            )

        for status in operation["error_statuses"]:
            assert_contract(
                endpoint.get("responses", {}).get(status, {}).get("$ref")
                == "#/components/responses/ErrorResponse",
                f"missing stable {status} error response for {label}",
            )

    webhook_refs = parameter_refs(spec, "/calle/webhook", "post")
    assert_contract(
        webhook_refs == ["#/components/parameters/WebhookEventId"],
        "webhook endpoint must expose only the event id header",
    )
    parameters = spec.get("components", {}).get("parameters", {})
    assert_contract(
        "WebhookTimestamp" not in parameters and "WebhookSignature" not in parameters,
        "webhook contract must not define legacy signature parameters",
    )

    webhook_security = spec.get("paths", {}).get("/calle/webhook", {}).get("post", {}).get(
        "security"
    )
    assert_contract(webhook_security == [], "webhook endpoint must not require bearer auth")

    schemas = spec.get("components", {}).get("schemas", {})
    for schema_name in [
        "CreateCallRequest",
        "CallTaskRecipientRequest",
        "CallStatus",
        "CompletionConfidence",
        "RecipientStatus",
        "AttemptStatus",
        "TranscriptSpeaker",
        "CallTranscriptTurn",
        "CallTaskAttempt",
        "CallTaskRecipient",
        "CallTask",
        "DeveloperEvent",
        "EventList",
        "WebhookEventType",
        "WebhookEvent",
        "WebhookCallData",
        "WebhookAcknowledgement",
        "GoalList",
        "Goal",
        "GoalPublishedRunSpec",
        "CreateGoalRunRequest",
        "GoalVariables",
        "GoalRun",
        "GoalRunSpecSnapshot",
        "GoalRunStatus",
        "GoalRunError",
        "ErrorEnvelope",
        "APIError",
    ]:
        assert_contract(schema_name in schemas, f"missing schema {schema_name}")

    assert_contract(
        schemas["WebhookCallData"].get("allOf")
        == [{"$ref": "#/components/schemas/CallTask"}],
        "webhook data must reuse the complete call task shape",
    )
    terminal_result_fields = {
        "structured_result",
        "summary",
        "task_completed",
        "completion_confidence",
        "evidence",
        "completed_at",
    }
    assert_contract(
        terminal_result_fields.issubset(set(schemas["CallTask"].get("required", []))),
        "complete terminal result fields must remain required in webhook call data",
    )

    create_call_properties = schemas["CreateCallRequest"].get("properties", {})
    for property_name in [
        "task",
        "recipients",
        "result_schema",
        "recipient_result_schema",
        "metadata",
        "webhook_url",
    ]:
        assert_contract(
            property_name in create_call_properties,
            f"CreateCallRequest missing {property_name}",
        )

    assert_contract(
        schemas["CreateCallRequest"].get("required", []) == ["task"],
        "CreateCallRequest must require only task",
    )

    call_properties = schemas["CallTask"].get("properties", {})
    for property_name in [
        "id",
        "object",
        "status",
        "task",
        "recipients",
        "structured_result",
        "summary",
        "task_completed",
        "completion_confidence",
        "evidence",
        "metadata",
        "created_at",
        "completed_at",
    ]:
        assert_contract(property_name in call_properties, f"CallTask missing {property_name}")

    assert_contract("result_validation" not in call_properties, "CallTask must not expose result_validation")

    event_list_data_ref = (
        schemas["EventList"]
        .get("properties", {})
        .get("data", {})
        .get("items", {})
        .get("$ref")
    )
    assert_contract(
        event_list_data_ref == "#/components/schemas/DeveloperEvent",
        "EventList.data must contain DeveloperEvent items",
    )

    create_goal_run = schemas["CreateGoalRunRequest"]
    create_goal_run_properties = create_goal_run.get("properties", {})
    assert_contract(
        sorted(create_goal_run_properties) == ["phone", "variables"],
        "CreateGoalRunRequest must contain only phone and variables",
    )
    assert_contract(
        create_goal_run.get("required") == ["phone"],
        "CreateGoalRunRequest must require only phone",
    )
    assert_contract(
        create_goal_run.get("additionalProperties") is False,
        "CreateGoalRunRequest must reject unknown fields",
    )

    goal_properties = schemas["Goal"].get("properties", {})
    for property_name in [
        "id",
        "title",
        "description",
        "status",
        "published_run_spec",
    ]:
        assert_contract(property_name in goal_properties, f"Goal missing {property_name}")

    published_run_spec_properties = schemas["GoalPublishedRunSpec"].get("properties", {})
    for checksum in [
        "semantic_checksum",
        "input_schema_checksum",
        "result_schema_checksum",
    ]:
        assert_contract(checksum not in goal_properties, f"Goal must not expose {checksum}")
        assert_contract(
            checksum not in published_run_spec_properties,
            f"GoalPublishedRunSpec must not expose {checksum}",
        )

    goal_run_properties = schemas["GoalRun"].get("properties", {})
    for property_name in [
        "id",
        "goal_id",
        "run_id",
        "run_spec",
        "status",
        "result",
        "error",
        "created_at",
        "completed_at",
    ]:
        assert_contract(
            property_name in goal_run_properties,
            f"GoalRun missing {property_name}",
        )

    goal_run_parameter_refs = parameter_refs(
        spec,
        "/v1/goals/{goal_id}/runs",
        "post",
    )
    assert_contract(
        "#/components/parameters/GoalRunIdempotencyKey" in goal_run_parameter_refs,
        "create Goal Run must require the stable idempotency header",
    )

    print(f"Verified CALL-E OpenAPI contract at {SPEC_PATH}.")


if __name__ == "__main__":
    main()
