import os
import subprocess
import sys
from pathlib import Path


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_importing_app_does_not_create_database_file(tmp_path):
    project_root = Path(__file__).resolve().parent.parent
    result = subprocess.run(
        [sys.executable, "-c", "import app.main"],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(project_root)},
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert list(tmp_path.glob("*.db")) == []
