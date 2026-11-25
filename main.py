"""Entry point for the news-image-20261124 make.fun submission.

The artwork for this entry is finished ahead of time and stored in the
repository as ``art.png``.  This script's only job is to deliver that
image to the grader: it copies ``art.png`` into the output directory
under the name ``entry.png``.  The copy is byte-for-byte identical, so
running the script any number of times always yields the same result.
"""

import os
import sys
from pathlib import Path

from copier import CopyVerificationError, deliver_artwork


def main() -> int:
    # Locate art.png relative to this script, not the working directory,
    # so the script behaves the same no matter where it is invoked from.
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "art.png")

    # The grader tells us where to write via MAKEFUN_OUTPUT_DIR; fall
    # back to the conventional "/output" location when it is not set.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    # The actual copy-and-verify work lives in copier.py; this entry
    # point only translates its outcome into messages and exit codes.
    try:
        size = deliver_artwork(Path(source), Path(out_dir))
    except FileNotFoundError:
        print(f"error: artwork file not found: {source}", file=sys.stderr)
        return 1
    except CopyVerificationError as exc:
        print(f"error: copy verification failed: {exc}", file=sys.stderr)
        return 1

    print(f"Copied {source} -> {target} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
