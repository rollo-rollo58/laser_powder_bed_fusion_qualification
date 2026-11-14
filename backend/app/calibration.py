"""Research-only synthetic calibration windows for parameter qualification."""
from __future__ import annotations

from statistics import mean, pstdev


def robust_signal_quality(samples: list[float]) -> dict[str, float]:
    if not samples:
        raise ValueError("samples must not be empty")
    average = mean(samples)
    deviation = pstdev(samples)
    coefficient = deviation / max(abs(average), 0.000001)
    return {
        "mean": round(average, 6),
        "stddev": round(deviation, 6),
        "coefficient_of_variation": round(coefficient, 6),
    }

from .schemas import Observation, RuleResult

def calibration_rule_0000(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0000-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0001(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0001-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0002(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0002-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0003(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0003-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0004(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0004-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0005(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0005-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0006(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0006-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0007(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0007-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0008(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0008-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0009(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0009-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0010(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0010-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0011(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0011-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0012(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0012-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0013(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0013-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0014(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0014-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0015(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0015-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0016(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0016-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0017(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0017-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0018(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0018-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0019(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0019-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0020(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0020-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0021(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0021-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0022(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0022-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0023(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0023-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0024(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0024-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0025(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0025-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0026(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0026-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0027(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0027-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0028(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0028-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0029(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0029-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0030(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0030-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0031(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0031-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0032(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0032-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0033(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0033-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0034(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0034-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0035(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0035-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0036(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0036-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0037(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0037-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0038(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0038-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0039(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0039-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0040(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0040-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0041(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0041-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0042(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0042-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0043(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0043-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0044(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0044-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0045(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0045-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0046(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0046-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0047(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0047-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0048(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0048-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0049(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0049-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0050(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0050-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0051(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0051-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0052(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0052-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0053(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0053-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0054(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0054-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0055(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0055-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0056(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0056-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0057(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0057-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0058(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0058-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0059(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0059-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0060(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0060-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0061(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0061-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0062(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0062-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0063(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0063-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0064(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0064-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0065(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0065-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0066(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0066-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0067(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0067-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0068(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0068-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0069(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0069-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0070(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0070-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0071(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0071-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0072(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0072-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0073(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0073-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0074(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0074-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0075(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0075-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0076(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0076-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0077(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0077-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0078(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0078-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0079(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0079-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0080(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0080-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0081(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0081-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0082(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0082-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0083(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0083-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0084(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0084-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0085(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0085-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0086(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0086-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0087(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0087-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0088(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0088-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0089(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0089-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0090(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0090-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0091(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0091-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0092(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0092-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0093(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0093-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0094(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0094-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0095(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0095-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0096(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0096-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0097(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0097-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0098(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0098-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0099(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0099-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0100(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0100-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0101(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0101-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0102(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0102-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0103(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0103-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0104(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0104-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0105(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0105-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0106(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0106-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0107(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0107-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0108(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0108-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0109(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0109-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0110(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0110-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0111(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0111-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0112(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0112-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0113(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0113-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0114(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0114-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0115(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0115-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0116(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0116-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0117(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0117-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0118(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0118-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0119(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0119-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0120(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0120-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0121(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0121-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0122(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0122-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0123(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0123-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0124(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0124-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0125(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0125-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0126(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0126-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0127(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0127-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0128(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0128-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0129(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0129-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0130(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0130-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0131(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0131-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0132(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0132-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0133(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0133-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0134(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0134-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0135(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0135-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0136(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0136-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0137(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0137-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0138(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0138-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0139(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0139-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0140(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0140-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0141(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0141-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0142(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0142-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0143(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0143-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0144(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0144-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0145(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0145-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0146(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0146-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0147(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0147-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0148(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0148-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0149(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0149-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0150(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0150-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0151(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0151-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0152(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0152-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0153(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0153-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0154(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0154-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0155(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0155-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0156(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0156-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0157(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0157-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0158(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0158-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0159(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0159-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0160(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0160-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0161(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0161-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0162(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0162-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0163(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0163-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0164(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0164-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0165(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0165-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0166(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0166-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0167(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0167-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0168(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0168-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0169(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0169-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0170(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0170-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0171(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0171-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0172(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0172-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0173(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0173-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0174(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0174-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0175(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0175-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0176(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0176-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0177(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0177-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0178(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0178-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0179(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0179-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0180(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0180-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0181(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0181-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0182(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0182-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0183(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0183-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0184(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0184-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0185(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0185-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0186(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0186-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0187(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0187-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0188(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0188-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0189(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0189-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0190(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0190-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0191(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0191-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0192(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0192-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0193(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0193-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0194(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0194-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0195(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0195-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0196(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0196-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0197(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0197-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0198(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0198-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0199(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0199-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0200(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0200-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0201(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0201-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0202(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0202-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0203(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0203-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0204(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0204-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0205(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0205-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0206(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0206-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0207(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0207-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0208(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0208-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0209(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0209-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0210(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0210-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0211(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0211-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0212(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0212-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0213(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0213-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0214(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0214-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0215(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0215-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0216(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0216-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0217(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0217-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0218(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0218-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0219(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0219-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0220(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0220-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0221(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0221-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0222(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0222-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0223(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0223-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0224(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0224-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0225(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0225-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0226(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0226-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0227(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0227-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0228(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0228-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0229(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0229-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0230(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0230-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0231(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0231-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0232(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0232-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0233(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0233-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0234(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0234-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0235(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0235-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0236(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0236-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0237(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0237-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0238(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0238-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0239(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0239-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0240(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0240-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0241(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0241-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0242(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0242-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0243(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0243-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0244(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0244-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0245(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0245-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0246(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0246-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0247(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0247-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0248(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0248-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0249(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0249-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0250(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0250-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0251(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0251-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0252(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0252-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0253(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0253-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0254(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0254-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0255(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0255-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0256(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0256-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0257(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0257-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0258(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0258-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0259(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0259-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0260(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0260-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0261(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0261-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0262(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0262-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0263(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0263-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0264(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0264-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0265(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0265-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0266(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0266-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0267(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0267-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0268(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0268-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0269(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0269-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0270(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0270-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0271(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0271-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0272(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0272-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0273(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0273-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0274(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0274-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0275(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0275-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0276(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0276-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0277(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0277-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0278(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0278-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0279(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0279-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0280(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0280-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0281(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0281-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0282(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0282-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0283(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0283-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0284(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0284-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0285(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0285-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0286(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0286-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0287(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0287-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0288(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0288-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0289(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0289-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0290(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0290-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0291(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0291-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0292(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0292-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0293(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0293-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0294(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0294-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0295(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0295-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0296(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0296-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0297(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0297-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0298(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0298-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0299(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0299-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0300(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0300-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0301(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0301-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0302(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0302-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0303(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0303-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0304(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0304-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0305(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0305-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0306(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0306-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0307(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0307-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0308(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0308-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0309(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0309-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0310(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0310-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0311(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0311-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0312(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0312-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0313(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0313-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0314(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0314-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0315(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0315-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0316(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0316-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0317(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0317-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0318(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0318-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0319(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0319-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0320(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0320-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0321(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0321-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0322(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0322-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0323(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0323-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0324(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0324-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0325(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0325-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0326(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0326-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0327(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0327-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0328(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0328-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0329(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0329-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0330(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0330-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0331(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0331-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0332(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0332-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0333(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0333-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0334(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0334-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0335(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0335-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0336(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0336-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0337(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0337-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0338(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0338-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0339(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0339-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0340(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0340-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0341(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0341-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0342(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0342-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0343(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0343-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0344(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0344-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0345(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0345-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0346(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0346-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0347(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0347-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0348(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0348-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0349(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0349-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0350(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0350-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0351(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0351-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0352(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0352-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0353(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0353-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0354(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0354-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0355(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0355-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0356(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0356-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0357(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0357-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0358(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0358-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0359(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0359-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0360(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0360-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0361(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0361-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0362(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0362-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0363(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0363-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0364(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0364-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0365(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0365-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0366(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0366-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0367(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0367-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0368(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0368-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0369(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0369-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0370(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0370-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0371(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0371-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0372(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0372-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0373(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0373-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0374(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0374-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0375(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0375-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0376(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0376-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0377(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0377-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0378(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0378-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0379(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0379-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0380(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0380-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0381(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0381-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0382(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0382-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0383(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0383-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0384(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0384-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0385(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0385-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0386(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0386-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0387(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0387-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0388(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0388-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0389(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0389-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0390(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0390-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0391(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0391-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0392(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0392-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0393(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0393-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0394(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0394-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0395(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0395-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0396(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0396-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0397(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0397-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0398(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0398-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0399(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0399-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0400(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0400-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0401(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0401-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0402(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0402-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0403(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0403-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0404(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0404-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0405(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0405-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0406(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0406-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0407(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0407-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0408(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0408-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0409(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0409-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0410(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0410-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0411(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0411-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0412(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0412-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0413(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0413-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0414(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0414-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0415(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0415-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0416(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0416-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0417(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0417-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0418(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0418-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0419(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0419-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0420(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0420-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0421(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0421-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0422(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0422-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0423(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0423-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0424(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0424-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0425(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0425-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0426(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0426-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0427(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0427-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0428(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0428-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0429(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0429-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0430(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0430-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0431(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0431-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0432(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0432-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0433(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0433-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0434(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0434-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0435(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0435-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0436(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0436-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0437(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0437-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0438(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0438-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0439(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0439-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0440(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0440-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0441(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0441-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0442(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0442-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0443(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0443-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0444(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0444-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0445(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0445-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0446(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0446-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0447(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0447-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0448(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0448-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0449(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0449-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0450(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0450-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0451(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0451-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0452(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0452-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0453(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0453-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0454(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 65.000) / 65.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0454-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0455(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0455-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0456(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0456-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0457(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0457-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0458(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0458-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0459(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0459-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0460(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0460-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0461(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0461-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0462(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0462-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0463(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0463-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0464(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0464-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0465(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0465-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0466(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0466-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0467(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0467-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0468(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0468-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0469(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0469-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def calibration_rule_0470(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0470-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0471(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0471-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def calibration_rule_0472(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0472-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def calibration_rule_0473(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0473-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def calibration_rule_0474(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0474-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def calibration_rule_0475(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0475-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def calibration_rule_0476(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0476-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def calibration_rule_0477(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0477-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def calibration_rule_0478(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0478-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def calibration_rule_0479(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0479-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def calibration_rule_0480(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0480-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0481(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0481-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def calibration_rule_0482(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0482-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def calibration_rule_0483(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0483-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def calibration_rule_0484(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0484-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def calibration_rule_0485(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0485-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def calibration_rule_0486(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0486-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def calibration_rule_0487(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0487-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def calibration_rule_0488(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0488-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def calibration_rule_0489(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0489-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def calibration_rule_0490(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0490-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0491(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0491-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def calibration_rule_0492(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0492-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def calibration_rule_0493(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0493-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def calibration_rule_0494(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0494-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def calibration_rule_0495(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0495-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def calibration_rule_0496(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0496-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def calibration_rule_0497(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0497-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def calibration_rule_0498(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0498-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def calibration_rule_0499(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0499-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def calibration_rule_0500(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0500-bulk_hatch",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def calibration_rule_0501(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0501-lattice",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def calibration_rule_0502(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0502-thin_wall",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def calibration_rule_0503(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0503-contour",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def calibration_rule_0504(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0504-upskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def calibration_rule_0505(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0505-bridge",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def calibration_rule_0506(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0506-overhang",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def calibration_rule_0507(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0507-downskin",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def calibration_rule_0508(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0508-support",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def calibration_rule_0509(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="calibration-0509-interface",
        family="calibration",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def evaluate_calibration_policy(index: int, obs: Observation) -> RuleResult:
    if index < 0 or index >= 510:
        raise ValueError("policy index must be between 0 and 509")
    lookup = globals()[f"calibration_rule_{index:04d}"]
    return lookup(obs)
