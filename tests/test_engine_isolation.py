import subprocess
import sys
from pathlib import Path

HEAVY_MODULES = ["sqlalchemy", "fastapi", "pydantic", "starlette"]


def test_engine_modules_do_not_import_the_web_or_database_stack():
    project_root = Path(__file__).resolve().parent.parent
    engine_dir = project_root / "app" / "engine"
    modules = sorted(
        f"app.engine.{path.stem}"
        for path in engine_dir.glob("*.py")
        if path.stem != "__init__"
    )
    script = (
        "import sys\n"
        + "".join(f"import {module}\n" for module in modules)
        + f"print(sorted(m for m in {HEAVY_MODULES!r} if m in sys.modules))\n"
    )

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=project_root,
        capture_output=True,
        text=True,
    )

    assert "app.engine.two_opt" in modules
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "[]"
