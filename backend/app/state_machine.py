"""Deterministic process qualification transitions and evidence gates."""
from __future__ import annotations

from .schemas import BuildStage


ALLOWED_TRANSITIONS: dict[BuildStage, set[BuildStage]] = {
    BuildStage.queued: {BuildStage.preflight, BuildStage.rejected},
    BuildStage.preflight: {BuildStage.printing, BuildStage.rejected},
    BuildStage.printing: {BuildStage.cooldown, BuildStage.rejected},
    BuildStage.cooldown: {BuildStage.inspection, BuildStage.rejected},
    BuildStage.inspection: {BuildStage.qualified, BuildStage.rejected},
    BuildStage.qualified: set(),
    BuildStage.rejected: set(),
}


class InvalidTransition(ValueError):
    """Requested stage transition violates the qualification protocol."""


def transition(current: BuildStage, destination: BuildStage) -> BuildStage:
    if destination not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransition(f"transition from {current} to {destination} not allowed")
    return destination


def gate_status(build_id: str) -> list[dict[str, str]]:
    gates = (
        "powder_chemistry", "machine_calibration", "oxygen_control",
        "layer_imaging", "density_coupon", "surface_inspection",
        "metallography", "dimensional_inspection",
    )
    return [
        {
            "build_id": build_id,
            "code": code,
            "state": "pending" if index >= 4 else "passed",
            "evidence": "synthetic_demo_data",
        }
        for index, code in enumerate(gates)
    ]
