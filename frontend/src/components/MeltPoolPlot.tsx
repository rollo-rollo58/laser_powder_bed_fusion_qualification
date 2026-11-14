"use client";

import { useState } from "react";
import type { StreamPacket } from "@/types/domain";

export function MeltPoolPlot({ samples }: { samples: StreamPacket[] }) {
  const [metric, setMetric] = useState<"melt_pool_width_um" | "cooling_rate_k_s">(
    "melt_pool_width_um",
  );
  const values = samples.map((sample) => sample.physics[metric]);
  const maximum = Math.max(1, ...values);
  const points = values.map((value, index) => {
    const x = 18 + index * (444 / Math.max(1, values.length - 1));
    const y = 177 - (value / maximum) * 150;
    return `${x.toFixed(2)},${y.toFixed(2)}`;
  }).join(" ");
  return (
    <section className="panel">
      <div className="flex items-center justify-between gap-2">
        <div><p className="eyebrow">Optical process proxy</p>
          <h2 className="mt-1 text-lg font-semibold">Melt-pool trend</h2></div>
        <select className="field" value={metric} onChange={(event) =>
          setMetric(event.target.value as typeof metric)} aria-label="Melt pool metric">
          <option value="melt_pool_width_um">Width (µm)</option>
          <option value="cooling_rate_k_s">Cooling rate (K/s)</option>
        </select>
      </div>
      <svg viewBox="0 0 480 200" className="mt-4 w-full grid-lines"
           role="img" aria-label="Live melt pool monitoring line chart">
        <path d="M18 12 V178 H462" fill="none" stroke="#536b7b" />
        <polyline points={points} stroke="#67e8d6" strokeWidth="2.5" fill="none" />
        <text x="25" y="19" fill="#bdc9d7" fontSize="12">{maximum.toFixed(1)}</text>
        <text x="400" y="194" fill="#bdc9d7" fontSize="12">Latest</text>
      </svg>
      <p className="muted">{values.length} streamed samples in rolling window</p>
    </section>
  );
}
