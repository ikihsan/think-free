<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-08
-->

# Raw data provenance

Berka dataset (PKDD'99 Discovery Challenge), real anonymized Czech retail-bank
transactions 1993–1998. Original release: `relational.fel.cvut.cz` (Berka,
1999). Retrieved 2026-10-08 from a GitHub mirror of the original tables
(`fenil264/berka-credit-risk`, path `data/raw/`), which carries the same row
counts as the original release (trans: 1,056,320 rows; account: 4,500 rows).

| file | sha256 | bytes |
|---|---|---|
| `trans.csv` | `111c70dc6626411d1d6547245c318b507e0c2892093f092d579468b71619bd3e` | 68,350,257 |
| `account.csv` | `215f4bfcb2520ab8d41154f22b5b294050cc142bb0c7362b05ab6da4742432eb` | 150,855 |

Retrieval command:

```bash
curl -sL -o raw/trans.csv \
  https://raw.githubusercontent.com/fenil264/berka-credit-risk/main/data/raw/trans.csv
curl -sL -o raw/account.csv \
  https://raw.githubusercontent.com/fenil264/berka-credit-risk/main/data/raw/account.csv
```

k_symbol vocabulary used by the protocol (from the dataset's own
documentation): `POJISTNE` insurance, `SIPO` household, `LEASING` leasing,
`UVER` loan payment, `SLUZBY` statement-for-payment fee, `UROK` interest,
`SANKC. UROK` sanction interest, `DUCHOD` old-age pension. `type`:
`PRIJEM` credit, `VYDAJ`/`VYBER` debit.

The raw CSVs are raw machine-consumed data, exempt from the line cap like
other raw captures; they are not republished (internal by default per
`RELEASE-MANIFEST.md`).
