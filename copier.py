"""Verified hand-off of the finished artwork for this entry.

The picture lives in the repository as ``art.png``; the grader expects
to receive it as ``entry.png`` inside a chosen output folder.  This
module performs that delivery and then proves it went well: a copy is
only accepted when both its length and its SHA-256 digest agree with
the original file.
"""

import hashlib
import shutil
from pathlib import Path


class CopyVerificationError(RuntimeError):
    """Raised when a copied file fails to match its source."""


def _digest(path: Path) -> str:
    """Stream the file at ``path`` through SHA-256; return the hex digest."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def deliver_artwork(art_path: Path, output_dir: Path) -> int:
    """Copy ``art_path`` into ``output_dir`` as ``entry.png``, verified.

    The output folder is created when it does not exist yet.  Once the
    bytes are written, the copy is compared with the source twice over
    — first by size, then by digest — and any disagreement raises
    :class:`CopyVerificationError`.  A missing source raises
    :class:`FileNotFoundError` before anything is written.  On success
    the number of bytes copied is returned.
    """
    source = Path(art_path)
    if not source.is_file():
        raise FileNotFoundError(f"artwork not found: {source}")

    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"

    shutil.copyfile(source, target)

    written = target.stat().st_size
    if written != source.stat().st_size:
        raise CopyVerificationError(
            f"size mismatch for {target}: got {written} bytes"
        )
    if _digest(target) != _digest(source):
        raise CopyVerificationError(f"digest mismatch for {target}")
    return written
