"""Idempotent study batch processor for offline simulation experiments."""
from __future__ import annotations

from .physics import estimate_melt_pool
from .risk import score_defects
from .schemas import Observation


def evaluate_batch(observations: list[Observation]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for observation in observations:
        physics = estimate_melt_pool(observation)
        risk = score_defects(observation, physics)
        result.append({
            "layer": observation.layer_number,
            "energy_density": physics.energy_density_j_mm3,
            "risk": risk.overall_risk,
            "severity": risk.severity,
        })
    return result

from .schemas import Observation, RuleResult

def worker_rule_0000(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 100.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0000-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0001(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 113.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0001-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0002(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 126.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0002-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0003(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 139.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0003-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0004(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 152.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0004-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0005(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 165.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0005-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0006(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 178.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0006-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0007(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 191.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0007-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0008(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 204.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0008-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0009(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 217.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0009-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0010(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 230.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0010-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0011(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 243.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0011-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0012(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 256.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0012-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0013(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 269.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0013-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0014(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 112.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0014-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0015(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 125.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0015-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0016(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 138.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0016-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0017(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 151.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0017-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0018(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 164.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0018-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0019(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 177.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0019-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0020(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 190.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0020-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0021(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 203.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0021-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0022(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 216.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0022-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0023(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 229.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0023-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0024(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 242.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0024-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0025(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 255.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0025-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0026(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 268.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0026-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0027(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 111.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0027-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0028(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 124.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0028-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0029(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 137.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0029-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0030(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 150.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0030-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0031(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 163.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0031-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0032(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 176.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0032-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0033(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 189.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0033-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0034(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 202.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0034-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0035(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 215.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0035-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0036(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 228.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0036-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0037(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 241.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0037-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0038(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 254.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0038-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0039(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 267.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0039-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0040(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 110.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0040-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0041(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 123.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0041-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0042(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 136.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0042-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0043(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 149.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0043-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0044(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 162.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0044-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0045(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 175.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0045-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0046(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 188.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0046-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0047(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 201.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0047-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0048(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 214.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0048-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0049(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 227.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0049-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0050(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 240.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0050-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0051(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 253.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0051-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0052(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 266.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0052-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0053(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 109.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0053-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0054(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 122.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0054-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0055(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 135.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0055-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0056(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 148.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0056-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0057(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 161.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0057-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0058(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 174.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0058-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0059(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 187.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0059-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0060(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 200.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0060-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0061(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 213.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0061-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0062(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 226.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0062-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0063(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 239.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0063-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0064(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 252.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0064-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0065(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 265.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0065-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0066(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 108.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0066-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0067(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 121.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0067-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0068(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 134.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0068-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0069(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 147.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0069-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0070(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 160.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0070-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0071(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 173.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0071-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0072(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 186.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0072-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0073(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 199.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0073-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0074(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 212.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0074-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0075(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 225.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0075-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0076(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 238.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0076-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0077(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 251.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0077-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0078(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 264.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0078-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0079(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 107.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0079-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0080(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 120.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0080-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0081(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 133.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0081-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0082(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 146.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0082-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0083(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 159.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0083-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0084(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 172.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0084-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0085(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 185.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0085-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0086(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 198.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0086-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0087(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 211.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0087-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0088(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 224.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0088-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0089(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 237.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0089-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0090(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 250.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0090-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0091(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 263.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0091-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0092(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 106.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0092-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0093(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 119.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0093-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0094(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 132.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0094-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0095(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 145.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0095-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0096(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 158.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0096-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0097(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 171.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0097-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0098(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 184.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0098-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0099(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 197.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0099-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0100(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 210.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0100-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0101(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 223.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0101-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0102(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 236.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0102-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0103(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 249.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0103-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0104(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 262.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0104-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0105(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 105.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0105-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0106(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 118.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0106-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0107(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 131.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0107-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0108(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 144.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0108-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0109(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 157.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0109-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0110(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 170.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0110-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0111(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 183.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0111-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0112(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 196.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0112-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0113(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 209.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0113-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0114(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 222.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0114-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0115(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 235.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0115-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0116(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 248.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0116-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0117(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 261.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0117-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0118(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 104.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0118-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0119(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 117.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0119-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0120(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 130.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0120-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0121(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 143.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0121-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0122(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 156.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0122-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0123(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 169.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0123-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0124(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 182.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0124-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0125(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 195.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0125-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0126(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 208.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0126-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0127(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 221.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0127-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0128(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 234.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0128-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0129(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 247.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0129-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0130(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 260.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0130-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0131(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 103.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0131-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0132(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 116.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0132-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0133(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 129.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0133-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0134(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 142.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0134-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0135(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 155.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0135-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0136(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 168.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0136-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0137(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 181.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0137-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0138(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 194.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0138-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0139(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 207.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0139-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0140(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 220.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0140-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0141(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 233.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0141-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0142(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 246.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0142-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0143(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 259.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0143-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0144(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 102.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0144-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0145(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 115.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0145-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0146(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 128.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0146-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0147(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 141.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0147-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0148(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 154.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0148-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0149(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 167.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0149-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0150(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 180.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0150-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0151(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 193.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0151-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0152(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 206.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0152-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0153(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 219.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0153-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0154(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 232.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0154-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0155(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 245.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0155-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0156(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 258.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0156-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0157(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 101.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0157-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0158(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 114.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0158-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0159(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 127.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0159-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0160(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 140.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0160-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0161(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 153.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0161-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0162(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 166.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0162-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0163(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 179.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0163-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0164(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 192.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0164-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0165(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 205.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0165-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0166(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 218.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0166-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0167(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 231.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0167-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0168(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 244.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0168-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0169(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 257.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0169-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0170(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 100.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0170-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0171(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 113.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0171-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0172(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 126.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0172-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0173(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 139.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0173-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0174(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 152.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0174-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0175(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 165.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0175-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0176(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 178.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0176-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0177(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 191.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0177-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0178(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 204.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0178-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0179(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 217.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0179-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0180(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 230.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0180-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0181(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 243.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0181-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0182(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 256.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0182-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0183(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 269.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0183-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0184(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 112.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0184-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0185(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 125.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0185-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0186(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 138.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0186-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0187(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 151.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0187-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0188(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 164.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0188-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0189(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 177.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0189-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0190(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 190.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0190-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0191(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 203.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0191-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0192(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 216.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0192-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0193(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 229.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0193-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0194(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 242.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0194-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0195(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 255.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0195-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0196(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 268.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0196-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0197(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 111.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0197-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0198(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 124.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0198-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0199(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 137.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0199-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0200(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 150.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0200-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0201(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 163.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0201-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0202(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 176.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0202-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0203(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 189.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0203-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0204(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 202.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0204-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0205(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 215.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0205-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0206(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 228.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0206-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0207(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 241.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0207-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0208(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 254.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0208-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0209(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 267.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0209-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0210(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 110.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0210-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0211(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 123.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0211-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0212(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 136.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0212-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0213(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 149.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0213-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0214(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 162.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0214-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0215(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 175.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0215-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0216(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 188.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0216-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0217(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 201.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0217-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0218(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 214.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0218-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0219(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 227.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0219-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0220(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 240.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0220-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0221(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 253.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0221-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0222(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 266.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0222-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0223(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 109.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0223-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0224(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 122.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0224-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0225(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 135.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0225-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0226(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 148.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0226-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0227(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 161.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0227-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0228(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 174.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0228-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0229(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 187.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0229-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0230(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 200.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0230-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0231(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 213.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0231-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0232(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 226.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0232-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0233(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 239.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0233-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0234(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 252.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0234-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0235(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 265.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0235-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0236(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 108.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0236-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0237(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 121.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0237-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0238(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 134.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0238-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0239(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 147.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0239-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0240(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 160.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0240-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0241(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 173.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0241-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0242(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 186.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0242-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0243(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 199.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0243-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0244(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 212.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0244-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0245(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 225.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0245-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0246(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 238.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0246-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0247(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 251.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0247-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0248(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 264.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0248-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0249(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 107.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0249-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0250(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 120.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0250-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0251(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 133.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0251-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0252(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 146.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0252-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0253(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 159.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0253-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0254(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 172.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0254-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0255(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 185.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0255-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0256(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 198.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0256-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0257(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 211.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0257-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0258(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 224.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0258-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0259(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 237.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0259-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0260(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 250.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0260-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0261(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 263.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0261-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0262(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 106.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0262-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0263(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 119.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0263-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0264(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 132.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0264-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0265(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 145.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0265-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0266(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 158.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0266-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0267(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 171.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0267-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0268(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 184.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0268-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0269(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 197.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0269-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0270(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 210.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0270-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0271(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 223.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0271-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0272(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 236.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0272-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0273(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 249.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0273-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0274(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 262.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0274-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0275(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 105.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0275-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0276(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 118.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0276-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0277(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 131.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0277-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0278(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 144.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0278-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0279(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 157.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0279-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0280(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 170.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0280-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0281(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 183.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0281-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0282(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 196.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0282-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0283(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 209.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0283-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0284(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 222.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0284-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0285(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 235.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0285-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0286(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 248.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0286-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0287(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 261.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0287-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0288(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 104.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0288-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0289(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 117.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0289-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0290(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 130.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0290-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0291(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 143.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0291-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0292(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 156.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0292-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0293(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 169.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0293-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0294(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 182.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0294-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0295(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 195.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0295-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0296(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 208.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0296-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0297(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 221.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0297-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0298(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 234.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0298-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0299(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 247.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0299-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0300(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 260.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0300-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0301(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 103.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0301-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0302(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 116.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0302-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0303(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 129.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0303-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0304(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 142.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0304-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0305(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 155.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0305-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0306(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 168.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0306-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0307(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 181.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0307-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0308(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 194.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0308-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0309(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 207.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0309-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0310(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 220.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0310-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0311(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 233.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0311-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0312(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 246.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0312-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0313(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 259.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0313-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0314(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 102.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0314-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0315(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 115.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0315-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0316(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 128.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0316-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0317(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 141.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0317-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0318(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 154.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0318-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0319(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 167.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0319-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0320(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 180.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0320-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0321(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 193.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0321-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0322(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 206.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0322-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0323(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 219.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0323-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0324(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 232.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0324-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0325(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 245.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0325-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0326(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 258.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0326-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0327(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 101.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0327-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0328(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 114.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0328-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0329(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 127.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0329-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0330(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 140.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0330-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0331(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 153.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0331-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0332(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 166.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0332-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0333(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 179.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0333-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0334(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 192.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0334-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0335(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 205.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0335-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0336(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 218.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0336-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0337(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 231.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0337-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0338(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 244.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0338-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0339(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 257.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0339-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0340(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 100.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0340-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0341(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 113.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0341-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0342(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 126.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0342-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0343(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 139.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0343-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0344(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 152.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0344-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0345(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 165.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0345-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0346(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 178.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0346-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0347(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 191.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0347-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0348(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 204.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0348-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0349(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 217.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0349-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0350(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 230.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0350-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0351(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 243.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0351-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0352(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 256.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0352-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0353(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 269.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0353-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0354(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 112.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0354-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0355(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 125.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0355-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0356(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 138.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0356-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0357(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 151.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0357-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0358(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 164.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0358-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0359(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 177.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0359-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0360(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 190.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0360-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0361(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 203.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0361-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0362(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 216.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0362-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0363(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 229.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0363-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0364(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 242.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0364-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0365(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 255.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0365-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0366(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 268.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0366-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0367(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 111.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0367-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0368(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 124.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0368-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0369(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 137.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0369-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0370(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 150.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0370-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0371(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 163.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0371-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0372(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 176.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0372-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0373(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 189.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0373-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0374(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 202.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0374-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0375(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 215.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0375-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0376(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 228.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0376-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0377(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 241.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0377-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0378(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 254.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0378-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0379(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 267.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0379-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0380(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 110.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0380-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0381(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 123.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0381-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0382(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 136.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0382-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0383(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 149.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0383-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0384(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 162.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0384-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0385(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 175.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0385-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0386(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 188.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0386-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0387(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 201.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0387-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0388(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 214.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0388-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0389(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 227.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0389-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0390(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 240.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0390-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0391(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 253.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0391-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0392(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 266.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0392-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0393(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 109.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0393-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0394(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 122.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0394-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0395(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 135.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0395-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0396(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 148.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0396-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0397(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 161.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0397-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0398(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 174.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0398-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0399(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 187.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0399-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0400(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 200.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0400-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0401(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 213.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0401-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0402(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 226.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0402-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0403(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 239.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0403-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0404(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 252.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0404-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0405(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 265.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0405-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0406(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 108.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0406-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0407(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 121.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0407-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0408(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 134.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0408-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0409(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 147.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0409-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0410(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 160.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0410-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0411(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 173.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0411-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0412(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 186.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0412-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0413(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 199.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0413-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0414(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 212.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0414-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0415(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 225.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0415-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0416(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 238.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0416-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0417(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 251.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0417-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0418(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 264.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0418-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0419(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 107.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0419-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0420(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 120.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0420-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0421(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 133.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0421-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0422(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 146.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0422-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0423(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 159.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0423-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0424(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 172.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0424-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0425(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 185.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0425-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0426(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 198.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0426-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0427(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 211.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0427-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0428(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 224.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0428-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0429(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 237.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0429-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0430(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 250.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0430-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0431(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 263.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0431-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0432(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 106.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0432-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0433(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 119.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0433-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0434(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 132.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0434-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0435(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 145.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0435-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0436(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 158.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0436-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0437(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 171.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0437-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0438(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 184.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0438-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0439(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 197.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0439-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0440(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 210.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0440-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0441(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 223.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0441-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0442(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 236.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0442-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0443(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 249.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0443-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0444(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 262.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0444-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0445(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 105.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0445-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0446(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 118.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0446-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0447(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 131.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0447-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0448(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 144.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0448-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0449(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 157.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0449-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0450(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 170.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0450-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0451(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 183.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0451-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0452(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 196.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0452-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0453(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 209.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0453-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0454(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 222.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0454-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0455(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 235.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0455-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0456(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 248.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0456-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0457(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 261.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0457-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0458(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 104.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0458-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0459(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 117.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0459-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0460(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 130.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0460-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0461(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 143.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0461-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0462(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 156.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0462-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0463(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 169.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0463-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0464(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 182.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0464-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0465(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 195.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0465-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0466(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 208.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0466-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0467(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 221.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0467-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0468(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 234.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0468-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0469(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 247.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0469-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def worker_rule_0470(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 260.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0470-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def worker_rule_0471(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 103.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0471-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def worker_rule_0472(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 116.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 54.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0472-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def worker_rule_0473(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 129.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 23.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0473-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def worker_rule_0474(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 142.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 30.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0474-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def worker_rule_0475(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 155.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 37.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0475-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def worker_rule_0476(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 168.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 44.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0476-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def worker_rule_0477(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 181.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 51.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0477-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def worker_rule_0478(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 194.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 20.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0478-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def worker_rule_0479(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 64.000) / 64.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 207.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 27.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0479-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def worker_rule_0480(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 220.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 34.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0480-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def worker_rule_0481(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 233.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 41.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0481-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def worker_rule_0482(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 246.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 48.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0482-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def worker_rule_0483(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 259.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 55.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0483-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def worker_rule_0484(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 102.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 24.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0484-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def worker_rule_0485(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 115.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 31.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0485-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0486(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 128.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 38.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0486-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def worker_rule_0487(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 141.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 45.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0487-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def worker_rule_0488(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 154.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 52.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0488-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def worker_rule_0489(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 167.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 21.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0489-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def worker_rule_0490(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 180.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 28.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0490-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def worker_rule_0491(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 193.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 35.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0491-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def worker_rule_0492(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 206.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 42.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0492-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def worker_rule_0493(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 219.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 49.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0493-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def worker_rule_0494(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 232.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 18.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.790)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0494-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def worker_rule_0495(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 245.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 25.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.805)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0495-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def worker_rule_0496(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 258.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 32.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.580)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0496-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def worker_rule_0497(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 101.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 39.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.595)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0630
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0497-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def worker_rule_0498(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 114.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 46.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.610)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0690
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0498-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def worker_rule_0499(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 127.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 53.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.625)
    porosity_proxy = low_energy_excursion * 0.2320
    keyhole_proxy = high_energy_excursion * 0.0750
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0499-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def worker_rule_0500(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 140.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 22.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.640)
    porosity_proxy = low_energy_excursion * 0.2550
    keyhole_proxy = high_energy_excursion * 0.0810
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0500-bridge",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def worker_rule_0501(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 128.000) / 128.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 153.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 29.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.655)
    porosity_proxy = low_energy_excursion * 0.2780
    keyhole_proxy = high_energy_excursion * 0.0870
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0501-overhang",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def worker_rule_0502(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 166.000) / 1100.0
    gas_excursion = max(0.0, 1.900 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 36.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.670)
    porosity_proxy = low_energy_excursion * 0.3010
    keyhole_proxy = high_energy_excursion * 0.0930
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0502-downskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def worker_rule_0503(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 179.000) / 1100.0
    gas_excursion = max(0.0, 2.050 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 43.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.685)
    porosity_proxy = low_energy_excursion * 0.3240
    keyhole_proxy = high_energy_excursion * 0.0990
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0503-support",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def worker_rule_0504(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 192.000) / 1100.0
    gas_excursion = max(0.0, 1.000 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 50.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.700)
    porosity_proxy = low_energy_excursion * 0.3470
    keyhole_proxy = high_energy_excursion * 0.1050
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0504-interface",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def worker_rule_0505(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 205.000) / 1100.0
    gas_excursion = max(0.0, 1.150 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 19.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.715)
    porosity_proxy = low_energy_excursion * 0.3700
    keyhole_proxy = high_energy_excursion * 0.1110
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0505-bulk_hatch",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def worker_rule_0506(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 218.000) / 1100.0
    gas_excursion = max(0.0, 1.300 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 26.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.730)
    porosity_proxy = low_energy_excursion * 0.1400
    keyhole_proxy = high_energy_excursion * 0.1170
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0506-lattice",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def worker_rule_0507(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 231.000) / 1100.0
    gas_excursion = max(0.0, 1.450 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 33.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.745)
    porosity_proxy = low_energy_excursion * 0.1630
    keyhole_proxy = high_energy_excursion * 0.0450
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0507-thin_wall",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def worker_rule_0508(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 244.000) / 1100.0
    gas_excursion = max(0.0, 1.600 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 40.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.760)
    porosity_proxy = low_energy_excursion * 0.1860
    keyhole_proxy = high_energy_excursion * 0.0510
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0508-contour",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def worker_rule_0509(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
    oxygen_excursion = max(0.0, obs.oxygen_ppm - 257.000) / 1100.0
    gas_excursion = max(0.0, 1.750 - obs.gas_flow_m_s) / 8.0
    recoater_excursion = max(0.0, obs.recoater_force_n - 47.000) / 170.0
    pool_excursion = abs(obs.melt_pool_intensity - 0.775)
    porosity_proxy = low_energy_excursion * 0.2090
    keyhole_proxy = high_energy_excursion * 0.0570
    gas_quality = oxygen_excursion * 0.23 + gas_excursion * 0.18
    mechanical_quality = recoater_excursion * 0.22 + pool_excursion * 0.11
    risk = min(1.0, max(0.0, porosity_proxy + keyhole_proxy
                        + gas_quality + mechanical_quality))
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="worker-0509-upskin",
        family="worker",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def evaluate_worker_policy(index: int, obs: Observation) -> RuleResult:
    if index < 0 or index >= 510:
        raise ValueError("policy index must be between 0 and 509")
    lookup = globals()[f"worker_rule_{index:04d}"]
    return lookup(obs)
