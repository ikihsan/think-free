<!-- origin-meta
owner: docs/INDEX.md
status: complete
last-verified: 2026-10-09
-->

# Raw data provenance

CFPB Consumer Complaint Database, the U.S. Consumer Financial Protection
Bureau's public bulk download. The database is the largest public corpus of
consumer financial complaints: 18M+ records, each a consumer complaint with the
company's response as its outcome field.

| file | sha256 | bytes | role |
|---|---|---|---|
| `complaints.csv.zip` | `d9ad58a54a55c8736169aeaa9c62dad981f2e628dc6f1cf36a4e5b6f47ac96e4` | 352,136,392 | the bulk archive, as published |
| `complaints.csv` | `3061ba8cf06dfdd8db40923356e939ed3fa3b7027417be99744e34e08fe001a7` | 5,538,368,989 | the 5.5 GB expanded archive |
| `cfpb_complaints.jsonl` | `33f7cf640c4fa1aaaa2e3eecd86ce3ac9b93cd7aa66be0aee33b84b8edf28524` | 6,229,804 | the 10,000-row deterministic sample `process_csv.py` wrote |

Retrieval and sample commands:

```bash
cd EXPERIMENTS/070-discourse-fresh-observation/raw
curl -sL -o complaints.csv.zip \
  https://files.consumerfinance.gov/ccdb/complaints.csv.zip
unzip complaints.csv.zip
python3 ../process_csv.py    # writes cfpb_complaints.jsonl
```

`cfpb_complaints.jsonl` carries the 14 fields the experiment reads plus two the
harvest computed: `outcome_class` (`served` / `unserved`, from the company's
`company_response`) and `view_count` (1 per complaint — the instrument of E062,
where one complaint is one arrival at a need). Row count 10,000; the row set is
the head of the published CSV, which is date-descending, so the sample is the
most recent complaints and not a random draw over the full history. **That is a
stated limitation, not a property of the measurement**: it is recorded here
because the whole archive cannot be reproduced by anyone who does not re-download
5.5 GB, and the hash fixes which bytes the result was derived from.

The two bulk files are raw machine-consumed third-party input, exempt from the
line cap like other raw captures, not tracked in git, and not republished
(internal by default per `RELEASE-MANIFEST.md`). The record is this table and
the sample file, by the same clause `.gitignore` applies to `sdists/` and to
E066's `raw/*.csv`.