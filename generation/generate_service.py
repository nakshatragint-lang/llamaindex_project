from ingestion.clone import clone_repo
from .retriever import retrieve_chunks
from .test_generator import generate_tests
from .test_runner import save_tests, run_robot

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # project root
TESTS_DIR = BASE_DIR / "tests"
TESTS_DIR.mkdir(exist_ok=True)

def generate_service(prompt: str, repo_url: str = None):
    # repo_path = clone_repo(repo_url) if repo_url else tempfile.mkdtemp()

    # STEP 1: retrieve relevant chunks
    context = retrieve_chunks(prompt)

    # STEP 2: ask Groq
    tests = generate_tests(context, prompt)

    # STEP 3: save robot test files
    # tests_dir = Path("tests")
    # tests_dir.mkdir(exist_ok=True)

    saved_files = save_tests(str(TESTS_DIR), tests)

    # STEP 4: run tests
    out, err, rc = run_robot(str(TESTS_DIR))
    return {
        "saved_files": saved_files,
        "retrieved_context_preview": context[:1000],
        "robot_output": out[:20000],
        "robot_errors": err[:5000],
        "exit_code": rc
    }
