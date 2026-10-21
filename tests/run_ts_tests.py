"""Runs the TypeScript tests (tests/*.test.ts): bundles each with Remotion's own esbuild, then runs it with node.
Run: .venv\\Scripts\\python.exe tests\\run_ts_tests.py"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTION = ROOT / "remotion"
failed = 0
for test in sorted((ROOT / "tests").glob("*.test.ts")):
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "test.cjs"
        subprocess.run([shutil.which("npx"), "esbuild", str(test), "--bundle", "--platform=node", "--format=cjs",
                        f"--outfile={out}", "--log-level=error"], cwd=REMOTION, check=True)
        failed += subprocess.run(["node", str(out)], cwd=REMOTION).returncode != 0
sys.exit(1 if failed else 0)
