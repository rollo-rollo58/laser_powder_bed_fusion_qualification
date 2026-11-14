"use client";

import { useState } from "react";
import { optimizeBuild } from "@/lib/api-client";
import type { OptimizationCandidate } from "@/types/domain";

export function SimulationControls() {
  const [target, setTarget] = useState(62);
  const [options, setOptions] = useState<OptimizationCandidate[]>([]);
  const [status, setStatus] = useState("idle");
  const run = async () => {
    setStatus("running");
    try { setOptions(await optimizeBuild(target)); setStatus("complete"); }
    catch { setStatus("API unavailable"); }
  };
  return (
    <section className="panel">
      <p className="eyebrow">Experiment designer</p>
      <h2 className="mt-1 text-xl font-semibold">Parameter search</h2>
      <label className="mt-4 block text-sm text-slate-300">Target volumetric energy (J/mm³)
        <input className="field mt-2 w-full" type="number" min="1" max="250"
          value={target} onChange={(event) => setTarget(Number(event.target.value))} />
      </label>
      <button className="action mt-4" onClick={run} disabled={status === "running"}>
        {status === "running" ? "Evaluating" : "Run bounded search"}
      </button>
      <p className="mt-3 muted">{status} / {options.length} qualifying candidates</p>
      <div className="mt-4 max-h-44 overflow-auto text-sm">
        {options.slice(0, 6).map((candidate, index) => <p key={index}
          className="border-b border-stroke py-2">
          {candidate.laser_power_w} W · {candidate.scan_speed_mm_s} mm/s ·
          {candidate.predicted_energy_j_mm3.toFixed(1)} J/mm³
        </p>)}
      </div>
    </section>
  );
}
