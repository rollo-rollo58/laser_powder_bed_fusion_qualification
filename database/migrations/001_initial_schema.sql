BEGIN;
CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS material_lots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  material_code VARCHAR(48) NOT NULL,
  lot_number VARCHAR(80) NOT NULL UNIQUE,
  d10_um NUMERIC(10, 3) NOT NULL CHECK (d10_um > 0),
  d50_um NUMERIC(10, 3) NOT NULL CHECK (d50_um > 0),
  d90_um NUMERIC(10, 3) NOT NULL CHECK (d90_um > 0),
  oxygen_ppm NUMERIC(12, 3) NOT NULL CHECK (oxygen_ppm >= 0),
  received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CHECK (d10_um <= d50_um AND d50_um <= d90_um)
);
CREATE TABLE IF NOT EXISTS builds (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  machine_id VARCHAR(90) NOT NULL,
  lot_id UUID NOT NULL REFERENCES material_lots(id),
  label VARCHAR(120) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued', 'preflight', 'printing', 'cooldown',
                      'inspection', 'qualified', 'rejected')),
  layer_count INTEGER NOT NULL CHECK (layer_count BETWEEN 1 AND 50000),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  version INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_builds_status_created ON builds(status, created_at DESC);
CREATE INDEX idx_builds_machine ON builds(machine_id);
CREATE TABLE IF NOT EXISTS observations (
  id BIGSERIAL PRIMARY KEY,
  build_id UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  layer_number INTEGER NOT NULL CHECK (layer_number > 0),
  laser_power_w NUMERIC(12, 4) NOT NULL CHECK (laser_power_w > 0),
  scan_speed_mm_s NUMERIC(12, 4) NOT NULL CHECK (scan_speed_mm_s > 0),
  hatch_spacing_mm NUMERIC(10, 5) NOT NULL CHECK (hatch_spacing_mm > 0),
  layer_thickness_mm NUMERIC(10, 5) NOT NULL CHECK (layer_thickness_mm > 0),
  oxygen_ppm NUMERIC(12, 3) NOT NULL CHECK (oxygen_ppm >= 0),
  chamber_temp_c NUMERIC(10, 3) NOT NULL,
  melt_pool_intensity NUMERIC(10, 6) NOT NULL,
  recoater_force_n NUMERIC(12, 3) NOT NULL,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_observations_build_layer ON observations(build_id, layer_number);
CREATE INDEX idx_observations_time ON observations(recorded_at DESC);
COMMIT;
