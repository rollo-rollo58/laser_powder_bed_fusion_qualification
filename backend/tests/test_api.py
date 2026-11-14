"""HTTP contract checks exercising validation and error paths."""
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_available_materials():
    response = client.get("/api/v1/materials")
    assert "Ti6Al4V" in response.json()["materials"]


def test_evaluation_nominal():
    response = client.post("/api/v1/evaluate", json={"material": "Ti6Al4V"})
    assert response.status_code == 200
    assert 0 <= response.json()["risk"]["overall_risk"] <= 1


def test_evaluation_rejects_invalid_inputs():
    response = client.post("/api/v1/evaluate", json={"scan_speed_mm_s": -200})
    assert response.status_code == 422


def test_optimization_contract():
    response = client.post("/api/v1/optimize", json={"target_energy_j_mm3": 65})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_qualification_not_found():
    response = client.get("/api/v1/qualification/unknown")
    assert response.status_code == 404


def test_demo_builds():
    response = client.get("/api/v1/builds")
    assert response.status_code == 200
    assert len(response.json()) == 2
