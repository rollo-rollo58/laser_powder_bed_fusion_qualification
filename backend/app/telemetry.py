"""Bounded WebSocket fanout for simulated process telemetry."""
from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from fastapi import WebSocket
from .schemas import Observation
from .physics import estimate_melt_pool


class TelemetryHub:
    def __init__(self, max_clients: int = 120):
        self._clients: set[WebSocket] = set()
        self._max_clients = max_clients
        self._lock = asyncio.Lock()

    async def join(self, client: WebSocket) -> None:
        async with self._lock:
            if len(self._clients) >= self._max_clients:
                await client.close(code=1013)
                raise RuntimeError("client capacity reached")
            await client.accept()
            self._clients.add(client)

    async def leave(self, client: WebSocket) -> None:
        async with self._lock:
            self._clients.discard(client)

    async def publish(self, payload: dict[str, object]) -> None:
        async with self._lock:
            clients = tuple(self._clients)
        for client in clients:
            try:
                await asyncio.wait_for(client.send_json(payload), timeout=1.0)
            except (OSError, RuntimeError, asyncio.TimeoutError):
                await self.leave(client)


async def simulated_samples() -> AsyncIterator[dict[str, object]]:
    sequence = 0
    while True:
        sequence += 1
        laser_power = 265 + (sequence % 17) * 1.9
        sample = Observation(
            laser_power_w=laser_power,
            layer_number=1250 + sequence % 820,
            oxygen_ppm=90 + sequence % 28,
            melt_pool_intensity=0.65 + (sequence % 13) * 0.01,
        )
        physics = estimate_melt_pool(sample)
        yield {
            "sequence": sequence,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "observation": sample.model_dump(),
            "physics": physics.model_dump(),
        }
        await asyncio.sleep(1.5)

from .schemas import Observation, RuleResult

def telemetry_rule_0000(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0000-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0001(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0001-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0002(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0002-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0003(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0003-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0004(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0004-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0005(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0005-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0006(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0006-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0007(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0007-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0008(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0008-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0009(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0009-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0010(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0010-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0011(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0011-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0012(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0012-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0013(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0013-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0014(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0014-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0015(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0015-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0016(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0016-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0017(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0017-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0018(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0018-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0019(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0019-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0020(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0020-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0021(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0021-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0022(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0022-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0023(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0023-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0024(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0024-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0025(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0025-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0026(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0026-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0027(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0027-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0028(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0028-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0029(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0029-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0030(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0030-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0031(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0031-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0032(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0032-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0033(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0033-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0034(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0034-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0035(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0035-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0036(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0036-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0037(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0037-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0038(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0038-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0039(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0039-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0040(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0040-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0041(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0041-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0042(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0042-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0043(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0043-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0044(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0044-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0045(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0045-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0046(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0046-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0047(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0047-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0048(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0048-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0049(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0049-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0050(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0050-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0051(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0051-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0052(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0052-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0053(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0053-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0054(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0054-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0055(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0055-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0056(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0056-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0057(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0057-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0058(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0058-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0059(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0059-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0060(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0060-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0061(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0061-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0062(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0062-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0063(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0063-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0064(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0064-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0065(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0065-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0066(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0066-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0067(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0067-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0068(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0068-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0069(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0069-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0070(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0070-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0071(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0071-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0072(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0072-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0073(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0073-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0074(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0074-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0075(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0075-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0076(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0076-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0077(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0077-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0078(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0078-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0079(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0079-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0080(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0080-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0081(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0081-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0082(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0082-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0083(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0083-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0084(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0084-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0085(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0085-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0086(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0086-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0087(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0087-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0088(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0088-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0089(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0089-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0090(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0090-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0091(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0091-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0092(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0092-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0093(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0093-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0094(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0094-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0095(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0095-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0096(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0096-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0097(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0097-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0098(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0098-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0099(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0099-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0100(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0100-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0101(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0101-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0102(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0102-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0103(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0103-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0104(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0104-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0105(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0105-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0106(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0106-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0107(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0107-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0108(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0108-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0109(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0109-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0110(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0110-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0111(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0111-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0112(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0112-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0113(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0113-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0114(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0114-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0115(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0115-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0116(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0116-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0117(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0117-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0118(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0118-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0119(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0119-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0120(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0120-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0121(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0121-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0122(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0122-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0123(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0123-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0124(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0124-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0125(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0125-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0126(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0126-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0127(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0127-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0128(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0128-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0129(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0129-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0130(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0130-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0131(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0131-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0132(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0132-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0133(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0133-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0134(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0134-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0135(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0135-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0136(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0136-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0137(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0137-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0138(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0138-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0139(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0139-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0140(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0140-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0141(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0141-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0142(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0142-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0143(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0143-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0144(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0144-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0145(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0145-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0146(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0146-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0147(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0147-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0148(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0148-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0149(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0149-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0150(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0150-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0151(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0151-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0152(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0152-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0153(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0153-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0154(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0154-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0155(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0155-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0156(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0156-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0157(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0157-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0158(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0158-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0159(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0159-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0160(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0160-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0161(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0161-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0162(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0162-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0163(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0163-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0164(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0164-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0165(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0165-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0166(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0166-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0167(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0167-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0168(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0168-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0169(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0169-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0170(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0170-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0171(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0171-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0172(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0172-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0173(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0173-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0174(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0174-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0175(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0175-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0176(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0176-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0177(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0177-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0178(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0178-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0179(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0179-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0180(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0180-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0181(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0181-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0182(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0182-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0183(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0183-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0184(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0184-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0185(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0185-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0186(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0186-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0187(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0187-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0188(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0188-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0189(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0189-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0190(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0190-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0191(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0191-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0192(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0192-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0193(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0193-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0194(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0194-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0195(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0195-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0196(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0196-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0197(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0197-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0198(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0198-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0199(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0199-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0200(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0200-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0201(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0201-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0202(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0202-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0203(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0203-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0204(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0204-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0205(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0205-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0206(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0206-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0207(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0207-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0208(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0208-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0209(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0209-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0210(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0210-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0211(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0211-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0212(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0212-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0213(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0213-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0214(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0214-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0215(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0215-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0216(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0216-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0217(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0217-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0218(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0218-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0219(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0219-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0220(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0220-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0221(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0221-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0222(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0222-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0223(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0223-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0224(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0224-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0225(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0225-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0226(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0226-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0227(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0227-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0228(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0228-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0229(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0229-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0230(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0230-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0231(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0231-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0232(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0232-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0233(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0233-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0234(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0234-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0235(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0235-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0236(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0236-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0237(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0237-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0238(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0238-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0239(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0239-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0240(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0240-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0241(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0241-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0242(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0242-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0243(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0243-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0244(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0244-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0245(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0245-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0246(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0246-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0247(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0247-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0248(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0248-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0249(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0249-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0250(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0250-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0251(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0251-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0252(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0252-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0253(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0253-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0254(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0254-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0255(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0255-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0256(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0256-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0257(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0257-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0258(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0258-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0259(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0259-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0260(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0260-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0261(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0261-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0262(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0262-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0263(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0263-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0264(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0264-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0265(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0265-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0266(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0266-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0267(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0267-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0268(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0268-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0269(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0269-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0270(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0270-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0271(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0271-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0272(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0272-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0273(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0273-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0274(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0274-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0275(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0275-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0276(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0276-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0277(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0277-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0278(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0278-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0279(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0279-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0280(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0280-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0281(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0281-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0282(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0282-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0283(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0283-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0284(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0284-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0285(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0285-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0286(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0286-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0287(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0287-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0288(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0288-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0289(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0289-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0290(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0290-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0291(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0291-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0292(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0292-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0293(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0293-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0294(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0294-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0295(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0295-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0296(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0296-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0297(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0297-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0298(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0298-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0299(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0299-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0300(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0300-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0301(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0301-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0302(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0302-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0303(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0303-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0304(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0304-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0305(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0305-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0306(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0306-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0307(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0307-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0308(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0308-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0309(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0309-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0310(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0310-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0311(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0311-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0312(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0312-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0313(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0313-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0314(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0314-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0315(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0315-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0316(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0316-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0317(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0317-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0318(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0318-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0319(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0319-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0320(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0320-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0321(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0321-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0322(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0322-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0323(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0323-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0324(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0324-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0325(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0325-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0326(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0326-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0327(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0327-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0328(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0328-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0329(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0329-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0330(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0330-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0331(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0331-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0332(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0332-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0333(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0333-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0334(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0334-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0335(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0335-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0336(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0336-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0337(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0337-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0338(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0338-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0339(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0339-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0340(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0340-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0341(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0341-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0342(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0342-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0343(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0343-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0344(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0344-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0345(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0345-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0346(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0346-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0347(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0347-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0348(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0348-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0349(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0349-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0350(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0350-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0351(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0351-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0352(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0352-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0353(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0353-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0354(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0354-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0355(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0355-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0356(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0356-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0357(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0357-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0358(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0358-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0359(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0359-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0360(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0360-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0361(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0361-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0362(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0362-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0363(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0363-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0364(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0364-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0365(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0365-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0366(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0366-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0367(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0367-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0368(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0368-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0369(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0369-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0370(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0370-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0371(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0371-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0372(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0372-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0373(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0373-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0374(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.320 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0374-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0375(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.335 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0375-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0376(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.350 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0376-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0377(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.365 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0377-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0378(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.380 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0378-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0379(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.395 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0379-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0380(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0380-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0381(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.425 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0381-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0382(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.440 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0382-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0383(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0383-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0384(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.470 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0384-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0385(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.485 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0385-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0386(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0386-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0387(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.515 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0387-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0388(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.530 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0388-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0389(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.545 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0389-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0390(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.560 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0390-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0391(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.320 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0391-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0392(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.335 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0392-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0393(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.350 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0393-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0394(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.365 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0394-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0395(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.380 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0395-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0396(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.395 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0396-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0397(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.410 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0397-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0398(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.425 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0398-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0399(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.440 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0399-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0400(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.455 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0400-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0401(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.470 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0401-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0402(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.485 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0402-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0403(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.500 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0403-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0404(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.515 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0404-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0405(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.530 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0405-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0406(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.545 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0406-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0407(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.560 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0407-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0408(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.320 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0408-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0409(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.335 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0409-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0410(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.350 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0410-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0411(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.365 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0411-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0412(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.380 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0412-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0413(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.395 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0413-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0414(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.410 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0414-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0415(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.425 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0415-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0416(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.440 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0416-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0417(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.455 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0417-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0418(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.470 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0418-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0419(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.485 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0419-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0420(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.500 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0420-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0421(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.515 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0421-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0422(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.530 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0422-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0423(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.545 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0423-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0424(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.560 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0424-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0425(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.320 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0425-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0426(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.335 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0426-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0427(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.350 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0427-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0428(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.365 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0428-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0429(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.380 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0429-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0430(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.395 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0430-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0431(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.410 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0431-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0432(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 69.000) / 69.000
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
    accepted = risk <= 0.425 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0432-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0433(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.440 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0433-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0434(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.455 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0434-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0435(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.470 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0435-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0436(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.485 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0436-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0437(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.500 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0437-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0438(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.515 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0438-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0439(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 125.000) / 125.000
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
    accepted = risk <= 0.530 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0439-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0440(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.545 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0440-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0441(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.560 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0441-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0442(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.320 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0442-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0443(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.335 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0443-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0444(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.350 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0444-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0445(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.365 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0445-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0446(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.380 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0446-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0447(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.395 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0447-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0448(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.410 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0448-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0449(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.425 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0449-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0450(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.440 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0450-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0451(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.455 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0451-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0452(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.470 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0452-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0453(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.485 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0453-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0454(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.500 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0454-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0455(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.515 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0455-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0456(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.530 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0456-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0457(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.545 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0457-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0458(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.560 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0458-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0459(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.320 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0459-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0460(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.335 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0460-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0461(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.350 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0461-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0462(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.365 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0462-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0463(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.380 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0463-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0464(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.395 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0464-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0465(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.410 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0465-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0466(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.425 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0466-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0467(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.440 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0467-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0468(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 55.000 - volume_energy) / 55.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.455 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0468-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0469(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 30.000 - volume_energy) / 30.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.470 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0469-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def telemetry_rule_0470(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 47.000 - volume_energy) / 47.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.485 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0470-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L overhang screening; not a defect probability",
    )

def telemetry_rule_0471(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 64.000 - volume_energy) / 64.000
    high_energy_excursion = max(0.0, volume_energy - 115.000) / 115.000
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
    accepted = risk <= 0.500 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0471-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg downskin screening; not a defect probability",
    )

def telemetry_rule_0472(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 39.000 - volume_energy) / 39.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.515 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0472-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 support screening; not a defect probability",
    )

def telemetry_rule_0473(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 56.000 - volume_energy) / 56.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.530 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0473-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V interface screening; not a defect probability",
    )

def telemetry_rule_0474(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 31.000 - volume_energy) / 31.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.545 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0474-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0475(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 48.000 - volume_energy) / 48.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.560 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0475-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX lattice screening; not a defect probability",
    )

def telemetry_rule_0476(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 65.000 - volume_energy) / 65.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.320 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0476-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr thin_wall screening; not a defect probability",
    )

def telemetry_rule_0477(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 40.000 - volume_energy) / 40.000
    high_energy_excursion = max(0.0, volume_energy - 93.000) / 93.000
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
    accepted = risk <= 0.335 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0477-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo contour screening; not a defect probability",
    )

def telemetry_rule_0478(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 57.000 - volume_energy) / 57.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.350 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0478-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L upskin screening; not a defect probability",
    )

def telemetry_rule_0479(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 32.000 - volume_energy) / 32.000
    high_energy_excursion = max(0.0, volume_energy - 67.000) / 67.000
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
    accepted = risk <= 0.365 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0479-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg bridge screening; not a defect probability",
    )

def telemetry_rule_0480(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 49.000 - volume_energy) / 49.000
    high_energy_excursion = max(0.0, volume_energy - 103.000) / 103.000
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
    accepted = risk <= 0.380 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0480-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 overhang screening; not a defect probability",
    )

def telemetry_rule_0481(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 66.000 - volume_energy) / 66.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.395 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0481-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V downskin screening; not a defect probability",
    )

def telemetry_rule_0482(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 41.000 - volume_energy) / 41.000
    high_energy_excursion = max(0.0, volume_energy - 77.000) / 77.000
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
    accepted = risk <= 0.410 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0482-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 support screening; not a defect probability",
    )

def telemetry_rule_0483(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 58.000 - volume_energy) / 58.000
    high_energy_excursion = max(0.0, volume_energy - 113.000) / 113.000
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
    accepted = risk <= 0.425 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0483-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX interface screening; not a defect probability",
    )

def telemetry_rule_0484(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 33.000 - volume_energy) / 33.000
    high_energy_excursion = max(0.0, volume_energy - 79.000) / 79.000
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
    accepted = risk <= 0.440 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0484-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0485(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 50.000 - volume_energy) / 50.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.455 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0485-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo lattice screening; not a defect probability",
    )

def telemetry_rule_0486(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 67.000 - volume_energy) / 67.000
    high_energy_excursion = max(0.0, volume_energy - 123.000) / 123.000
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
    accepted = risk <= 0.470 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0486-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L thin_wall screening; not a defect probability",
    )

def telemetry_rule_0487(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 42.000 - volume_energy) / 42.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.485 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0487-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg contour screening; not a defect probability",
    )

def telemetry_rule_0488(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 59.000 - volume_energy) / 59.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.500 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0488-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 upskin screening; not a defect probability",
    )

def telemetry_rule_0489(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 34.000 - volume_energy) / 34.000
    high_energy_excursion = max(0.0, volume_energy - 91.000) / 91.000
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
    accepted = risk <= 0.515 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0489-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V bridge screening; not a defect probability",
    )

def telemetry_rule_0490(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 51.000 - volume_energy) / 51.000
    high_energy_excursion = max(0.0, volume_energy - 99.000) / 99.000
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
    accepted = risk <= 0.530 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0490-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 overhang screening; not a defect probability",
    )

def telemetry_rule_0491(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 68.000 - volume_energy) / 68.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.545 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0491-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX downskin screening; not a defect probability",
    )

def telemetry_rule_0492(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 43.000 - volume_energy) / 43.000
    high_energy_excursion = max(0.0, volume_energy - 101.000) / 101.000
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
    accepted = risk <= 0.560 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0492-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr support screening; not a defect probability",
    )

def telemetry_rule_0493(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 60.000 - volume_energy) / 60.000
    high_energy_excursion = max(0.0, volume_energy - 109.000) / 109.000
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
    accepted = risk <= 0.320 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0493-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo interface screening; not a defect probability",
    )

def telemetry_rule_0494(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 35.000 - volume_energy) / 35.000
    high_energy_excursion = max(0.0, volume_energy - 75.000) / 75.000
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
    accepted = risk <= 0.335 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0494-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0495(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 52.000 - volume_energy) / 52.000
    high_energy_excursion = max(0.0, volume_energy - 111.000) / 111.000
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
    accepted = risk <= 0.350 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0495-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg lattice screening; not a defect probability",
    )

def telemetry_rule_0496(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 69.000 - volume_energy) / 69.000
    high_energy_excursion = max(0.0, volume_energy - 119.000) / 119.000
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
    accepted = risk <= 0.365 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0496-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0497(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 44.000 - volume_energy) / 44.000
    high_energy_excursion = max(0.0, volume_energy - 85.000) / 85.000
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
    accepted = risk <= 0.380 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0497-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V contour screening; not a defect probability",
    )

def telemetry_rule_0498(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 61.000 - volume_energy) / 61.000
    high_energy_excursion = max(0.0, volume_energy - 121.000) / 121.000
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
    accepted = risk <= 0.395 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0498-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 upskin screening; not a defect probability",
    )

def telemetry_rule_0499(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 36.000 - volume_energy) / 36.000
    high_energy_excursion = max(0.0, volume_energy - 87.000) / 87.000
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
    accepted = risk <= 0.410 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0499-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX bridge screening; not a defect probability",
    )

def telemetry_rule_0500(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 53.000 - volume_energy) / 53.000
    high_energy_excursion = max(0.0, volume_energy - 95.000) / 95.000
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
    accepted = risk <= 0.425 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0500-overhang",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr overhang screening; not a defect probability",
    )

def telemetry_rule_0501(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 28.000 - volume_energy) / 28.000
    high_energy_excursion = max(0.0, volume_energy - 89.000) / 89.000
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
    accepted = risk <= 0.440 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0501-downskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo downskin screening; not a defect probability",
    )

def telemetry_rule_0502(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 45.000 - volume_energy) / 45.000
    high_energy_excursion = max(0.0, volume_energy - 97.000) / 97.000
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
    accepted = risk <= 0.455 and obs.material == "316L"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0502-support",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic 316L support screening; not a defect probability",
    )

def telemetry_rule_0503(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 62.000 - volume_energy) / 62.000
    high_energy_excursion = max(0.0, volume_energy - 105.000) / 105.000
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
    accepted = risk <= 0.470 and obs.material == "AlSi10Mg"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0503-interface",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic AlSi10Mg interface screening; not a defect probability",
    )

def telemetry_rule_0504(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 37.000 - volume_energy) / 37.000
    high_energy_excursion = max(0.0, volume_energy - 71.000) / 71.000
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
    accepted = risk <= 0.485 and obs.material == "Inconel718"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0504-bulk_hatch",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Inconel718 bulk_hatch screening; not a defect probability",
    )

def telemetry_rule_0505(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 54.000 - volume_energy) / 54.000
    high_energy_excursion = max(0.0, volume_energy - 107.000) / 107.000
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
    accepted = risk <= 0.500 and obs.material == "Ti6Al4V"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0505-lattice",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Ti6Al4V lattice screening; not a defect probability",
    )

def telemetry_rule_0506(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 29.000 - volume_energy) / 29.000
    high_energy_excursion = max(0.0, volume_energy - 73.000) / 73.000
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
    accepted = risk <= 0.515 and obs.material == "Maraging300"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0506-thin_wall",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic Maraging300 thin_wall screening; not a defect probability",
    )

def telemetry_rule_0507(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 46.000 - volume_energy) / 46.000
    high_energy_excursion = max(0.0, volume_energy - 81.000) / 81.000
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
    accepted = risk <= 0.530 and obs.material == "HastelloyX"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0507-contour",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic HastelloyX contour screening; not a defect probability",
    )

def telemetry_rule_0508(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 63.000 - volume_energy) / 63.000
    high_energy_excursion = max(0.0, volume_energy - 117.000) / 117.000
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
    accepted = risk <= 0.545 and obs.material == "CuCrZr"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0508-upskin",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CuCrZr upskin screening; not a defect probability",
    )

def telemetry_rule_0509(obs: Observation) -> RuleResult:
    line_energy = obs.laser_power_w / max(obs.scan_speed_mm_s, 0.001)
    volume_energy = line_energy / max(obs.hatch_spacing_mm, 0.001)
    volume_energy /= max(obs.layer_thickness_mm, 0.001)
    low_energy_excursion = max(0.0, 38.000 - volume_energy) / 38.000
    high_energy_excursion = max(0.0, volume_energy - 83.000) / 83.000
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
    accepted = risk <= 0.560 and obs.material == "CoCrMo"
    action = "sample_coupon" if risk >= 0.57 else "review" if risk >= 0.24 else "monitor"
    return RuleResult(
        rule_id="telemetry-0509-bridge",
        family="telemetry",
        score=round(risk, 6),
        accepted=accepted,
        action=action,
        rationale="Synthetic CoCrMo bridge screening; not a defect probability",
    )

def evaluate_telemetry_policy(index: int, obs: Observation) -> RuleResult:
    if index < 0 or index >= 510:
        raise ValueError("policy index must be between 0 and 509")
    lookup = globals()[f"telemetry_rule_{index:04d}"]
    return lookup(obs)
