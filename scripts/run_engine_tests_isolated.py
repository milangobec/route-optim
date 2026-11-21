import sys
from pathlib import Path

sys.modules["sqlalchemy"] = None
sys.modules["fastapi"] = None

import pytest

WEB_AND_DB_TESTS = {
    "test_models.py",
    "test_stops_api.py",
    "test_routes_api.py",
    "test_app.py",
}

tests_dir = Path(__file__).resolve().parent.parent / "tests"
engine_tests = sorted(
    str(path)
    for path in tests_dir.glob("test_*.py")
    if path.name not in WEB_AND_DB_TESTS
)

sys.exit(pytest.main(["-q", "-p", "no:cacheprovider", *engine_tests]))
