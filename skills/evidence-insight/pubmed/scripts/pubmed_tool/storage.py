from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def write_json(path: Path, value: Any) -> None:
    atomic_write(
        path, (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    body = "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in values)
    atomic_write(path, body.encode("utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()
