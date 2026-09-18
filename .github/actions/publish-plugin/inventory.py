"""Plan current packages plus reviewed historical versions; no registry writes."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def identity(path, ref):
    for manifest in (".tessl-plugin/plugin.json", "tile.json"):
        result = subprocess.run(["git", "show", f"{ref}:{path}/{manifest}"], capture_output=True, text=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if not re.fullmatch(r"[a-z0-9_-]+/[a-z0-9_-]+", data["name"]):
                raise ValueError(f"Invalid package name in {path}")
            if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?", data["version"]):
                raise ValueError(f"Invalid package version in {path}")
            return {"path": path, "ref": ref, "name": data["name"], "version": data["version"]}
    raise ValueError(f"No package manifest: {path} at {ref}")


def inventory(root, selected, manual, backfills):
    head = git("rev-parse", "HEAD")
    packages = []
    for directory in sorted(Path(root).iterdir()):
        path = directory.as_posix()
        if not directory.is_dir() or (directory / ".local-only").exists():
            continue
        if not any((directory / p).is_file() for p in (".tessl-plugin/plugin.json", "tile.json")):
            continue
        if selected and path != selected:
            continue
        if path in manual and not selected:
            continue
        packages.append(identity(path, head))
    if selected and not packages:
        raise ValueError(f"Selected package is absent, local-only, or outside {root}: {selected}")
    for entry in backfills:
        if selected and entry["path"] != selected:
            continue
        if not re.fullmatch(r"[a-f0-9]{40}", entry["ref"]):
            raise ValueError("Backfill source must be a full commit SHA")
        subprocess.run(["git", "merge-base", "--is-ancestor", entry["ref"], head], check=True)
        current = next((p for p in packages if p["path"] == entry["path"]), None)
        if current is None:
            raise ValueError("Backfills must belong to a current, publishable package")
        historical = identity(entry["path"], entry["ref"])
        if historical["name"] != current["name"] or historical["version"] != entry["version"]:
            raise ValueError("Backfill identity does not match its reviewed source")
        if historical["version"] != current["version"]:
            packages.append(historical)
    identities = [(p["name"], p["version"]) for p in packages]
    if len(identities) != len(set(identities)):
        raise ValueError("Duplicate package versions in publication plan")
    return packages


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--package", default="")
    parser.add_argument("--manual", action="append", default=[])
    parser.add_argument("--backfills")
    args = parser.parse_args()
    backfills = json.loads(Path(args.backfills).read_text()) if args.backfills else []
    print(json.dumps(inventory(args.root, args.package, args.manual, backfills), separators=(",", ":")))
