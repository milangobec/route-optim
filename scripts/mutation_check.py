import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MUTATIONS = [
    (
        "2-opt swap range starts at index 0",
        "app/engine/two_opt.py",
        "range(1, len(best) - 1)",
        "range(0, len(best) - 1)",
    ),
    (
        "2-opt improvement tolerance removed",
        "app/engine/two_opt.py",
        " - IMPROVEMENT_TOLERANCE_KM",
        "",
    ),
    (
        "tie-break picks the stop nearer the centroid",
        "app/engine/nearest_neighbor.py",
        "next_stop = max(tied",
        "next_stop = min(tied",
    ),
    (
        "total_distance drops the return-to-depot leg",
        "app/engine/distance.py",
        "total += haversine_distance(ordered_stops[-1], ordered_stops[0])",
        "total += 0.0",
    ),
    (
        "wrong Earth radius",
        "app/engine/distance.py",
        "EARTH_RADIUS_KM = 6371.0",
        "EARTH_RADIUS_KM = 6378.0",
    ),
    (
        "compare_routes divide-by-zero guard removed",
        "app/engine/compare.py",
        "if naive_distance == 0:",
        "if False:",
    ),
]


def run_tests(workdir):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--tb=no",
            "-p",
            "no:cacheprovider",
            "tests",
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
    )
    lines = [line for line in result.stdout.strip().splitlines() if line.strip()]
    return result.returncode, lines[-1] if lines else ""


def main():
    ignore = shutil.ignore_patterns("__pycache__", ".pytest_cache")
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp) / "project"
        workdir.mkdir()
        shutil.copytree(PROJECT_ROOT / "app", workdir / "app", ignore=ignore)
        shutil.copytree(PROJECT_ROOT / "tests", workdir / "tests", ignore=ignore)
        shutil.copy(PROJECT_ROOT / "pyproject.toml", workdir / "pyproject.toml")

        code, summary = run_tests(workdir)
        if code != 0:
            print(f"Baseline suite fails, fix it first: {summary}")
            sys.exit(1)
        print(f"baseline: {summary}")

        survivors = 0
        for label, relative_path, old, new in MUTATIONS:
            target = workdir / relative_path
            original = target.read_text()
            if original.count(old) != 1:
                print(f"SKIPPED   {label}: expected exactly one match")
                survivors += 1
                continue

            target.write_text(original.replace(old, new))
            code, summary = run_tests(workdir)
            target.write_text(original)

            if code == 0:
                survivors += 1
            status = "caught" if code != 0 else "SURVIVED"
            print(f"{status:9} {label} ({summary})")

        print(f"{len(MUTATIONS) - survivors} of {len(MUTATIONS)} mutations caught")
        sys.exit(1 if survivors else 0)


if __name__ == "__main__":
    main()
