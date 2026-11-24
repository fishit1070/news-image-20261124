#!/usr/bin/env python3
"""Deterministic artwork copier for the news-image-20261124 entry.

The finished page -- one picture summing up Tuesday 24 November 2026 --
is stored in this repository as plain data in ``art.png``, right beside
this script. There is nothing to render at run time: the artwork was
produced once, checked, and frozen as bytes.

Running this program therefore does exactly one thing: it copies those
bytes, unchanged, to ``entry.png`` inside the output directory. The
output directory comes from the ``MAKEFUN_OUTPUT_DIR`` environment
variable and falls back to ``/output`` when the variable is unset.

Because the program only ever copies a fixed file, two runs always
produce byte-identical output.
"""

import os
import shutil
import sys

# The artwork lives next to this script, wherever the repo is checked out.
HERE = os.path.dirname(os.path.abspath(__file__))
ARTWORK = os.path.join(HERE, "art.png")

# Name the grader expects inside the output directory.
OUTPUT_FILENAME = "entry.png"


def resolve_output_dir() -> str:
    """Return the directory the entry image should be written to."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main() -> int:
    if not os.path.isfile(ARTWORK):
        print(f"error: artwork file not found: {ARTWORK}", file=sys.stderr)
        return 1

    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)

    target = os.path.join(out_dir, OUTPUT_FILENAME)
    shutil.copyfile(ARTWORK, target)

    source_size = os.path.getsize(ARTWORK)
    copied_size = os.path.getsize(target)
    if copied_size != source_size:
        print(f"error: copy verification failed: wrote {copied_size} bytes, expected {source_size}", file=sys.stderr)
        return 1

    print(f"copied {ARTWORK} -> {target} ({copied_size} bytes, verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
