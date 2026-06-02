from pathlib import Path
from typing import Any

import yaml


SPEC_PATH = Path("openapi/calle.openapi.yaml")


def assert_contract(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"OpenAPI contract check failed: {message}")


def response_schema_ref(spec: dict[str, Any], path: str, method: str) -> str | None:
    endpoint = spec.get("paths", {}).get(path, {}).get(method, {})
    return (
        endpoint.get("responses", {})
        .get("200", {})
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
        spec.get("info", {}).get("version") == "0.1.0",
        "unexpected API version",
    )

    required_operations = [
        {
            "path": "/v1/calls",
            "method": "post",
            "operation_id": "createCall",
            "request_schema": "#/components/schemas/CreateCallRequest",
            "response_schema": "#/components/schemas/Call",
            "error_statuses": ["400", "401", "403", "409", "429", "500"],
        },
        {
            "path": "/v1/calls/{call_id}",
            "method": "get",
            "operation_id": "getCall",
            "response_schema": "#/components/schemas/Call",
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
            response_schema_ref(spec, path, method) == operation["response_schema"],
            f"unexpected 200 response schema for {label}",
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
    for ref in [
        "#/components/parameters/WebhookEventId",
        "#/components/parameters/WebhookTimestamp",
        "#/components/parameters/WebhookSignature",
    ]:
        assert_contract(ref in webhook_refs, f"missing webhook parameter {ref}")

    webhook_security = spec.get("paths", {}).get("/calle/webhook", {}).get("post", {}).get(
        "security"
    )
    assert_contract(webhook_security == [], "webhook endpoint must not require bearer auth")

    schemas = spec.get("components", {}).get("schemas", {})
    for schema_name in [
        "CreateCallRequest",
        "CallRecipient",
        "CallPolicy",
        "CallStatus",
        "ResultValidation",
        "Call",
        "DeveloperEvent",
        "EventList",
        "WebhookEventType",
        "WebhookEvent",
        "WebhookCallData",
        "WebhookAcknowledgement",
        "ErrorEnvelope",
        "APIError",
    ]:
        assert_contract(schema_name in schemas, f"missing schema {schema_name}")

    create_call_properties = schemas["CreateCallRequest"].get("properties", {})
    for property_name in [
        "task",
        "recipient",
        "result_schema",
        "policy",
        "metadata",
        "webhook_url",
    ]:
        assert_contract(
            property_name in create_call_properties,
            f"CreateCallRequest missing {property_name}",
        )

    assert_contract(
        "result_schema" in schemas["CreateCallRequest"].get("required", []),
        "CreateCallRequest must require result_schema",
    )

    call_properties = schemas["Call"].get("properties", {})
    for property_name in [
        "id",
        "status",
        "structured_result",
        "result_validation",
        "summary",
        "metadata",
        "created_at",
        "completed_at",
    ]:
        assert_contract(property_name in call_properties, f"Call missing {property_name}")

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

    print(f"Verified Phase 1 OpenAPI contract at {SPEC_PATH}.")


if __name__ == "__main__":
    main()
