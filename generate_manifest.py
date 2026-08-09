#!/usr/bin/env python3
"""
Scans the /screenshots folder and writes manifest.json listing every
image file along with the date/time it was first added to the repo
(taken from git history), so the website can show "Uploaded: <date>"
without any manual editing.
"""

import datetime
import json
import os
import subprocess

SCREENSHOTS_DIR = "screenshots"
MANIFEST_PATH = "manifest.json"
VALID_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def get_first_commit_date(filepath):
    """Return the ISO 8601 date the file was first added (git log, oldest match)."""
    result = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%aI", "--", filepath],
        capture_output=True,
        text=True,
        check=False,
    )
    dates = [line for line in result.stdout.strip().split("\n") if line]
    if dates:
        return dates[-1]  # git log lists newest first, so the last line is the earliest
    return None


def get_fallback_date(filepath):
    """If the file isn't in git history yet (e.g. local run), fall back to file mtime."""
    mtime = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(mtime).astimezone().isoformat()


def main():
    entries = []

    if os.path.isdir(SCREENSHOTS_DIR):
        for filename in sorted(os.listdir(SCREENSHOTS_DIR)):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in VALID_EXTENSIONS:
                continue

            filepath = os.path.join(SCREENSHOTS_DIR, filename)
            uploaded_at = get_first_commit_date(filepath) or get_fallback_date(filepath)

            entries.append({"file": filename, "uploadedAt": uploaded_at})

    with open(MANIFEST_PATH, "w") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(entries)} entries to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
