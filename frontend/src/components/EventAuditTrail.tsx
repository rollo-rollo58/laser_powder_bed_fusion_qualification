"use client";

import { useCallback, useState } from "react";
import { getEvents } from "@/lib/api-client";

interface AuditEvent {
  type: string;
  occurred_at: string;
  checksum: string;
}

export function EventAuditTrail() {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState("");
  const refresh = useCallback(async () => {
    try { setEvents(await getEvents()); setError(""); }
    catch { setError("Could not fetch event journal"); }
  }, []);
  return (
    <section className="panel">
      <div className="flex items-center justify-between">
        <div><p className="eyebrow">Traceability</p>
          <h2 className="mt-1 text-xl font-semibold">Audit event journal</h2></div>
        <button className="action" onClick={refresh}>Refresh events</button>
      </div>
      {error && <p role="alert" className="mt-3 text-orange-300">{error}</p>}
      <div className="mt-4 max-h-56 space-y-3 overflow-auto">
        {events.length === 0 && <p className="muted">No events loaded.</p>}
        {events.map((event, index) => <div key={`${event.checksum}-${index}`}
          className="border-b border-stroke pb-2 text-sm">
          <p className="font-medium">{event.type}</p>
          <p className="muted">{event.occurred_at}</p>
          <code className="text-xs text-aqua">{event.checksum.slice(0, 20)}</code>
        </div>)}
      </div>
    </section>
  );
}
