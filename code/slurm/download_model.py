#!/usr/bin/env python3
"""Download Qwen to the path used by its inference configuration."""

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from model.model_config_qwen import MODEL_CONFIG


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    destination = Path(MODEL_CONFIG["local_path"])
    if args.dry_run:
        print(MODEL_CONFIG["model_id"], destination)
        return 0
    from huggingface_hub import snapshot_download
    destination.mkdir(parents=True, exist_ok=True)
    path = snapshot_download(repo_id=MODEL_CONFIG["model_id"], local_dir=str(destination))
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

