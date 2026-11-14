"""Deterministic numerical sanity checks for surrogate models."""
import pytest
from app.domain import powder_spreadability_index, process_fingerprint
from app.optimizer import optimize_parameters
from app.physics import estimate_melt_pool
from app.qualification import summarize_gates, REQUIRED_GATES
from app.risk import score_defects
from app.schemas import Observation, OptimizationRequest, BuildStage
from app.state_machine import transition, InvalidTransition


def test_energy_density_identity():
    observed = Observation()
    physics = estimate_melt_pool(observed)
    expected = observed.laser_power_w / (
        observed.scan_speed_mm_s * observed.hatch_spacing_mm
        * observed.layer_thickness_mm
    )
    assert physics.energy_density_j_mm3 == pytest.approx(expected, abs=0.0001)


def test_line_energy_is_power_over_speed():
    observation = Observation()
    result = estimate_melt_pool(observation)
    assert result.line_energy_j_mm == pytest.approx(0.25, abs=0.00001)


def test_risk_monotonic_with_high_oxygen():
    base = Observation(oxygen_ppm=80)
    polluted = Observation(oxygen_ppm=980)
    base_risk = score_defects(base, estimate_melt_pool(base)).overall_risk
    high_risk = score_defects(polluted, estimate_melt_pool(polluted)).overall_risk
    assert high_risk > base_risk


def test_reject_invalid_powder_size():
    with pytest.raises(ValueError):
        Observation(powder_d50_um=120, layer_thickness_mm=0.02)


def test_spreadability_requires_monotonic_distribution():
    with pytest.raises(ValueError):
        powder_spreadability_index(50, 32, 15)


def test_process_fingerprint_positive():
    material, line_energy, volumetric = process_fingerprint(Observation())
    assert material == "Ti6Al4V"
    assert line_energy > 0
    assert volumetric > line_energy


def test_optimizer_ranks_candidates():
    candidates = optimize_parameters(OptimizationRequest())
    assert candidates
    assert all(a.objective <= b.objective for a, b in zip(candidates, candidates[1:]))


def test_qualification_evidence_complete():
    passed = summarize_gates({gate: True for gate in REQUIRED_GATES})
    assert passed["accepted"] is True


def test_reject_unsafe_stage_jump():
    with pytest.raises(InvalidTransition):
        transition(BuildStage.queued, BuildStage.qualified)


def test_allow_linear_stage_transition():
    assert transition(BuildStage.preflight, BuildStage.printing) == BuildStage.printing
