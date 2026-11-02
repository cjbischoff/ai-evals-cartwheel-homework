"""Homework 2 tests for tool-span attributes and endpoint authentication.

The tests record spans with an in-memory exporter, so they need no Langfuse,
Docker, or model provider key.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from fastapi import HTTPException
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from agent import agent as support
from agent.auth import AuthContext, permission_denied
from observability.instrument import record_tool_result
from server import app as server_app
from tests.eval.fake_model import FakeModel, text_message


@pytest.fixture
def tracer():
    """Return a tracer and the exporter that collects its finished spans.

    Returns:
        A (tracer, exporter) pair that is independent of the global provider.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    return provider.get_tracer("test"), exporter


def _record(tracer, ctx: AuthContext, result: dict) -> dict:
    tracer, exporter = tracer
    with tracer.start_as_current_span("tool"):
        record_tool_result(ctx, result)
    return dict(exporter.get_finished_spans()[-1].attributes)


def test_tool_span_records_shopper_identity_and_allowed_call(tracer) -> None:
    attrs = _record(tracer, AuthContext(user_id=1, role="shopper"), {"ok": True})

    assert attrs == {
        "cartwheel.user_role": "shopper",
        "cartwheel.user_id": "1",
        "cartwheel.permission_denied": False,
    }


def test_tool_span_records_merchant_store_and_denial_reason(tracer) -> None:
    ctx = AuthContext(user_id=9001, role="merchant", store_id=1)
    attrs = _record(tracer, ctx, permission_denied("order belongs to another store"))

    assert attrs == {
        "cartwheel.user_role": "merchant",
        "cartwheel.user_id": "9001",
        "cartwheel.store_id": "1",
        "cartwheel.permission_denied": True,
        "cartwheel.permission_denied.reason": "order belongs to another store",
    }


def test_tool_span_treats_other_errors_as_not_denied(tracer) -> None:
    attrs = _record(
        tracer,
        AuthContext(user_id=9501, role="support"),
        {"ok": False, "error": "not_found", "reason": "no such order"},
    )

    assert attrs["cartwheel.permission_denied"] is False
    assert "cartwheel.permission_denied.reason" not in attrs


@pytest.mark.parametrize(
    ("user_id", "role", "status"),
    [
        (1, "admin", 400),  # not a known role
        (999999, "shopper", 404),  # no such user
        (1, "support", 403),  # user 1 is a shopper, not support
    ],
)
def test_create_session_rejects_unverified_identity(
    world: dict, user_id: int, role: str, status: int
) -> None:
    with pytest.raises(HTTPException) as exc:
        server_app.create_session(server_app.SessionCreate(user_id=user_id, role=role))

    assert exc.value.status_code == status


@pytest.fixture
def server(world: dict, tmp_path, monkeypatch):
    """Run the endpoint offline with a scripted model and an in-memory exporter.

    Returns:
        The exporter that collects the server's root spans.
    """
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    monkeypatch.setattr(server_app, "_tracer", provider.get_tracer("test"))
    monkeypatch.setattr(server_app, "SESSIONS_DB", tmp_path / "sessions.db")
    model = FakeModel()
    model.set_next_output([text_message("You have 3 orders.")])
    monkeypatch.setattr(support, "resolve_model", lambda _: model)
    server_app._SESSIONS.clear()
    yield exporter
    provider.shutdown()


def _send(session_id: str, token: str, message: str, **fields) -> dict:
    body = server_app.MessageIn(message=message, **fields)
    return asyncio.run(server_app.post_message(session_id, body, f"Bearer {token}"))


def test_post_message_records_root_span(server, monkeypatch) -> None:
    monkeypatch.setenv("TRACELOOP_TRACE_CONTENT", "true")
    session = server_app.create_session(server_app.SessionCreate(user_id=1, role="shopper"))

    reply = _send(session["session_id"], session["token"], "Show my orders.", scenario_id="s-1")

    assert reply == {
        "session_id": session["session_id"],
        "reply": "You have 3 orders.",
        "prompt_version": support.prompt_version(),
    }
    (span,) = [s for s in server.get_finished_spans() if s.name == "cartwheel.session_message"]
    attrs = span.attributes
    assert attrs["cartwheel.session_id"] == session["session_id"]
    assert attrs["cartwheel.user_role"] == "shopper"
    assert attrs["cartwheel.user_id"] == "1"
    assert attrs["cartwheel.prompt_version"] == support.prompt_version()
    assert attrs["cartwheel.scenario_id"] == "s-1"
    assert json.loads(attrs["gen_ai.input.messages"]) == [
        {"role": "user", "parts": [{"type": "text", "content": "Show my orders."}]}
    ]
    assert json.loads(attrs["gen_ai.output.messages"]) == [
        {"role": "assistant", "parts": [{"type": "text", "content": "You have 3 orders."}]}
    ]


def test_post_message_omits_content_and_empty_scenario(server, monkeypatch) -> None:
    monkeypatch.setenv("TRACELOOP_TRACE_CONTENT", "false")
    session = server_app.create_session(server_app.SessionCreate(user_id=1, role="shopper"))

    _send(session["session_id"], session["token"], "Show my orders.", scenario_id="")

    attrs = server.get_finished_spans()[-1].attributes
    assert "cartwheel.scenario_id" not in attrs
    assert "gen_ai.input.messages" not in attrs
    assert "gen_ai.output.messages" not in attrs


def test_token_for_one_session_cannot_authorize_another(server) -> None:
    first = server_app.create_session(server_app.SessionCreate(user_id=1, role="shopper"))
    second = server_app.create_session(server_app.SessionCreate(user_id=2, role="shopper"))

    with pytest.raises(HTTPException) as exc:
        _send(second["session_id"], first["token"], "Show my orders.")

    assert exc.value.status_code == 403
