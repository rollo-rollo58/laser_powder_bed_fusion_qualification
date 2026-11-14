import type { RiskResult } from "@/types/domain";

export function DefectRiskPanel({ risk }: { risk: RiskResult | null }) {
  const level = risk?.overall_risk ?? 0;
  const color = level > 0.55 ? "#ff956c" : level > 0.25 ? "#ffd18c" : "#67e8d6";
  const circumference = 2 * Math.PI * 72;
  return (
    <section className="panel">
      <p className="eyebrow">Quality screening</p>
      <h2 className="mt-1 text-xl font-semibold">Defect risk proxy</h2>
      <div className="mt-4 flex items-center gap-6">
        <svg viewBox="0 0 180 180" className="w-40 shrink-0" role="img"
             aria-label={`Synthetic risk proxy ${Math.round(level * 100)} percent`}>
          <circle cx="90" cy="90" r="72" stroke="#394a5c" strokeWidth="12" fill="none" />
          <circle cx="90" cy="90" r="72" stroke={color} strokeWidth="12" fill="none"
                  strokeDasharray={`${circumference * level} ${circumference}`}
                  transform="rotate(-90 90 90)" strokeLinecap="round" />
          <text x="90" y="98" textAnchor="middle" fill="white" fontSize="28">
            {Math.round(level * 100)}%
          </text>
        </svg>
        <div><p className="metric" style={{ color }}>{risk?.severity ?? "Unscored"}</p>
          <p className="muted">Recommended: {risk?.recommended_action ?? "evaluate"}</p></div>
      </div>
      <ul className="mt-3 space-y-1 text-sm text-orange-200">
        {(risk?.warnings ?? []).map((warning) => <li key={warning}>{warning}</li>)}
      </ul>
      <p className="mt-3 muted">Heuristic estimate, not a validated defect probability.</p>
    </section>
  );
}
