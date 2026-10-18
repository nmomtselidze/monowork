from __future__ import annotations
from typing import Any, Dict, List, Optional

import orjson
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse

from ai_sanatorium_scheduler.core.services import SchedulerService


class ORJSONResponseCustom(ORJSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)


app = FastAPI(title="AI-Sanatorium Scheduler API", default_response_class=ORJSONResponseCustom)


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/schedule/run")
def run_schedule(payload: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    service = SchedulerService()
    result = service.run_schedule(requests=payload or [])
    return result
