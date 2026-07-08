from pathlib import Path


def test_no_private_markers_or_workflows():
    root = Path(__file__).resolve().parents[1]
    assert not (root / ".github" / "workflows").exists()
    skipped_dirs = {".git", "__pycache__", ".pytest_cache", "build", "dist"}
    forbidden = [
        "Her" + "mes",
        "Fei" + "shu",
        "/" + "home" + "/" + "xjyin",
        "/" + "mnt" + "/" + "c",
    ]
    for path in root.rglob("*"):
        if path.is_file() and not skipped_dirs.intersection(path.parts):
            if any(part.endswith(".egg-info") for part in path.parts):
                continue
            if path.suffix in {".py", ".md", ".toml", ".json", ".html", ".txt"} or path.name == "LICENSE":
                text = path.read_text(encoding="utf-8", errors="ignore")
                for marker in forbidden:
                    assert marker not in text, f"{marker} found in {path.relative_to(root)}"
