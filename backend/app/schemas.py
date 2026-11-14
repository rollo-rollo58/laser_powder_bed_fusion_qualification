"""Validated request and response contracts for manufacturing research."""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, model_validator


class BuildStage(str, Enum):
    queued = "queued"
    preflight = "preflight"
    printing = "printing"
    cooldown = "cooldown"
    inspection = "inspection"
    qualified = "qualified"
    rejected = "rejected"


class Observation(BaseModel):
    material: str = Field(default="Ti6Al4V", min_length=2, max_length=48)
    layer_number: int = Field(default=1, ge=1, le=50000)
    laser_power_w: float = Field(default=275, gt=20, le=1200)
    scan_speed_mm_s: float = Field(default=1100, gt=10, le=5000)
    hatch_spacing_mm: float = Field(default=0.105, gt=0.01, le=0.5)
    layer_thickness_mm: float = Field(default=0.04, gt=0.01, le=0.2)
    oxygen_ppm: float = Field(default=95, ge=0, le=10000)
    chamber_temp_c: float = Field(default=38, ge=-20, le=350)
    melt_pool_intensity: float = Field(default=0.72, ge=0, le=1)
    recoater_force_n: float = Field(default=13, ge=0, le=500)
    gas_flow_m_s: float = Field(default=2.4, ge=0, le=25)
    powder_d50_um: float = Field(default=33, gt=0, le=150)
    scan_rotation_deg: float = Field(default=67, ge=0, lt=360)

    @model_validator(mode="after")
    def validate_physical_window(self) -> "Observation":
        if self.powder_d50_um / 1000 > 2.5 * self.layer_thickness_mm:
            raise ValueError("powder D50 exceeds supported layer envelope")
        return self


class PhysicsEstimate(BaseModel):
    energy_density_j_mm3: float
    line_energy_j_mm: float
    melt_pool_width_um: float
    melt_pool_depth_um: float
    cooling_rate_k_s: float
    thermal_gradient_k_mm: float


class RuleResult(BaseModel):
    rule_id: str
    family: str
    score: float = Field(ge=0, le=1)
    accepted: bool
    action: str
    rationale: str


class RiskResult(BaseModel):
    overall_risk: float = Field(ge=0, le=1)
    severity: str
    warnings: list[str]
    recommended_action: str


class EvaluationResponse(BaseModel):
    observation: Observation
    physics: PhysicsEstimate
    risk: RiskResult
    evaluated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class OptimizationRequest(BaseModel):
    material: str = "Ti6Al4V"
    target_energy_j_mm3: float = Field(default=62, gt=0, le=250)
    max_risk: float = Field(default=0.35, ge=0, le=1)
    powder_d50_um: float = Field(default=33, gt=0, le=150)


class OptimizationCandidate(BaseModel):
    laser_power_w: float
    scan_speed_mm_s: float
    hatch_spacing_mm: float
    layer_thickness_mm: float
    predicted_energy_j_mm3: float
    objective: float


class BuildRecord(BaseModel):
    id: str
    machine_id: str
    material: str
    layer_count: int
    status: BuildStage
    completed_layers: int = 0
