from __future__ import annotations
from typing import Any, Dict, List

from ai_sanatorium_scheduler.core.solver import SchedulerSolver


class SchedulerService:
    def __init__(self) -> None:
        self.solver = SchedulerSolver()

    def run_schedule(self, requests: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
        # TODO: load inputs from DB, validate, map to solver inputs
        result = self.solver.solve(requests=requests or [])
        # TODO: persist schedule results to DB
        return result
