"""Request routers for research measurements and process optimization."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException
from .schemas import (
    Observation, EvaluationResponse, OptimizationCandidate, OptimizationRequest,
)
from .physics import estimate_melt_pool
from .risk import score_defects
from .optimizer import optimize_parameters
from .domain import SUPPORTED_MATERIALS
from .repository import DEMO_BUILDS
from .state_machine import gate_status
from .events import EventJournal


router = APIRouter(prefix="/api/v1")
journal = EventJournal()


@router.get("/materials")
async def materials() -> dict[str, object]:
    return {"materials": list(SUPPORTED_MATERIALS), "synthetic": True}


@router.get("/builds")
async def builds() -> list[dict[str, object]]:
    return [record.model_dump(mode="json") for record in DEMO_BUILDS]


@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate(observation: Observation) -> EvaluationResponse:
    estimate = estimate_melt_pool(observation)
    risk = score_defects(observation, estimate)
    journal.append("evaluation_completed", {
        "material": observation.material,
        "layer": observation.layer_number,
        "risk": risk.overall_risk,
    })
    return EvaluationResponse(observation=observation, physics=estimate, risk=risk)


@router.post("/optimize", response_model=list[OptimizationCandidate])
async def optimize(request: OptimizationRequest) -> list[OptimizationCandidate]:
    return optimize_parameters(request)


@router.get("/qualification/{build_id}")
async def qualification(build_id: str) -> dict[str, object]:
    if not any(build.id == build_id for build in DEMO_BUILDS):
        raise HTTPException(status_code=404, detail="Build not found")
    return {"build_id": build_id, "gates": gate_status(build_id)}


@router.get("/events")
async def events(limit: int = 50) -> list[dict[str, object]]:
    return journal.recent(limit=limit)
