"""Byte-level attribution for two zip artifacts.

The question this answers is causal, not correlational: if I rewrite only the
DOS date/time fields of artifact A to artifact B's values and the result is
byte-identical to B, then every differing byte was a timestamp byte. Anything
that survives that patch is a cause other than timestamps, which is exactly what
a "timestamps are worth fixing first" claim has to be able to survive.

Standard library only. Imported by `attribute.py`; not meant to be run directly.

Where the timestamp bytes are, from the PKWARE APPNOTE layout:

  local file header   PK\\x03\\x04  ... 10: mod time (2)  12: mod date (2)
  central directory   PK\\x01\\x02  ... 12: mod time (2)  14: mod date (2)

Central-directory records are walked sequentially from `ZipFile.start_dir`
rather than by scanning for signatures, because the signature bytes can occur
inside compressed data and a scan would attribute bytes to the wrong entry.
"""

from __future__ import annotations

import struct
import zipfile

LOCAL_SIG = b"PK\x03\x04"
CENTRAL_SIG = b"PK\x01\x02"
LOCAL_TIME_OFFSET = 10
CENTRAL_TIME_OFFSET = 12
TIME_LEN = 4  # two-byte DOS time followed by two-byte DOS date


def _central_offsets(raw: bytes, start_dir: int, count: int) -> list[int]:
    """Start offset of each central-directory record, walked in stored order."""
    offsets = []
    cursor = start_dir
    for _ in range(count):
        if raw[cursor:cursor + 4] != CENTRAL_SIG:
            raise ValueError(f"no central header at {cursor}")
        name_len, extra_len, comment_len = struct.unpack_from("<HHH", raw, cursor + 28)
        offsets.append(cursor)
        cursor += 46 + name_len + extra_len + comment_len
    return offsets


def timestamp_fields(raw: bytes) -> dict[str, list[tuple[int, int]]]:
    """Map each entry name to its (offset, length) timestamp fields.

    Two entries per name: the local file header and the central-directory
    record. Patching one half and not the other is the negative control, so both
    halves have to be locatable.
    """
    import io

    fields: dict[str, list[tuple[int, int]]] = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        central = _central_offsets(raw, archive.start_dir, len(infos))
        for info, central_at in zip(infos, central):
            local_at = info.header_offset
            fields[info.filename] = [
                (local_at + LOCAL_TIME_OFFSET, TIME_LEN),
                (central_at + CENTRAL_TIME_OFFSET, TIME_LEN),
            ]
    return fields


def read_stamps(raw: bytes) -> dict[str, list[bytes]]:
    """Each entry's timestamp field values, by name, for the patch target."""
    out = {}
    for name, positions in timestamp_fields(raw).items():
        out[name] = [raw[at:at + length] for at, length in positions]
    return out


def patch(raw: bytes, stamps: dict[str, list[bytes]], halves=("local", "central")) -> bytes:
    """Write `stamps` into `raw`'s timestamp fields, in place on a copy.

    `halves` selects which header gets written, so a caller can patch one half
    and assert that the result is *not* identical: that is the control proving
    the attribution can localise a cause rather than just detect a difference.
    """
    out = bytearray(raw)
    for name, positions in timestamp_fields(raw).items():
        if name not in stamps:
            raise KeyError(f"entry {name!r} is not in the patch target")
        for half, (at, length) in zip(("local", "central"), positions):
            if half not in halves:
                continue
            out[at:at + length] = stamps[name][0 if half == "local" else 1][:length]
    return bytes(out)


def differing_bytes(left: bytes, right: bytes) -> dict:
    """Count differing bytes, separating a length change from aligned content."""
    shared = min(len(left), len(right))
    mismatches = [i for i in range(shared) if left[i] != right[i]]
    return {
        "left_bytes": len(left),
        "right_bytes": len(right),
        "length_delta": len(right) - len(left),
        "differing_positions": len(mismatches),
        "tail_bytes": abs(len(right) - len(left)),
        "differing_bytes_total": len(mismatches) + abs(len(right) - len(left)),
        "positions": mismatches[:4096],
    }


def attribute(left: bytes, right: bytes) -> dict:
    """Split the difference between two artifacts into timestamp and other.

    Byte positions are classified against the timestamp fields of *both* sides,
    because a length change shifts every later offset and a position that is a
    timestamp in one artifact is not necessarily one in the other.
    """
    difference = differing_bytes(left, right)
    stamp_positions: set[int] = set()
    for raw in (left, right):
        try:
            fields = timestamp_fields(raw)
        except (ValueError, zipfile.BadZipFile):
            continue
        for positions in fields.values():
            for at, length in positions:
                stamp_positions.update(range(at, at + length))

    inside = sum(1 for i in difference["positions"] if i in stamp_positions)
    other_positions = difference["differing_positions"] - inside
    # A tail (length change) is never a timestamp field: the artifact structure
    # itself moved, which is a different kind of finding.
    other_total = other_positions + difference["tail_bytes"]
    total = difference["differing_bytes_total"]
    return {
        "left_sha256": _digest(left),
        "right_sha256": _digest(right),
        "differing_bytes_total": total,
        "differing_bytes_in_timestamp_fields": inside,
        "differing_bytes_other": other_total,
        "timestamp_share": round(inside / total, 6) if total else None,
        "identical": total == 0,
        "left_entries": _entries(left),
        "right_entries": _entries(right),
    }


def _digest(raw: bytes) -> str:
    import hashlib

    return hashlib.sha256(raw).hexdigest()


def _entries(raw: bytes) -> list[dict]:
    """Entry names, order, sizes and content hashes: the semantic layer.

    The byte layer says *how many* bytes a cause owns. This says *which file*
    a residual difference is in, which is the difference between a finding and a
    number.
    """
    import hashlib
    import io

    rows = []
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for index, info in enumerate(archive.infolist()):
            try:
                body = hashlib.sha256(archive.read(info)).hexdigest()
                error = None
            except (zipfile.BadZipFile, RuntimeError) as problem:
                body, error = None, f"{type(problem).__name__}"
            rows.append({
                "order": index,
                "name": info.filename,
                "size": info.file_size,
                "compressed_size": info.compress_size,
                "compress_type": info.compress_type,
                "content_sha256": body,
                "date_time": list(info.date_time),
                "read_error": error,
            })
    return rows


def residual_causes(left: dict, right: dict) -> list[dict]:
    """Per-entry differences that a timestamp patch cannot explain."""
    by_name_left = {row["name"]: row for row in left["left_entries"]}
    by_name_right = {row["name"]: row for row in right["right_entries"]}
    causes = []
    for name in sorted(set(by_name_left) | set(by_name_right)):
        a, b = by_name_left.get(name), by_name_right.get(name)
        if a is None:
            causes.append({"entry": name, "kind": "entry-only-in-second",
                           "detail": "present in the second artifact only"})
        elif b is None:
            causes.append({"entry": name, "kind": "entry-only-in-first",
                           "detail": "present in the first artifact only"})
        elif a["content_sha256"] != b["content_sha256"]:
            causes.append({
                "entry": name,
                "kind": "content-differs",
                "detail": f"sha256 {str(a['content_sha256'])[:12]} vs {str(b['content_sha256'])[:12]}",
            })
        elif a["compressed_size"] != b["compressed_size"] or a["compress_type"] != b["compress_type"]:
            causes.append({
                "entry": name,
                "kind": "compression-differs",
                "detail": f"{a['compress_type']}/{a['compressed_size']} vs "
                          f"{b['compress_type']}/{b['compressed_size']}",
            })
    orders_left = [row["name"] for row in left["left_entries"]]
    orders_right = [row["name"] for row in right["right_entries"]]
    if orders_left != orders_right and len(causes) == 0:
        causes.append({"entry": None, "kind": "entry-order-differs",
                       "detail": f"{orders_left[:4]} vs {orders_right[:4]}"})
    return causes