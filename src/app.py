
from pathlib import Path
import os
import asyncio

from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.routers.webhook import router as webhook_router

app = FastAPI(title="UrbanSphere MVP")

# --- Resolve paths relative to this file (src/) ---
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Ensure templates dir exists so TemplateResponse won't blow up later
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Only mount /static if the folder actually exists (avoids RuntimeError)
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Routers
app.include_router(webhook_router)

@app.on_event("startup")
async def _warm_up():
    """
    Never block app startup. Optionally skip warmup entirely with WX_SKIP_WARMUP=1.
    Any health check runs in the background.
    """
    if os.getenv("WX_SKIP_WARMUP") in ("1", "true", "True"):
        print("[startup] skipping watsonx warm-up (WX_SKIP_WARMUP=1)")
        return

    async def _do_check():
        try:
            # Import inside task to avoid doing it at import time
            from src.services import watsonx_client
            # run the (fast) health_check off the event loop
            ok = await asyncio.to_thread(watsonx_client.health_check)
            print(f"[startup] watsonx health_check={ok}")
        except Exception as e:
            print(f"[startup] warm-up failed: {e}")

    asyncio.create_task(_do_check())
    print("[startup] scheduled watsonx health_check in background")

# Minimal dashboard (demo-friendly)
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, cdn: str = Query(default="play")):
    use_link = (cdn.lower() == "link")
    counts = dict(waste_count=2, queue_count=1, property_count=3)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "use_link": use_link, **counts},
    )

# Convenience redirect
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/dashboard")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
