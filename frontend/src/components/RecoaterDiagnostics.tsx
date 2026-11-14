"use client";

import { useState } from "react";

export function RecoaterDiagnostics({ force }: { force: number }) {
  const [limit, setLimit] = useState(30);
  const level = Math.min(100, (force / Math.max(limit, 1)) * 100);
  return (
    <section className="panel">
      <p className="eyebrow">Mechanical condition</p>
      <h2 className="mt-1 text-xl font-semibold">Recoater diagnostics</h2>
      <p className="mt-4 metric">{force.toFixed(1)} N</p>
      <p className="muted">Estimated blade drag force</p>
      <div className="mt-4 h-4 overflow-hidden rounded-full bg-slate-700">
        <div className={`h-full ${force > limit ? "bg-orange-400" : "bg-aqua"}`}
             style={{ width: `${level}%` }} />
      </div>
      <label className="mt-5 block text-sm text-slate-300">
        Research alarm threshold: {limit} N
        <input className="mt-3 w-full accent-teal-300" type="range" min="10" max="80"
               value={limit} onChange={(event) => setLimit(Number(event.target.value))} />
      </label>
      <p className={`mt-3 text-sm ${force > limit ? "text-orange-300" : "text-aqua"}`}>
        {force > limit ? "Over demonstration threshold" : "Within demonstration threshold"}
      </p>
    </section>
  );
}
