BEGIN;
CREATE TABLE IF NOT EXISTS qualification_gates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  build_id UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  gate_code VARCHAR(48) NOT NULL,
  state VARCHAR(32) NOT NULL DEFAULT 'pending'
    CHECK (state IN ('pending', 'passed', 'failed', 'waived')),
  evidence_uri TEXT,
  reviewed_by TEXT,
  reviewed_at TIMESTAMPTZ,
  UNIQUE (build_id, gate_code)
);
CREATE TABLE IF NOT EXISTS layer_defects (
  id BIGSERIAL PRIMARY KEY,
  build_id UUID NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
  layer_number INTEGER NOT NULL CHECK (layer_number > 0),
  defect_kind VARCHAR(50) NOT NULL,
  risk_score NUMERIC(8, 6) NOT NULL CHECK (risk_score BETWEEN 0 AND 1),
  point_x_mm NUMERIC(10, 4) NOT NULL,
  point_y_mm NUMERIC(10, 4) NOT NULL,
  discovered_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_defects_build_kind ON layer_defects(build_id, defect_kind);
CREATE INDEX idx_gates_state ON qualification_gates(state);
COMMIT;
