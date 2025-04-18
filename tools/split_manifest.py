# split_and_manifest.py
import os
import json
import hashlib
import sys

SOURCE_DIR = "files"

# Optional folder path from CLI argument
try:
    SOURCE_DIR = sys.argv[1]
except IndexError:
    pass

TARGET_PART_SIZE = 80 * 1024 * 1024  # 80MB


def hash_file_part(path):
    """Returns the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def split_file(filepath, part_size=TARGET_PART_SIZE):
    """Splits a file into chunks and returns their metadata."""
    parts = []
    file_size = os.path.getsize(filepath)
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        index = 1
        while True:
            chunk = f.read(part_size)
            if not chunk:
                break
            part_filename = f"{filename}.part{index:02d}"
            part_path = os.path.join(SOURCE_DIR, part_filename)
            with open(part_path, "wb") as pf:
                pf.write(chunk)
            parts.append(
                {
                    "filename": part_filename,
                    "hash": hash_file_part(part_path),
                }
            )
            print(f"✓ Part created: {part_filename}")
            index += 1

    return parts, file_size


def create_manifest(file_path, parts, original_size):
    """Creates a manifest JSON file containing file metadata."""
    filename = os.path.basename(file_path)
    manifest = {
        "file": filename,
        "original_size": original_size,
        "part_size": TARGET_PART_SIZE,
        "parts": parts,
    }
    manifest_path = f"{file_path}.manifest.json"
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)
    print(f"✓ Manifest created: {manifest_path}")


def process_all():
    """Processes all eligible files in the source directory."""
    for file in os.listdir(SOURCE_DIR):
        full_path = os.path.join(SOURCE_DIR, file)
        if not os.path.isfile(full_path):
            continue
        if file.endswith(".manifest.json") or ".part" in file:
            continue

        if file.lower().endswith(".pk2"):
            parts, size = split_file(full_path)
        else:
            # Single-part hash (e.g. .dll or .exe)
            hash_val = hash_file_part(full_path)
            parts = [{"filename": file, "hash": hash_val}]
            size = os.path.getsize(full_path)

        create_manifest(full_path, parts, size)


if __name__ == "__main__":
    process_all()
