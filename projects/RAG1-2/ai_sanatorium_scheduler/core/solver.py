from __future__ import annotations
from typing import Any, Dict, List

from ortools.sat.python import cp_model


class SchedulerSolver:
    """Minimal CP-SAT solver stub. Encodes a trivial problem and returns a dummy schedule.

    In the real implementation, encode resources, time slots, and constraints.
    """

    def __init__(self) -> None:
        self.model = cp_model.CpModel()

    def solve(self, requests: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
        # Trivial CP-SAT variable just to exercise the solver
        x = self.model.NewBoolVar("x")
        self.model.Add(x == 1)

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 1.0
        status = solver.Solve(self.model)

        schedule = {
            "status": cp_model.OPTIMAL if status == cp_model.OPTIMAL else status,
            "assignments": [
                {
                    "patient_id": 1,
                    "procedure_id": 1,
                    "room_id": 101,
                    "staff_id": 1001,
                    "start": "09:00",
                    "end": "09:30",
                }
            ],
        }
        return schedule
