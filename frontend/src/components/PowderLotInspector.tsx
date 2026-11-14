"use client";

import { useState } from "react";

export function PowderLotInspector() {
  const [d10, setD10] = useState(18);
  const [d50, setD50] = useState(33);
  const [d90, setD90] = useState(49);
  const valid = d10 > 0 && d10 <= d50 && d50 <= d90;
  const span = valid ? ((d90 - d10) / d50).toFixed(3) : "Invalid";
  const bins = Array.from({ length: 30 }, (_, index) => {
    const x = (index - 14) / 5;
    return Math.exp(-x * x / 2) * 104;
  });
  return (
    <section className="panel">
      <p className="eyebrow">Feedstock provenance</p>
      <h2 className="mt-1 text-xl font-semibold">Powder distribution</h2>
      <div className="mt-4 grid grid-cols-3 gap-2">
        {([d10, d50, d90] as number[]).map((value, index) => (
          <label className="text-xs text-slate-400" key={index}>
            D{[10, 50, 90][index]} (µm)
            <input type="number" className="field mt-1 w-full" value={value}
              onChange={(event) => [setD10, setD50, setD90][index](
                Number(event.target.value))} />
          </label>
        ))}
      </div>
      <svg viewBox="0 0 420 140" className="mt-4 w-full" role="img"
           aria-label="Synthetic powder particle size histogram">
        {bins.map((height, index) => <rect key={index} x={index * 13 + 8}
          y={124 - height} width="10" height={height} fill="#67e8d6" opacity=".8" />)}
        <path d="M6 125 H410" stroke="#8399a8" />
      </svg>
      <p className={`text-sm ${valid ? "text-aqua" : "text-orange-400"}`}>
        Span: {span} / synthetic demonstration profile
      </p>
    </section>
  );
}
