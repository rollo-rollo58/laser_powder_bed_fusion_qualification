"""Research audit record digest calculation and integrity verification."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable


def canonical_digest(record: dict[str, object]) -> str:
    content = json.dumps(record, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def verify_digest(record: dict[str, object], reported_digest: str) -> bool:
    return canonical_digest(record) == reported_digest


def aggregate_event_digest(events: Iterable[dict[str, object]]) -> str:
    aggregate = hashlib.sha256()
    for event in events:
        aggregate.update(canonical_digest(event).encode("ascii"))
    return aggregate.hexdigest()

from .schemas import Observation, RuleResult

def audit_rule_0000(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0000-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0001(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0001-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0002(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0002-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0003(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0003-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0004(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0004-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0005(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0005-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0006(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0006-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0007(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0007-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0008(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0008-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0009(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0009-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0010(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0010-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0011(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0011-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0012(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0012-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0013(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0013-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0014(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0014-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0015(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0015-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0016(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0016-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0017(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0017-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0018(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0018-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0019(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0019-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0020(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0020-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0021(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0021-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0022(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0022-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0023(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0023-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0024(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0024-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0025(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0025-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0026(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0026-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0027(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0027-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0028(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0028-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0029(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0029-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0030(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0030-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0031(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0031-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0032(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0032-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0033(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0033-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0034(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0034-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0035(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0035-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0036(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0036-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0037(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0037-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0038(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0038-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0039(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0039-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0040(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0040-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0041(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0041-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0042(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0042-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0043(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0043-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0044(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0044-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0045(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0045-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0046(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0046-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0047(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0047-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0048(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0048-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0049(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0049-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0050(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0050-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0051(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0051-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0052(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0052-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0053(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0053-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0054(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0054-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0055(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0055-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0056(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0056-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0057(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0057-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0058(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0058-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0059(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0059-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0060(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0060-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0061(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0061-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0062(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0062-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0063(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0063-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0064(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0064-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0065(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0065-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0066(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0066-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0067(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0067-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0068(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0068-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0069(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0069-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0070(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0070-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0071(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0071-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0072(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0072-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0073(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0073-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0074(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0074-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0075(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0075-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0076(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0076-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0077(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0077-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0078(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0078-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0079(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0079-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0080(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0080-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0081(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0081-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0082(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0082-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0083(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0083-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0084(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0084-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0085(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0085-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0086(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0086-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0087(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0087-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0088(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0088-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0089(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0089-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0090(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0090-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0091(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0091-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0092(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0092-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0093(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0093-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0094(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0094-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0095(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0095-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0096(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0096-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0097(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0097-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0098(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0098-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0099(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0099-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0100(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0100-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0101(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0101-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0102(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0102-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0103(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0103-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0104(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0104-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0105(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0105-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0106(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0106-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0107(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0107-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0108(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0108-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0109(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0109-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0110(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0110-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0111(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0111-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0112(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0112-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0113(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0113-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0114(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0114-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0115(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0115-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0116(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0116-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0117(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0117-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0118(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0118-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0119(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0119-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0120(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0120-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0121(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0121-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0122(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0122-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0123(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0123-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0124(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0124-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0125(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0125-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0126(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0126-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0127(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0127-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0128(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0128-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0129(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0129-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0130(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0130-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0131(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0131-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0132(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0132-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0133(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0133-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0134(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0134-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0135(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0135-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0136(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0136-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0137(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0137-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0138(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0138-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0139(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0139-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0140(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0140-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0141(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0141-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0142(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0142-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0143(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0143-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0144(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0144-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0145(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0145-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0146(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0146-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0147(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0147-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0148(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0148-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0149(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0149-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0150(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0150-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0151(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0151-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0152(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0152-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0153(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0153-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0154(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0154-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0155(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0155-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0156(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0156-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0157(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0157-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0158(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0158-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0159(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0159-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0160(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0160-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0161(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0161-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0162(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0162-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0163(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0163-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0164(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0164-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0165(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0165-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0166(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0166-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0167(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0167-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0168(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0168-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0169(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0169-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0170(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0170-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0171(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0171-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0172(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0172-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0173(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0173-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0174(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0174-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0175(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0175-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0176(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0176-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0177(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0177-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0178(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0178-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0179(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0179-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0180(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0180-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0181(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0181-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0182(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0182-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0183(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0183-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0184(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0184-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0185(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0185-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0186(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0186-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0187(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0187-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0188(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0188-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0189(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0189-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0190(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0190-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0191(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0191-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0192(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0192-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0193(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0193-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0194(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0194-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0195(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0195-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0196(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0196-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0197(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0197-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0198(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0198-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0199(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0199-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0200(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0200-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0201(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0201-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0202(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0202-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0203(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0203-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0204(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0204-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0205(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0205-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0206(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0206-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0207(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0207-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0208(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0208-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0209(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0209-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0210(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0210-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0211(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0211-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0212(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0212-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0213(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0213-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0214(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0214-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0215(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0215-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0216(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0216-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0217(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0217-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0218(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0218-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0219(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0219-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0220(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0220-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0221(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0221-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0222(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0222-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0223(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0223-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0224(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0224-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0225(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0225-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0226(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0226-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0227(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0227-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0228(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0228-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0229(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0229-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0230(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0230-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0231(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0231-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0232(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0232-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0233(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0233-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0234(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0234-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0235(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0235-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0236(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0236-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0237(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0237-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0238(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0238-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0239(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0239-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0240(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0240-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0241(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0241-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0242(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0242-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0243(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0243-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0244(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0244-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0245(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0245-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0246(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0246-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0247(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0247-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0248(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0248-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0249(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0249-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0250(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0250-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0251(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0251-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0252(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0252-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0253(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0253-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0254(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0254-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0255(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0255-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0256(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0256-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0257(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0257-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0258(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0258-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0259(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0259-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0260(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0260-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0261(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0261-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0262(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0262-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0263(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0263-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0264(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0264-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0265(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0265-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0266(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0266-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0267(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0267-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0268(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0268-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0269(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0269-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0270(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0270-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0271(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0271-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0272(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0272-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0273(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0273-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0274(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0274-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0275(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0275-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0276(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0276-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0277(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0277-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0278(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0278-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0279(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0279-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0280(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0280-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0281(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0281-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0282(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0282-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0283(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0283-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0284(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0284-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0285(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0285-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0286(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0286-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0287(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0287-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0288(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0288-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0289(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0289-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0290(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0290-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0291(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0291-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0292(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0292-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0293(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0293-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0294(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0294-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0295(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0295-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0296(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0296-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0297(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0297-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0298(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0298-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0299(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0299-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0300(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0300-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0301(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0301-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0302(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0302-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0303(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0303-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0304(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0304-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0305(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0305-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0306(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0306-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0307(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0307-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0308(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0308-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0309(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0309-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0310(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0310-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0311(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0311-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0312(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0312-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0313(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0313-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0314(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0314-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0315(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0315-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0316(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0316-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0317(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0317-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0318(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0318-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0319(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0319-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0320(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0320-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0321(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0321-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0322(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0322-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0323(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0323-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0324(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0324-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0325(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0325-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0326(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0326-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0327(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0327-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0328(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0328-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0329(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0329-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0330(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0330-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0331(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0331-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0332(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0332-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0333(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0333-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0334(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0334-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0335(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0335-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0336(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0336-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0337(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0337-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0338(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0338-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0339(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0339-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0340(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0340-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0341(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0341-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0342(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0342-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0343(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0343-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0344(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0344-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0345(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0345-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0346(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0346-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0347(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0347-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0348(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0348-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0349(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0349-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0350(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0350-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0351(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0351-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0352(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0352-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0353(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0353-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0354(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0354-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0355(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0355-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0356(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0356-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0357(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0357-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0358(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0358-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0359(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0359-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0360(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0360-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0361(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0361-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0362(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0362-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0363(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0363-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0364(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0364-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0365(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0365-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0366(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0366-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0367(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0367-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0368(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0368-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0369(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0369-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0370(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0370-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0371(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0371-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0372(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0372-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0373(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0373-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0374(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0374-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0375(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0375-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0376(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0376-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0377(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0377-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0378(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0378-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0379(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0379-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0380(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0380-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0381(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0381-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0382(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0382-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0383(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0383-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0384(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0384-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0385(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0385-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0386(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0386-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0387(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0387-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0388(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0388-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0389(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0389-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0390(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0390-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0391(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0391-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0392(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0392-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0393(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0393-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0394(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0394-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0395(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0395-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0396(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0396-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0397(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0397-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0398(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0398-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0399(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0399-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0400(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0400-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0401(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0401-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0402(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0402-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0403(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0403-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0404(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0404-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0405(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0405-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0406(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0406-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0407(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0407-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0408(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0408-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0409(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0409-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0410(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0410-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0411(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0411-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0412(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0412-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0413(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0413-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0414(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0414-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0415(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0415-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0416(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0416-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0417(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0417-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0418(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0418-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0419(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0419-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0420(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0420-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0421(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0421-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0422(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0422-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0423(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0423-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0424(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0424-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0425(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0425-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0426(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0426-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0427(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0427-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0428(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0428-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0429(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0429-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0430(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0430-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0431(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0431-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0432(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0432-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0433(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0433-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0434(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0434-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0435(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0435-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0436(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0436-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0437(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0437-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0438(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0438-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0439(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0439-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0440(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0440-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0441(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0441-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0442(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0442-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0443(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0443-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0444(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0444-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0445(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0445-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0446(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0446-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0447(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0447-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0448(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0448-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0449(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0449-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0450(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0450-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0451(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0451-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0452(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0452-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0453(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0453-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0454(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0454-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0455(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0455-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0456(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0456-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0457(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0457-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0458(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0458-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0459(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0459-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0460(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0460-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0461(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0461-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0462(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0462-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0463(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0463-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0464(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0464-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0465(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0465-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0466(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0466-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0467(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0467-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0468(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0468-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0469(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0469-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def audit_rule_0470(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0470-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def audit_rule_0471(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0471-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def audit_rule_0472(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0472-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def audit_rule_0473(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0473-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def audit_rule_0474(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0474-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def audit_rule_0475(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0475-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def audit_rule_0476(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0476-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def audit_rule_0477(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0477-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def audit_rule_0478(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0478-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def audit_rule_0479(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 63.000) / 63.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0479-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def audit_rule_0480(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0480-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def audit_rule_0481(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0481-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def audit_rule_0482(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0482-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def audit_rule_0483(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0483-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def audit_rule_0484(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0484-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def audit_rule_0485(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0485-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def audit_rule_0486(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0486-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def audit_rule_0487(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0487-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def audit_rule_0488(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0488-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def audit_rule_0489(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0489-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def audit_rule_0490(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0490-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def audit_rule_0491(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0491-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def audit_rule_0492(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0492-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0493(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0493-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def audit_rule_0494(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0494-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def audit_rule_0495(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0495-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def audit_rule_0496(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0496-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def audit_rule_0497(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0497-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def audit_rule_0498(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0498-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def audit_rule_0499(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0499-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def audit_rule_0500(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0500-support",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def audit_rule_0501(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 127.000) / 127.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0501-interface",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def audit_rule_0502(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0502-bulk_hatch",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def audit_rule_0503(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0503-lattice",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def audit_rule_0504(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0504-thin_wall",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def audit_rule_0505(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0505-contour",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def audit_rule_0506(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0506-upskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def audit_rule_0507(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0507-bridge",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def audit_rule_0508(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0508-overhang",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def audit_rule_0509(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="audit-0509-downskin",
        family="audit",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def evaluate_audit_policy(index: int, obs: Observation) -> RuleResult:
    if index < 0 or index >= 510:
        raise ValueError("policy index must be between 0 and 509")
    lookup = globals()[f"audit_rule_{index:04d}"]
    return lookup(obs)
