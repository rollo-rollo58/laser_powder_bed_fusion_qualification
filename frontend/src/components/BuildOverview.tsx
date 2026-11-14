import type { BuildRecord } from "@/types/domain";

export function BuildOverview({ builds }: { builds: BuildRecord[] }) {
  const completed = builds.reduce((count, build) => count + build.completed_layers, 0);
  const total = builds.reduce((count, build) => count + build.layer_count, 0);
  const progress = total === 0 ? 0 : Math.round((completed / total) * 100);
  return (
    <section className="panel" aria-label="Build portfolio overview">
      <div className="eyebrow">Fleet overview</div>
      <h2 className="mt-2 text-xl font-semibold">Research build queue</h2>
      <div className="mt-5 grid grid-cols-3 gap-4">
        <div><p className="muted">Builds</p><p className="metric">{builds.length}</p></div>
        <div><p className="muted">Layer progress</p><p className="metric">{progress}%</p></div>
        <div><p className="muted">Printed layers</p><p className="metric">{completed}</p></div>
      </div>
      <div className="mt-5 h-2 rounded-full bg-slate-700" role="progressbar"
           aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}>
        <div className="h-2 rounded-full bg-aqua" style={{ width: `${progress}%` }} />
      </div>
      <div className="mt-5 space-y-3">
        {builds.map((build) => (
          <div key={build.id} className="flex justify-between border-b border-stroke pb-3">
            <div><p className="font-medium">{build.id}</p>
              <p className="muted">{build.material} / {build.machine_id}</p></div>
            <p className="text-sm text-aqua">{build.status}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
