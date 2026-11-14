"use client";

import { useState } from "react";

export function ThermalGradientMap() {
  const [phase, setPhase] = useState(0);
  const cells = Array.from({ length: 144 }, (_, index) => {
    const x = index % 12;
    const y = Math.floor(index / 12);
    const radius = Math.hypot(x - 6 + phase * 0.4, y - 5);
    return Math.max(0, 1 - radius / 9);
  });
  return (
    <section className="panel">
      <p className="eyebrow">Layer thermography</p>
      <h2 className="mt-1 text-xl font-semibold">Thermal field surrogate</h2>
      <svg viewBox="0 0 348 348" className="mt-4 w-full max-w-sm rounded"
           role="img" aria-label="Synthetic 12 by 12 thermal field map">
        {cells.map((heat, index) => <rect key={index} x={(index % 12) * 29}
          y={Math.floor(index / 12) * 29} width="28" height="28"
          fill={`hsl(${220 - heat * 195} 85% ${22 + heat * 45}%)`} />)}
      </svg>
      <label className="mt-4 block text-sm">Scan rotation phase: {phase}
        <input className="mt-2 w-full accent-orange-300" type="range" min="0" max="6"
               value={phase} onChange={(event) => setPhase(Number(event.target.value))} />
      </label>
    </section>
  );
}
