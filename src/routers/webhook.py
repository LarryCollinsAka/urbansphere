from fastapi import APIRouter, Request, Response
from pydantic import BaseModel, Field
from typing import Optional
from twilio.twiml.messaging_response import MessagingResponse

from src.services.brenda import route as brenda_route
from src.services import waste, queue as queue_agent, realestate

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])

#  Pydantic schema (used in OpenAPI docs) 
class WhatsAppInbound(BaseModel):
    From: Optional[str] = Field(
        None, description="Sender MSISDN in WhatsApp format",
        examples=["whatsapp:+237700000000"]
    )
    Body: Optional[str] = Field(
        None, description="Message text body",
        examples=["Trash is piling up at Nlongkak"]
    )
    # Optional Twilio fields you may see, keep them for future use:
    ProfileName: Optional[str] = None
    WaId: Optional[str] = None

# Build a custom OpenAPI requestBody that shows BOTH JSON and form payloads
openapi_extra_webhook = {
    "requestBody": {
        "required": True,
        "content": {
            "application/json": {
                "schema": WhatsAppInbound.model_json_schema(),
                "example": {
                    "From": "whatsapp:+237700000000",
                    "Body": "Any rooms near Bonamoussadi under 150k?"
                },
            },
            "application/x-www-form-urlencoded": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "From": {"type": "string", "example": "whatsapp:+237700000000"},
                        "Body": {"type": "string", "example": "Trash at Nlongkak market entrance"}
                    },
                    "required": ["From", "Body"]
                },
                "example": "From=whatsapp:+237700000000&Body=Trash at Bodija"
            },
        },
    }
}

@router.post("/testjson")
async def whatsapp_testjson(req: Request):
    """Swagger-friendly echo that tolerates empty bodies (JSON or form)."""
    body = {}
    # Try JSON
    try:
        body = await req.json()
        if not isinstance(body, dict):
            body = {}
    except Exception:
        # Try form
        try:
            form = await req.form()
            body = dict(form)
        except Exception:
            body = {}

    text = (body.get("Body") or body.get("message_text") or "").strip()
    from_ = body.get("From") or body.get("from") or "whatsapp:unknown"
    return {"ok": True, "echo": {"From": from_, "Body": text}}

@router.post("/ping")
async def ping():
    """Simple TwiML ping to prove Twilio-style response path works."""
    tw = MessagingResponse()
    tw.message("pong")
    return Response(content=str(tw), media_type="application/xml")

@router.post("/webhook", openapi_extra=openapi_extra_webhook)
async def webhook(req: Request) -> Response:
    """
    Twilio webhook: accepts application/x-www-form-urlencoded (default) or JSON.
    Always returns TwiML so WhatsApp gets an immediate reply.
    """
    try:
        ctype = (req.headers.get("content-type") or "").lower()
        if "application/json" in ctype:
            body = await req.json()
            text = (body.get("Body") or body.get("message_text") or "").strip()
            msisdn = body.get("From") or body.get("from") or "whatsapp:unknown"
        else:
            # requires: python-multipart
            form = await req.form()
            text = (form.get("Body") or form.get("message_text") or "").strip()
            msisdn = form.get("From") or form.get("from") or "whatsapp:unknown"

        routed = brenda_route(text)
        intent = routed.get("intent") or "clarify"
        ent = routed.get("entities") or {}

        if intent == "sanita_report":
            msg = waste.handle_report(msisdn, ent)
        elif intent in ("queue_join", "queue_status"):
            msg = queue_agent.handle(msisdn, intent, ent)
        elif intent == "property_lookup":
            msg = realestate.lookup(ent)
        else:
            msg = {"user_friendly_text": "Do you want waste, queue, or property help?"}

        reply_text = msg.get("user_friendly_text") or "Got it."
    except Exception as e:
        reply_text = f"Oops—temporary issue on our side: {str(e)[:160]}"

    tw = MessagingResponse()
    tw.message(reply_text)
    return Response(content=str(tw), media_type="application/xml")
