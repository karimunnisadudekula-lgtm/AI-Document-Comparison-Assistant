
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "AI-Document-Comparison-Submission.zip"

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

def should_include(path):
    relative = path.relative_to(ROOT)

    if any(part in EXCLUDED_DIRS for part in relative.parts):
        return False

    if path.name == ".env":
        return False

    if path.suffix.lower() in {".zip", ".bak", ".pyc"}:
        return False

    return True

files = [
    path for path in ROOT.rglob("*")
    if path.is_file()
    and path != OUTPUT
    and should_include(path)
]

with zipfile.ZipFile(
    OUTPUT, "w", compression=zipfile.ZIP_DEFLATED
) as archive:
    for path in files:
        archive.write(path, path.relative_to(ROOT))

print("Submission ZIP created:", OUTPUT.name)
print("Files included:", len(files))
print("ZIP size (MB):", round(OUTPUT.stat().st_size / 1048576, 2))
print("Contains .env:", any(
    name == ".env" for name in zipfile.ZipFile(OUTPUT).namelist()
))
