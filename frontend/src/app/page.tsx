"use client";

import { useCallback, useEffect, useState } from "react";
import { Activity, FlaskConical, Pause, Play } from "lucide-react";
import { BuildOverview } from "@/components/BuildOverview";
import { BuildChamber } from "@/components/BuildChamber";
import { MeltPoolPlot } from "@/components/MeltPoolPlot";
import { LayerTimeline } from "@/components/LayerTimeline";
import { PowderLotInspector } from "@/components/PowderLotInspector";
import { ParameterMatrix } from "@/components/ParameterMatrix";
import { DefectRiskPanel } from "@/components/DefectRiskPanel";
import { QualificationChecklist } from "@/components/QualificationChecklist";
import { RecoaterDiagnostics } from "@/components/RecoaterDiagnostics";
import { ThermalGradientMap } from "@/components/ThermalGradientMap";
import { SimulationControls } from "@/components/SimulationControls";
import { EventAuditTrail } from "@/components/EventAuditTrail";
import { evaluateObservation, getBuilds } from "@/lib/api-client";
import { useDomainTelemetry } from "@/hooks/useDomainTelemetry";
import type { BuildRecord, EvaluationResponse } from "@/types/domain";
import { defaultObservation } from "@/types/domain";

export default function Dashboard() {
  const [playing, setPlaying] = useState(true);
  const [builds, setBuilds] = useState<BuildRecord[]>([]);
  const [evaluation, setEvaluation] = useState<EvaluationResponse | null>(null);
  const [error, setError] = useState("");
  const telemetry = useDomainTelemetry(playing);
  const current = telemetry.latest?.observation ?? defaultObservation;

  const evaluate = useCallback(async () => {
    try {
      setEvaluation(await evaluateObservation(current));
      setError("");
    } catch { setError("API evaluation is unavailable"); }
  }, [current]);

  useEffect(() => {
    const controller = new AbortController();
    getBuilds(controller.signal).then(setBuilds).catch(() => setBuilds([]));
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if ((event.target as HTMLElement).tagName.match(/INPUT|SELECT|TEXTAREA/)) return;
      if (event.code === "Space") { event.preventDefault(); setPlaying((value) => !value); }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <main className="mx-auto max-w-screen-2xl px-4 pb-16 pt-7 sm:px-8">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="rounded-xl bg-aqua/20 p-3 text-aqua"><FlaskConical /></div>
          <div><p className="eyebrow">Advanced manufacturing / research sandbox</p>
            <h1 className="text-3xl font-semibold tracking-tight">LPBF Process Qualification</h1>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex items-center gap-2 text-sm text-slate-300">
            <Activity size={15} /> Stream: {telemetry.status}
          </span>
          <button className="action flex items-center gap-2"
            onClick={() => setPlaying((value) => !value)}>
            {playing ? <Pause size={16} /> : <Play size={16} />}
            {playing ? "Pause feed" : "Resume feed"}
          </button>
          <button className="action" onClick={evaluate}>Evaluate layer</button>
        </div>
      </header>
      <p className="mb-6 rounded-lg border border-orange-900/50 bg-orange-950/20 p-3 text-sm">
        Research-only synthetic telemetry and risk proxies. Not for machine control or certification.
      </p>
      {error && <p role="alert" className="mb-4 text-orange-300">{error}</p>}
      <div className="grid gap-5 xl:grid-cols-12">
        <div className="xl:col-span-4"><BuildOverview builds={builds} /></div>
        <div className="xl:col-span-5"><BuildChamber temperature={current.chamber_temp_c} /></div>
        <div className="xl:col-span-3"><DefectRiskPanel risk={evaluation?.risk ?? null} /></div>
        <div className="xl:col-span-6"><MeltPoolPlot samples={telemetry.samples} /></div>
        <div className="xl:col-span-6"><LayerTimeline /></div>
        <div className="xl:col-span-4"><PowderLotInspector /></div>
        <div className="xl:col-span-4"><ParameterMatrix /></div>
        <div className="xl:col-span-4"><RecoaterDiagnostics force={current.recoater_force_n} /></div>
        <div className="xl:col-span-4"><ThermalGradientMap /></div>
        <div className="xl:col-span-4"><SimulationControls /></div>
        <div className="xl:col-span-4"><QualificationChecklist /></div>
        <div className="xl:col-span-12"><EventAuditTrail /></div>
      </div>
      <footer className="mt-10 text-xs text-slate-500">
        Synthetic additive manufacturing R&D workbench. Press Space to pause or resume telemetry.
      </footer>
    </main>
  );
}
