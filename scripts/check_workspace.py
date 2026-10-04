"""Validate the data manifest and optionally cached files; no network access."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


def check(manifest_path, cache_root, verify):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    folder = manifest.get("drive_folder_id")
    if folder is not None and (not isinstance(folder, str) or not folder.strip()):
        raise ValueError("drive_folder_id must be null or a nonempty string")
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise ValueError("files must be a list")
    seen = set()
    cache_root = cache_root.resolve()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("each file must be an object")
        name = entry.get("path")
        if not isinstance(name, str) or not name:
            raise ValueError("path must be a nonempty string")
        path = PurePosixPath(name)
        if path.is_absolute() or "\\" in name or any(p in ("", ".", "..") for p in name.split("/")):
            raise ValueError(f"unsafe relative path: {name}")
        if name in seen:
            raise ValueError(f"duplicate path: {name}")
        seen.add(name)
        for field in ("drive_file_id", "version"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                raise ValueError(f"{name}: {field} must be a nonempty string")
        digest = entry.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"{name}: invalid SHA-256")
        size = entry.get("size_bytes")
        if type(size) is not int or size < 0:
            raise ValueError(f"{name}: size_bytes must be a nonnegative integer")
        if verify:
            cached = (cache_root / name).resolve()
            if not cached.is_relative_to(cache_root):
                raise ValueError(f"{name}: cache path escapes root")
            if not cached.is_file() or cached.stat().st_size != size:
                raise ValueError(f"{name}: missing file or size mismatch")
            checksum = hashlib.sha256()
            with cached.open("rb") as source:
                for block in iter(lambda: source.read(1024 * 1024), b""):
                    checksum.update(block)
            if checksum.hexdigest() != digest:
                raise ValueError(f"{name}: SHA-256 mismatch")
    print(f"Manifest OK: {len(entries)} file(s)")
    if verify:
        print(f"Cache verified: {len(entries)} file(s)" if entries else "No data registered; cache transfer not validated")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/manifest.json")
    parser.add_argument("--cache-root", type=Path, default=ROOT / ".cache/data")
    parser.add_argument("--verify-cache", action="store_true")
    args = parser.parse_args()
    try:
        check(args.manifest, args.cache_root, args.verify_cache)
    except (OSError, ValueError) as error:
        print(f"Check failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
