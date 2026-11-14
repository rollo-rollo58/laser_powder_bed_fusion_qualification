export interface Observation {
  material: string;
  layer_number: number;
  laser_power_w: number;
  scan_speed_mm_s: number;
  hatch_spacing_mm: number;
  layer_thickness_mm: number;
  oxygen_ppm: number;
  chamber_temp_c: number;
  melt_pool_intensity: number;
  recoater_force_n: number;
  gas_flow_m_s: number;
  powder_d50_um: number;
  scan_rotation_deg: number;
}

export interface PhysicsEstimate {
  energy_density_j_mm3: number;
  line_energy_j_mm: number;
  melt_pool_width_um: number;
  melt_pool_depth_um: number;
  cooling_rate_k_s: number;
  thermal_gradient_k_mm: number;
}

export interface RiskResult {
  overall_risk: number;
  severity: "low" | "medium" | "high";
  warnings: string[];
  recommended_action: string;
}

export interface EvaluationResponse {
  observation: Observation;
  physics: PhysicsEstimate;
  risk: RiskResult;
  evaluated_at: string;
}

export interface BuildRecord {
  id: string;
  machine_id: string;
  material: string;
  layer_count: number;
  completed_layers: number;
  status: string;
}

export interface OptimizationCandidate {
  laser_power_w: number;
  scan_speed_mm_s: number;
  hatch_spacing_mm: number;
  layer_thickness_mm: number;
  predicted_energy_j_mm3: number;
  objective: number;
}

export interface StreamPacket {
  sequence: number;
  observed_at: string;
  observation: Observation;
  physics: PhysicsEstimate;
}

export const defaultObservation: Observation = {
  material: "Ti6Al4V",
  layer_number: 1253,
  laser_power_w: 275,
  scan_speed_mm_s: 1100,
  hatch_spacing_mm: 0.105,
  layer_thickness_mm: 0.04,
  oxygen_ppm: 95,
  chamber_temp_c: 38,
  melt_pool_intensity: 0.72,
  recoater_force_n: 13,
  gas_flow_m_s: 2.4,
  powder_d50_um: 33,
  scan_rotation_deg: 67,
};
