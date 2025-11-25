import subprocess
from pathlib import Path


def save_tests(tests_dir: str, tests: dict):
    """
    Save generated Robot Framework files into a local /tests directory.
    """
    root = Path(tests_dir)
    root.mkdir(parents=True, exist_ok=True)

    saved = []

    for filename, content in tests.items():
        # Ensure the filename ends with .robot
        if not filename.endswith(".robot"):
            filename = filename + ".robot"

        outpath = root / filename
        outpath.parent.mkdir(parents=True, exist_ok=True)
        outpath.write_text(content, encoding="utf-8")

        saved.append(str(outpath))

    return saved


def run_robot(tests_dir: str):
    """
    Run Robot Framework *inside* the /tests directory.
    Example:
        robot .
    """
    proc = subprocess.run(
        ["robot", "."],
        cwd=tests_dir,
        capture_output=True,
        text=True
    )

    return {
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returncode": proc.returncode
    }
