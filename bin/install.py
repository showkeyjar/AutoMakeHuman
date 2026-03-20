#!/usr/bin/env python3
import argparse
import shutil
from pathlib import Path


def copy_plugin(source_root: Path, target_root: Path, plugin_name: str) -> None:
    src = source_root / plugin_name
    dst = target_root / plugin_name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    print(f"Installed {plugin_name} -> {dst}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install AutoMakeHuman plugins into a MakeHuman plugins directory.")
    parser.add_argument("--target", required=True, help="Path to the MakeHuman plugins directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    source_root = repo_root / "src"
    target_root = Path(args.target).expanduser().resolve()
    target_root.mkdir(parents=True, exist_ok=True)

    for plugin_name in ("7_auto_human_body", "7_auto_human_pose"):
        copy_plugin(source_root, target_root, plugin_name)

    print("Installation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
