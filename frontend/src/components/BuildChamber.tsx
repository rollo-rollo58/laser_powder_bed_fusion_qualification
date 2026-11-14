"use client";

import { useMemo, useState } from "react";

export function BuildChamber({ temperature }: { temperature: number }) {
  const [showScan, setShowScan] = useState(true);
  const tracks = useMemo(() => Array.from({ length: 18 }, (_, i) => i), []);
  return (
    <section className="panel">
      <div className="flex items-center justify-between">
        <div><p className="eyebrow">Machine cross-section</p>
          <h2 className="mt-1 text-xl font-semibold">Build chamber</h2></div>
        <button onClick={() => setShowScan((value) => !value)} className="action">
          {showScan ? "Hide scan vectors" : "Show scan vectors"}
        </button>
      </div>
      <svg viewBox="0 0 480 260" className="mt-5 w-full rounded-xl bg-shell"
           role="img" aria-label="Schematic build plate, optics and scan paths">
        <rect x="35" y="28" width="410" height="204" fill="none" stroke="#355064" />
        <path d="M220 10 L260 10 L275 45 L205 45 Z" fill="#dbeafe" opacity=".7" />
        <path d="M240 45 L240 153" stroke="#67e8d6" strokeWidth="3" />
        <rect x="85" y="188" width="300" height="20" rx="3" fill="#6b8090" />
        <rect x="112" y="171" width="250" height="16" fill="#de8a60" opacity=".85" />
        {showScan && tracks.map((index) => (
          <path key={index} d={`M${125 + index * 13} 172 L${175 + index * 10} 185`}
                stroke="#ff956c" strokeWidth="1.4" opacity=".7" />
        ))}
        <circle cx="240" cy="171" r="9" fill="#fff3b5" />
        <text x="45" y="246" fill="#9eb6c5" fontSize="13">
          Chamber {temperature.toFixed(1)} °C / research schematic
        </text>
      </svg>
    </section>
  );
}
