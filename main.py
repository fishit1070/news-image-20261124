"""Copy the bundled art.png into the make.fun output directory.

The finished image ships in this repository as ``art.png`` next to
this script. The grader expects it as ``entry.png`` inside the
directory named by MAKEFUN_OUTPUT_DIR (falling back to "/output").
The copy is byte-for-byte, so repeated runs are identical.
"""

import os
import shutil
import sys


def main() -> int:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, "art.png")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    destination = os.path.join(output_dir, "entry.png")
    if not os.path.exists(source):
        print(f"Error: source file not found: {source}", file=sys.stderr)
        return 1
    shutil.copyfile(source, destination)
    source_size = os.path.getsize(source)
    destination_size = os.path.getsize(destination)
    if destination_size != source_size:
        print(
            f"Error: copied size mismatch: {destination} is "
            f"{destination_size} bytes, expected {source_size} bytes",
            file=sys.stderr,
        )
        return 1
    print(f"Copied {source} to {destination} ({source_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
