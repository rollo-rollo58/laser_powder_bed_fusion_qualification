import type {
  BuildRecord, EvaluationResponse, Observation, OptimizationCandidate,
} from "@/types/domain";

const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const payload = await response.text();
    throw new Error(`API ${response.status}: ${payload.slice(0, 240)}`);
  }
  return (await response.json()) as T;
}

export async function getBuilds(signal?: AbortSignal): Promise<BuildRecord[]> {
  return parseJson<BuildRecord[]>(await fetch(`${baseUrl}/api/v1/builds`, {
    cache: "no-store", signal,
  }));
}

export async function evaluateObservation(
  observation: Observation,
): Promise<EvaluationResponse> {
  return parseJson<EvaluationResponse>(await fetch(`${baseUrl}/api/v1/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(observation),
  }));
}

export async function optimizeBuild(targetEnergy: number): Promise<OptimizationCandidate[]> {
  return parseJson<OptimizationCandidate[]>(await fetch(`${baseUrl}/api/v1/optimize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ target_energy_j_mm3: targetEnergy }),
  }));
}

export async function getGates(buildId: string): Promise<{
  gates: Array<{ code: string; state: string; evidence: string }>;
}> {
  return parseJson(await fetch(`${baseUrl}/api/v1/qualification/${buildId}`, {
    cache: "no-store",
  }));
}

export async function getEvents(): Promise<Array<{
  type: string; occurred_at: string; checksum: string;
}>> {
  return parseJson(await fetch(`${baseUrl}/api/v1/events`, { cache: "no-store" }));
}
