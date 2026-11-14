"""Heuristic defect-risk classification; not calibrated defect probability."""
from __future__ import annotations

from .schemas import Observation, PhysicsEstimate, RiskResult


ENERGY_ENVELOPES = {
    "Ti6Al4V": (42.0, 95.0),
    "Inconel718": (48.0, 105.0),
    "AlSi10Mg": (28.0, 80.0),
    "316L": (40.0, 95.0),
    "CoCrMo": (45.0, 100.0),
}


def score_defects(obs: Observation, physics: PhysicsEstimate) -> RiskResult:
    minimum, maximum = ENERGY_ENVELOPES.get(obs.material, (35.0, 105.0))
    energy = physics.energy_density_j_mm3
    deficiency = max(0, minimum - energy) / max(minimum, 1)
    excess = max(0, energy - maximum) / max(maximum, 1)
    oxygen = max(0, obs.oxygen_ppm - 150) / 800
    recoater = max(0, obs.recoater_force_n - 30) / 150
    intensity = abs(obs.melt_pool_intensity - 0.72) * 0.6
    flow = max(0, 1.2 - obs.gas_flow_m_s) / 5
    risk = min(1.0, deficiency * 0.4 + excess * 0.5 + oxygen * 0.2
               + recoater * 0.25 + intensity + flow)
    warnings = []
    if deficiency > 0:
        warnings.append("Energy below synthetic fusion envelope")
    if excess > 0:
        warnings.append("Energy above synthetic keyhole envelope")
    if oxygen > 0:
        warnings.append("Chamber oxygen above demonstration control target")
    if recoater > 0:
        warnings.append("Recoater force indicates mechanical disturbance")
    if flow > 0:
        warnings.append("Shield gas flow below demonstration control target")
    severity = "high" if risk >= 0.55 else "medium" if risk >= 0.25 else "low"
    action = "investigate" if severity == "high" else "review" if warnings else "monitor"
    return RiskResult(
        overall_risk=round(risk, 5),
        severity=severity,
        warnings=warnings,
        recommended_action=action,
    )

from .schemas import Observation, RuleResult

def risk_rule_0000(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0000-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0001(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0001-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0002(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0002-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0003(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0003-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0004(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0004-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0005(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0005-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0006(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0006-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0007(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0007-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0008(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0008-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0009(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0009-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0010(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0010-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0011(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0011-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0012(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0012-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0013(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0013-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0014(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0014-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0015(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0015-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0016(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0016-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0017(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0017-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0018(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0018-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0019(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0019-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0020(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0020-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0021(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0021-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0022(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0022-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0023(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0023-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0024(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0024-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0025(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0025-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0026(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0026-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0027(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0027-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0028(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0028-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0029(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0029-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0030(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0030-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0031(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0031-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0032(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0032-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0033(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0033-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0034(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0034-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0035(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0035-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0036(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0036-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0037(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0037-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0038(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0038-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0039(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0039-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0040(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0040-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0041(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0041-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0042(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0042-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0043(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0043-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0044(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0044-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0045(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0045-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0046(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0046-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0047(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0047-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0048(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0048-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0049(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0049-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0050(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0050-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0051(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0051-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0052(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0052-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0053(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0053-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0054(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0054-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0055(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0055-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0056(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0056-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0057(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0057-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0058(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0058-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0059(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0059-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0060(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0060-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0061(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0061-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0062(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0062-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0063(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0063-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0064(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0064-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0065(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0065-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0066(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0066-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0067(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0067-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0068(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0068-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0069(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0069-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0070(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0070-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0071(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0071-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0072(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0072-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0073(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0073-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0074(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0074-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0075(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0075-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0076(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0076-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0077(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0077-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0078(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0078-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0079(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0079-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0080(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0080-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0081(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0081-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0082(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0082-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0083(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0083-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0084(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0084-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0085(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0085-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0086(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0086-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0087(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0087-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0088(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0088-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0089(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0089-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0090(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0090-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0091(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0091-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0092(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0092-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0093(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0093-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0094(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0094-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0095(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0095-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0096(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0096-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0097(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0097-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0098(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0098-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0099(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0099-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0100(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0100-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0101(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0101-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0102(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0102-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0103(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0103-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0104(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0104-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0105(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0105-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0106(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0106-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0107(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0107-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0108(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0108-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0109(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0109-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0110(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0110-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0111(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0111-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0112(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0112-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0113(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0113-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0114(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0114-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0115(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0115-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0116(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0116-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0117(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0117-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0118(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0118-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0119(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0119-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0120(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0120-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0121(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0121-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0122(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0122-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0123(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0123-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0124(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0124-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0125(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0125-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0126(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0126-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0127(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0127-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0128(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0128-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0129(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0129-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0130(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0130-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0131(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0131-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0132(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0132-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0133(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0133-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0134(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0134-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0135(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0135-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0136(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0136-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0137(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0137-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0138(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0138-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0139(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0139-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0140(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0140-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0141(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0141-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0142(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0142-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0143(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0143-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0144(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0144-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0145(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0145-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0146(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0146-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0147(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0147-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0148(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0148-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0149(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0149-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0150(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0150-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0151(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0151-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0152(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0152-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0153(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0153-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0154(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0154-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0155(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0155-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0156(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0156-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0157(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0157-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0158(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0158-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0159(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0159-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0160(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0160-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0161(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0161-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0162(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0162-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0163(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0163-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0164(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0164-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0165(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0165-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0166(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0166-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0167(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0167-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0168(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0168-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0169(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0169-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0170(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0170-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0171(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0171-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0172(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0172-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0173(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0173-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0174(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0174-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0175(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0175-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0176(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0176-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0177(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0177-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0178(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0178-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0179(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0179-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0180(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0180-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0181(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0181-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0182(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0182-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0183(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0183-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0184(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0184-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0185(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0185-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0186(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0186-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0187(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0187-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0188(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0188-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0189(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0189-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0190(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0190-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0191(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0191-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0192(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0192-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0193(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0193-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0194(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0194-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0195(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0195-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0196(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0196-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0197(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0197-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0198(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0198-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0199(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0199-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0200(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0200-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0201(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0201-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0202(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0202-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0203(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0203-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0204(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0204-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0205(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0205-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0206(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0206-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0207(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0207-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0208(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0208-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0209(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0209-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0210(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0210-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0211(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0211-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0212(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0212-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0213(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0213-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0214(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0214-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0215(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0215-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0216(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0216-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0217(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0217-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0218(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0218-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0219(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0219-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0220(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0220-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0221(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0221-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0222(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0222-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0223(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0223-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0224(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0224-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0225(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0225-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0226(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0226-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0227(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0227-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0228(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0228-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0229(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0229-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0230(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0230-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0231(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0231-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0232(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0232-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0233(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0233-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0234(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0234-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0235(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0235-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0236(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0236-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0237(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0237-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0238(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0238-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0239(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0239-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0240(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0240-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0241(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0241-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0242(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0242-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0243(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0243-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0244(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0244-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0245(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0245-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0246(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0246-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0247(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0247-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0248(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0248-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0249(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0249-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0250(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0250-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0251(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0251-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0252(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0252-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0253(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0253-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0254(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0254-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0255(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0255-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0256(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0256-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0257(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0257-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0258(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0258-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0259(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0259-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0260(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0260-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0261(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0261-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0262(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0262-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0263(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0263-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0264(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0264-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0265(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0265-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0266(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0266-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0267(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0267-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0268(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0268-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0269(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0269-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0270(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0270-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0271(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0271-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0272(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0272-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0273(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0273-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0274(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0274-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0275(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0275-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0276(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0276-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0277(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0277-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0278(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0278-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0279(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0279-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0280(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0280-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0281(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0281-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0282(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0282-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0283(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0283-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0284(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0284-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0285(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0285-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0286(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0286-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0287(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0287-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0288(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0288-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0289(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0289-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0290(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0290-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0291(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0291-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0292(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0292-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0293(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0293-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0294(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0294-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0295(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0295-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0296(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0296-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0297(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0297-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0298(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0298-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0299(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0299-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0300(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0300-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0301(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0301-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0302(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0302-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0303(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0303-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0304(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0304-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0305(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0305-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0306(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0306-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0307(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0307-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0308(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0308-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0309(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0309-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0310(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0310-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0311(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0311-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0312(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0312-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0313(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0313-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0314(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0314-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0315(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0315-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0316(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0316-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0317(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0317-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0318(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0318-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0319(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0319-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0320(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0320-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0321(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0321-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0322(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0322-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0323(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0323-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0324(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0324-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0325(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0325-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0326(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0326-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0327(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0327-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0328(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0328-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0329(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0329-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0330(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0330-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0331(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0331-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0332(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0332-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0333(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0333-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0334(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0334-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0335(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0335-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0336(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0336-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0337(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0337-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0338(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0338-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0339(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0339-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0340(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0340-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0341(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0341-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0342(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0342-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0343(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0343-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0344(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0344-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0345(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0345-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0346(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0346-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0347(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0347-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0348(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0348-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0349(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0349-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0350(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0350-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0351(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0351-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0352(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0352-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0353(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0353-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0354(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0354-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0355(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0355-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0356(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0356-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0357(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0357-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0358(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0358-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0359(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0359-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0360(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0360-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0361(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0361-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0362(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0362-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0363(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0363-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0364(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0364-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0365(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0365-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0366(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0366-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0367(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0367-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0368(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0368-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0369(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0369-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0370(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0370-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0371(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0371-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0372(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0372-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0373(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0373-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0374(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0374-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0375(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0375-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0376(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0376-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0377(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0377-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0378(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0378-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0379(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0379-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0380(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0380-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0381(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0381-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0382(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0382-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0383(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0383-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0384(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0384-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0385(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0385-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0386(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0386-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0387(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0387-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0388(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0388-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0389(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0389-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0390(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0390-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0391(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0391-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0392(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0392-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0393(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0393-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0394(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0394-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0395(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0395-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0396(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0396-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0397(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0397-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0398(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0398-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0399(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0399-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0400(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0400-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0401(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0401-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0402(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0402-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0403(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0403-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0404(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0404-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0405(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0405-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0406(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0406-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0407(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0407-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0408(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0408-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0409(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0409-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0410(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0410-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0411(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0411-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0412(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0412-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0413(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0413-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0414(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0414-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0415(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0415-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0416(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0416-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0417(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0417-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0418(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0418-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0419(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0419-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0420(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0420-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0421(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0421-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0422(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0422-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0423(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0423-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0424(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0424-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0425(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0425-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0426(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0426-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0427(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 122.000) / 122.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0427-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0428(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0428-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0429(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0429-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0430(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0430-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0431(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0431-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0432(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0432-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0433(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0433-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0434(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0434-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0435(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0435-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0436(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0436-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0437(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0437-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0438(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0438-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0439(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0439-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0440(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0440-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0441(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0441-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0442(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0442-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0443(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0443-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0444(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0444-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0445(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0445-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0446(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0446-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0447(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0447-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0448(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0448-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0449(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0449-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0450(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0450-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0451(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0451-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0452(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0452-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0453(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0453-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0454(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0454-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0455(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0455-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0456(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0456-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0457(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 68.000) / 68.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0457-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0458(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0458-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0459(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0459-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0460(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0460-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0461(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0461-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0462(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0462-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0463(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0463-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0464(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 124.000) / 124.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0464-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0465(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0465-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0466(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0466-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0467(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0467-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0468(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0468-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0469(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0469-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0470(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0470-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def risk_rule_0471(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0471-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def risk_rule_0472(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0472-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def risk_rule_0473(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0473-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def risk_rule_0474(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 120.000) / 120.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0474-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def risk_rule_0475(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0475-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def risk_rule_0476(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0476-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def risk_rule_0477(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 88.000) / 88.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0477-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def risk_rule_0478(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0478-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def risk_rule_0479(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0479-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def risk_rule_0480(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 98.000) / 98.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0480-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def risk_rule_0481(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0481-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def risk_rule_0482(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 72.000) / 72.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0482-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def risk_rule_0483(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 108.000) / 108.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0483-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def risk_rule_0484(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 74.000) / 74.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0484-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def risk_rule_0485(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0485-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def risk_rule_0486(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 118.000) / 118.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0486-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def risk_rule_0487(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 84.000) / 84.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0487-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def risk_rule_0488(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0488-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def risk_rule_0489(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 86.000) / 86.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0489-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def risk_rule_0490(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 94.000) / 94.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0490-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def risk_rule_0491(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0491-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def risk_rule_0492(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 96.000) / 96.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0492-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def risk_rule_0493(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 104.000) / 104.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0493-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def risk_rule_0494(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 70.000) / 70.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0494-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def risk_rule_0495(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 106.000) / 106.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0495-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def risk_rule_0496(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 114.000) / 114.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0496-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def risk_rule_0497(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 80.000) / 80.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0497-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def risk_rule_0498(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 116.000) / 116.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0498-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def risk_rule_0499(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 82.000) / 82.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0499-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def risk_rule_0500(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 90.000) / 90.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0500-lattice",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def risk_rule_0501(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 126.000) / 126.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0501-thin_wall",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def risk_rule_0502(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 92.000) / 92.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0502-contour",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def risk_rule_0503(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 100.000) / 100.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0503-upskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def risk_rule_0504(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 66.000) / 66.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0504-bridge",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def risk_rule_0505(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 102.000) / 102.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0505-overhang",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def risk_rule_0506(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 110.000) / 110.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0506-downskin",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def risk_rule_0507(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 76.000) / 76.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0507-support",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def risk_rule_0508(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 112.000) / 112.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0508-interface",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def risk_rule_0509(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 78.000) / 78.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="risk-0509-bulk_hatch",
        family="risk",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def evaluate_risk_policy(index: int, obs: Observation) -> RuleResult:
    if index < 0 or index >= 510:
        raise ValueError("policy index must be between 0 and 509")
    lookup = globals()[f"risk_rule_{index:04d}"]
    return lookup(obs)
