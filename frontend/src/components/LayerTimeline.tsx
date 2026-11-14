"use client";

import { useState } from "react";

export function LayerTimeline({ total = 2160 }: { total?: number }) {
  const [layer, setLayer] = useState(1253);
  const [interval, setInterval] = useState(25);
  const ticks = Array.from({ length: 30 }, (_, i) => i);
  return (
    <section className="panel">
      <p className="eyebrow">Build navigation</p>
      <h2 className="mt-1 text-xl font-semibold">Layer inspection</h2>
      <div className="mt-5 flex justify-between">
        <span className="metric">Layer {layer}</span>
        <span className="muted">/ {total} planned</span>
      </div>
      <input className="mt-5 w-full accent-teal-300" type="range" min="1" max={total}
             value={Math.min(layer, total)} aria-label="Selected layer"
             onChange={(event) => setLayer(Number(event.target.value))} />
      <div className="mt-4 flex gap-1" aria-hidden="true">
        {ticks.map((tick) => <div key={tick}
          className={`h-10 flex-1 rounded-sm ${tick % 7 === 0 ? "bg-thermal" : "bg-aqua/60"}`} />)}
      </div>
      <label className="mt-4 flex items-center justify-between gap-4 text-sm">
        Temporal aggregation
        <select className="field" value={interval}
                onChange={(event) => setInterval(Number(event.target.value))}>
          <option value="10">10 layers</option><option value="25">25 layers</option>
          <option value="50">50 layers</option>
        </select>
      </label>
      <p className="mt-3 muted">Inspecting {interval}-layer context near layer {layer}.</p>
    </section>
  );
}
