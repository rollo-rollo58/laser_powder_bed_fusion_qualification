import type { StreamPacket } from "@/types/domain";

const endpoint = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000")
  .replace(/^http/, "ws");

export function openTelemetryStream(
  onPacket: (packet: StreamPacket) => void,
  onStatus: (status: string) => void,
): () => void {
  if (typeof WebSocket === "undefined") return () => undefined;
  let disposed = false;
  let socket: WebSocket | null = null;
  let retry: ReturnType<typeof setTimeout> | null = null;
  let attempt = 0;

  const connect = () => {
    if (disposed) return;
    socket = new WebSocket(`${endpoint}/ws/telemetry`);
    onStatus("connecting");
    socket.onopen = () => { attempt = 0; onStatus("connected"); };
    socket.onmessage = (message: MessageEvent<string>) => {
      try {
        const payload = JSON.parse(message.data) as StreamPacket;
        if (typeof payload.sequence === "number") onPacket(payload);
      } catch { onStatus("invalid packet"); }
    };
    socket.onerror = () => onStatus("network error");
    socket.onclose = () => {
      onStatus("disconnected");
      if (!disposed) {
        const timeout = Math.min(12000, 700 * 2 ** Math.min(attempt++, 5));
        retry = setTimeout(connect, timeout);
      }
    };
  };
  connect();

  return () => {
    disposed = true;
    if (retry) clearTimeout(retry);
    socket?.close();
  };
}
