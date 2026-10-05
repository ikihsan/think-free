#!/usr/bin/env python3
"""E030 step 1 — harvest departure-framed HN comments and the control probes.

Writes, append-only:
  raw/fetch_log.jsonl   one row per HTTP request: framing, page, status, nbHits
  raw/harvest.jsonl     one row per comment body actually returned
  raw/probes.jsonl      gate A2 positive probes and A3 nonsense probes

Route every run through `tools/x --` so it is in the session record.
"""

import json
import os

import common as C

PAGES = 5
HITS = 100
MAX_PAGES = 1000 // HITS  # the API's own ceiling, recorded not exceeded


def harvest_framing(framing, fh_log, fh_out):
    """Fetch one framing's pages. Returns (comments, attempted, failures)."""
    comments = {}
    attempted = 0
    failures = 0
    for page in range(PAGES):
        status, data, raw = C.algolia_pages(C.phrase(framing), "comment", page, HITS)
        rec = {
            "kind": "framing",
            "framing": framing,
            "page": page,
            "status": status,
            "attempted_url_params": {"hitsPerPage": HITS, "page": page},
        }
        if data is None:
            rec["error"] = raw[:300]
            failures += 1
            C.log("fetch_failed", framing=framing, page=page, status=status)
            fh_log.write(json.dumps(rec, sort_keys=True) + "\n")
            fh_log.flush()
            continue
        rec["nbHits"] = data.get("nbHits")
        rec["nbPages"] = data.get("nbPages")
        rec["exhaustiveNbHits"] = data.get("exhaustiveNbHits")
        rec["api_ceiling_reached"] = data.get("nbPages", 0) > MAX_PAGES
        hits = data.get("hits", [])
        rec["hits_returned"] = len(hits)
        attempted += len(hits)
        fresh = []
        for hit in hits:
            oid = hit.get("objectID")
            if not oid or oid in comments:
                continue
            body = hit.get("comment_text") or hit.get("story_text") or ""
            comments[oid] = {
                "objectID": oid,
                "author": hit.get("author"),
                "story_id": hit.get("story_id"),
                "story_title": hit.get("story_title") or hit.get("title") or "",
                "parent_id": hit.get("parent_id"),
                "created_at": hit.get("created_at"),
                "created_at_i": hit.get("created_at_i"),
                "framing_first_seen": framing,
                "framing_hits": 1,
                "text": body,
            }
            fresh.append(comments[oid])
        # Write ONLY rows not yet written. The first version rewrote the whole
        # accumulated per-framing dict after every page, which put 1500 rows on
        # disk for a 500-row framing; the defect is recorded in AMENDMENT-3.
        for row in fresh:
            fh_out.write(json.dumps(row, sort_keys=True) + "\n")
        fh_out.flush()
        C.log("framing_page", framing=framing, page=page, hits=len(hits),
              fresh=len(fresh), nbHits=data.get("nbHits"),
              ceiling=rec["api_ceiling_reached"])
        fh_log.write(json.dumps(rec, sort_keys=True) + "\n")
        fh_log.flush()
    return list(comments.values()), attempted, failures


def harvest_probes(kind, probes, fh_log):
    """One page per probe. Used for gates A2 and A3."""
    out = []
    for probe in probes:
        status, data, raw = C.algolia_pages(C.phrase(probe), "comment", 0, HITS)
        hits = (data or {}).get("hits", [])
        out.append({"kind": kind, "probe": probe, "status": status,
                    "nbHits": (data or {}).get("nbHits"),
                    "accounts": len(hits)})
        C.log("probe", kind=kind, probe=probe, status=status,
              accounts=len(hits), nbHits=(data or {}).get("nbHits"))
        fh_log.write(json.dumps({"kind": "probe", "probe": probe, "probe_kind": kind,
                                 "status": status,
                                 "nbHits": (data or {}).get("nbHits")},
                                sort_keys=True) + "\n")
        fh_log.flush()
    return out


def main():
    os.makedirs(C.RAW, exist_ok=True)
    with open(os.path.join(C.RAW, "fetch_log.jsonl"), "w", encoding="utf-8") as fh_log, \
         open(os.path.join(C.RAW, "harvest.jsonl"), "w", encoding="utf-8") as fh_out:
        total = 0
        fail = 0
        attempts = 0
        for framing in C.FRAMINGS:
            rows, att, f = harvest_framing(framing, fh_log, fh_out)
            total += len(rows)
            attempts += att
            fail += f
            C.log("framing_done", framing=framing, comments=len(rows),
                  attempted=att, failed_pages=f)

        probes = harvest_probes("positive", C.POSITIVE_PROBES, fh_log)
        probes += harvest_probes("nonsense", C.NONSENSE_PROBES, fh_log)
        C.write_jsonl("probes.jsonl", probes)

    C.log("harvest_summary", comments=total, attempts=attempts, failed_pages=fail,
          framings=len(C.FRAMINGS), pages_each=PAGES)


if __name__ == "__main__":
    main()
