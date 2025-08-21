# src/services/brenda.py
import os, time, concurrent.futures
from typing import Any, Dict
from src.services.watsonx_client import generate_json

SYSTEM = (
  "You are Brenda, an intent router for a civic assistant handling: "
  "sanita_report (waste), queue_join, queue_status, property_lookup. "
  "Extract entities (location, waste_type, service, property_type, budget, urgency). "
  "Return ONLY valid JSON exactly matching: "
  '{"intent":"...", "confidence":0-1, "entities":{...}, "safety_flags":[], "trace":{"version":"brenda.v1","latency_ms":0}}. '
  "If unsure, set intent='clarify' and include entities.question."
)

LLM_TIMEOUT = float(os.getenv("BRENDA_LLM_TIMEOUT", "3.0"))
FORCE_OFFLINE = os.getenv("BRENDA_FORCE_OFFLINE") == "1"

def _offline_fallback(text: str) -> Dict[str, Any]:
    low = (text or "").lower()
    def pack(intent: str, entities: Dict[str, Any] | None = None, note: str = "offline_fallback"):
        return {"intent": intent, "confidence": 0.30, "entities": entities or {},
                "safety_flags": [], "trace": {"version": "brenda.v1", "latency_ms": 0, "note": note}}
    if any(k in low for k in ["waste","trash","garbage","refuse","sanitation"]): return pack("sanita_report")
    if "queue" in low and any(k in low for k in ["join","enrol","enroll","enter","add"]): return pack("queue_join")
    if "queue" in low: return pack("queue_status")
    if any(k in low for k in ["house","apartment","rent","property","room","real estate","estate"]): return pack("property_lookup")
    return {"intent":"clarify","confidence":0.0,"entities":{"question":"Do you need waste, queue, or property help?"},
            "safety_flags":[],"trace":{"version":"brenda.v1","latency_ms":0,"note":"offline_fallback"}}

def route(text: str) -> Dict[str, Any]:
    t0 = time.time()
    prompt = f"<system>{SYSTEM}</system>\n<user>{text}</user>"

    if FORCE_OFFLINE:
        data = _offline_fallback(text)
    else:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
                fut = ex.submit(generate_json, prompt)
                data = fut.result(timeout=LLM_TIMEOUT)
            if not isinstance(data, dict) or "error" in data:
                raise RuntimeError(data.get("error","json_parse_failed") if isinstance(data, dict) else "bad_response")
        except Exception:
            data = _offline_fallback(text)

    # normalize
    data.setdefault("intent", "clarify")
    data.setdefault("entities", {})
    data.setdefault("safety_flags", [])
    data.setdefault("trace", {})
    try:
        data["confidence"] = max(0.0, min(1.0, float(data.get("confidence", 0) or 0)))
    except Exception:
        data["confidence"] = 0.0
    data["trace"]["version"] = "brenda.v1"
    data["trace"]["latency_ms"] = int((time.time() - t0) * 1000)
    return data
