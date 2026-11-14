# Laser Powder-Bed Fusion: Build Qualification Workbench

A full-stack research and process-development application for laser powder-bed fusion
(LPBF) of metallic feedstock. The workspace visualizes layer thermal conditions,
recoater health, melt-pool proxies, powder lot properties, build qualification gates,
and an append-only simulated audit trail. Synthetic example inputs are provided.

## Boundaries and intended use

The process envelope and generated policy coefficients are **synthetic**, not
experimentally calibrated. This software is not a certified machine controller,
not an accepted ASTM/ISO qualification procedure, and not a substitute for in-situ
metrology, microscopy, validated process maps, or qualified materials engineers.
Any real build, airworthiness, medical-device or safety-critical decision must use
instrument-validated data, applicable standards, and independent engineering review.

## Architecture

- FastAPI with Pydantic v2 request and response schemas.
- A stateless calculation core with process physics proxy equations.
- SQLAlchemy 2 asynchronous-compatible models and transaction-oriented repository.
- WebSocket telemetry broadcaster with bounded client queues.
- Next.js App Router, React 19, TypeScript, Tailwind 3 UI; native SVG visualizations.
- PostgreSQL data model with four numbered SQL migrations.
- Docker Compose development stack; Kubernetes/monitoring/CI manifests.
- 5,000+ distinct *synthetic executable process policy functions*, distributed among
  domain modules. This sizeable catalogue is generated, not independently validated.

## Domain mathematics

Volumetric energy density (J/mm^3) = laser power (W) / (scan speed (mm/s) ×
 hatch spacing (mm) × layer thickness (mm)). Line energy (J/mm) = power / speed.
Thermal exposure and melt-pool width are illustrative bounded surrogate estimates,
not high-fidelity melt-fluid or radiation transfer solvers. Risk scores combine
normalized energy excursions, powder chemistry proxies, gas-flow conditions, and
recoater force. They are qualitative research outputs, not measured defect rates.

## API routes

- `GET /health` service health and schema version.
- `GET /api/v1/materials` available material envelopes.
- `GET /api/v1/builds` research build records.
- `POST /api/v1/evaluate` validate observation, estimate metrics, assign risk.
- `POST /api/v1/optimize` bounded candidate-grid process parameter search.
- `GET /api/v1/qualification/{build_id}` build gate checklist.
- `GET /api/v1/events` inspect bounded audit events.
- `WS /ws/telemetry` synthetic live process measurements and alerts.

## Local setup

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -e 'backend[dev]'
uvicorn app.main:app --app-dir backend --reload --port 8000
```

In a second terminal:

```sh
cd frontend
npm install
npm run dev
```

Frontend defaults to `http://localhost:8000`; set `NEXT_PUBLIC_API_URL` in the
shell or a private untracked local environment configuration if necessary.
Never commit actual secrets. `/docs` provides the OpenAPI console.

Run backend checks with `pytest -q backend/tests`. SQL migration scripts are
applied in numeric order to a fresh PostgreSQL database for integration tests.
The `docker-compose.yml` is a convenience demonstration, not hardened deployment.

## Repository navigation

`backend/app/physics.py` computes melt pool proxies; `risk.py` scores defects;
`optimizer.py` explores bounded settings; `state_machine.py` handles the
qualification workflow; `calibration.py` holds synthetic rule sets. The other
rule-bearing modules contain generated research policy families. The frontend
components demonstrate independent visual workflows and event controls.

## Trust and verification

The builder verifies file and line counts, allowed extensions, ZIP CRC integrity,
restricted path exclusions, basic secret patterns, Python AST syntax, and source
line widths. Integration tests, real sensor commissioning, independent validation,
benchmarking and threat modeling are **not completed** by these checks.
