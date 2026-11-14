"use client";

import { useEffect, useState } from "react";
import { openTelemetryStream } from "@/lib/websocket-stream";
import type { StreamPacket } from "@/types/domain";

export function useDomainTelemetry(enabled: boolean) {
  const [status, setStatus] = useState("idle");
  const [samples, setSamples] = useState<StreamPacket[]>([]);

  useEffect(() => {
    if (!enabled) {
      setStatus("paused");
      return;
    }
    return openTelemetryStream(
      (packet) => setSamples((previous) => [...previous, packet].slice(-80)),
      setStatus,
    );
  }, [enabled]);

  return { status, samples, latest: samples[samples.length - 1] ?? null };
}
