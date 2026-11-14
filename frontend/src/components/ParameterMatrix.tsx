"use client";

import { useMemo, useState } from "react";

export function ParameterMatrix() {
  const [power, setPower] = useState(275);
  const [speed, setSpeed] = useState(1100);
  const matrix = useMemo(() => [0.09, 0.11, 0.13, 0.15].map((hatch) =>
    [180, 220, 260, 300, 340].map((candidatePower) =>
      candidatePower / (speed * hatch * 0.04))), [speed]);
  const current = power / (speed * 0.105 * 0.04);
  return (
    <section className="panel">
      <p className="eyebrow">Process envelope</p>
      <h2 className="mt-1 text-xl font-semibold">Parameter surface</h2>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <label className="text-xs text-slate-300">Laser power (W)
          <input className="field mt-1 w-full" type="number" min="20" max="1200"
                 value={power} onChange={(event) => setPower(Number(event.target.value))} />
        </label>
        <label className="text-xs text-slate-300">Scan speed (mm/s)
          <input className="field mt-1 w-full" type="number" min="10" max="5000"
                 value={speed} onChange={(event) => setSpeed(Number(event.target.value))} />
        </label>
      </div>
      <p className="mt-3 text-sm">Current energy: <b>{current.toFixed(2)} J/mm³</b></p>
      <div className="mt-4 grid grid-cols-5 gap-2" aria-label="Volumetric energy matrix">
        {matrix.flat().map((energy, index) => (
          <div key={index} className="rounded p-2 text-center text-xs text-slate-950"
            style={{ background: `hsl(${Math.max(5, 175 - energy)} 70% 69%)` }}>
            {energy.toFixed(0)}
          </div>
        ))}
      </div>
      <p className="mt-3 muted">Values represent surrogate volumetric energy density.</p>
    </section>
  );
}
