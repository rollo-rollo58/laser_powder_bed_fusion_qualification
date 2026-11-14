"use client";

import { useState } from "react";

const gates = ["Powder chemistry", "Machine calibration", "Chamber oxygen",
  "Density coupons", "Surface inspection", "Metallography", "Dimensional inspection"];

export function QualificationChecklist() {
  const [checked, setChecked] = useState<string[]>(gates.slice(0, 3));
  const toggle = (gate: string) => setChecked((old) => old.includes(gate)
    ? old.filter((value) => value !== gate) : [...old, gate]);
  return (
    <section className="panel">
      <p className="eyebrow">Release protocol</p>
      <h2 className="mt-1 text-xl font-semibold">Qualification gates</h2>
      <p className="mt-2 muted">Local demonstration checklists are not release evidence.</p>
      <div className="mt-4 space-y-2">
        {gates.map((gate) => <label key={gate}
          className="flex items-center gap-3 rounded-lg border border-stroke p-3 text-sm">
          <input type="checkbox" checked={checked.includes(gate)}
                 onChange={() => toggle(gate)} className="accent-teal-300" />
          {gate}
        </label>)}
      </div>
      <p className="mt-4 text-aqua">{checked.length} of {gates.length} gates selected</p>
    </section>
  );
}
