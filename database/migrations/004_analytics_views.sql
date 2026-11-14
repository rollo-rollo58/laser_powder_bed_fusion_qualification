BEGIN;
CREATE OR REPLACE VIEW build_layer_energy AS
SELECT
  build_id,
  layer_number,
  COUNT(*) AS sample_count,
  AVG(laser_power_w / NULLIF(scan_speed_mm_s * hatch_spacing_mm *
                            layer_thickness_mm, 0)) AS mean_energy_j_mm3,
  MAX(oxygen_ppm) AS peak_oxygen_ppm,
  AVG(recoater_force_n) AS mean_recoater_force_n
FROM observations
GROUP BY build_id, layer_number;
CREATE OR REPLACE VIEW build_quality_rollup AS
SELECT
  b.id AS build_id,
  b.machine_id,
  b.status,
  COUNT(DISTINCT o.layer_number) AS layers_with_telemetry,
  COUNT(DISTINCT d.id) AS flagged_defect_count,
  COALESCE(MAX(d.risk_score), 0) AS maximum_defect_risk
FROM builds AS b
LEFT JOIN observations AS o ON o.build_id = b.id
LEFT JOIN layer_defects AS d ON d.build_id = b.id
GROUP BY b.id, b.machine_id, b.status;
INSERT INTO material_lots (
  material_code, lot_number, d10_um, d50_um, d90_um, oxygen_ppm
) VALUES
  ('Ti6Al4V', 'SYN-TI-001', 18.0, 34.0, 49.0, 145.0),
  ('Inconel718', 'SYN-IN-001', 17.0, 32.0, 48.0, 120.0),
  ('AlSi10Mg', 'SYN-AL-001', 16.0, 31.0, 46.0, 205.0)
ON CONFLICT (lot_number) DO NOTHING;
COMMIT;
