<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-14
-->

# E143 SOURCES — provenance of the Federal Register corpus

## Fetch parameters

| parameter | value |
|---|---|
| API endpoint | `https://www.federalregister.gov/api/v1/documents.json` |
| filter | `conditions[term]=final rule` |
| order | `newest` |
| per_page | 50 |
| pages | 1 |
| fields | `title`, `abstract`, `publication_date`, `document_number`, `raw_text_url` |
| fetch date | 2026-10-14 |

## Document digests

Each fetched document's raw text is stored in `raw/<document_number>.txt`.
The SHA-256 digests of the committed files are recorded below. Any change to
the raw files will be detected by `doc lint` or by re-running `fetch.py` and
comparing digests.

| document_number | sha256 |
|---|---|
| 2026-20889 | b4d7658cedcd1dcd17210ae1307ff233a929ff6378be82b0c41f0b0831897114 |
| 2026-20890 | 005a626148d703f9a09bf84e3dec774f61d6f58b69a765229fe7d554ec128848 |
| 2026-20894 | 6d96f145b40dcdee2f115fa624081dfa21182f2b74d8cbfdac95960fbf759158 |
| 2026-20903 | 79e4e11dafb2781e6e57af8729d405cc26741f6cbd7de20f347c85f377d30b26 |
| 2026-20904 | 22c7019841ce72ceea1862aaeeff8082fee3ef5be499adae34067eac8fe52805 |
| 2026-20930 | 22bf6c89e7c92eba5b74e4bd3d915ed302155425f5e780ca5c33f5880be0c960 |
| 2026-20932 | 4c5ea1c9787f440a11c69e306fb87b1e8525ed59c6f767db08b8f670436c9aab |
| 2026-20935 | 03f622e817c4bd29888ba86774da51c120d77856827be524f204a0acb78e5ebf |
| 2026-20941 | eeaea7e95203fc5672f74fa5dc771eca199f00cb541a5e4f01c61b4a84e38c77 |
| 2026-20942 | 08d096deee9462d3cd8918f0009d80298588fb75861c48d334e9b2efa754a2f3 |
| 2026-20943 | 411cf1dd77cf8297642d67cacffda68dd9a40c560cdc642f387d0cc2f2fa9da8 |
| 2026-20954 | 40c738be20a73ea7ad0c0b7953dc3694137d24612839638f9719972e924de7b4 |
| 2026-20955 | 73bdb6ef9302ec8e70fab6fcfc6c91b56b90ee6101b237f1777e50985a8599f7 |
| 2026-20956 | d6b8450532e314642ff342406038c2c39c868601cac6cb6ee01b5cb49b004d81 |
| 2026-20964 | be4f1f1e11af74411d7feeefcca68aa7d1d87ac6c1a68127332ae81f3ef1e4b0 |
| 2026-20970 | 8686170a757d61daf1c99f624840bfa7b907da0c9ebdc082c6b4acafb1890026 |
| 2026-20971 | 8ee0078ef1cbc02bd9da3c7dbd2b5356ea94f44b90eca00c8159faa432e14012 |
| 2026-20974 | 86b19610a180c46bbea6177105ebb58b5de075abef1c0f4b1156a0b1ca9902d9 |
| 2026-20982 | c4ad1a51087f07b8ca7e6e188d0e234b64ee279b6bd6eb7ea890f141af17e066 |
| 2026-20987 | 613125a9714a6a850780455ce885c222f88bbf4e0ff938695dd46138f8006da6 |
| 2026-20993 | f1997efa296c7384f838e8817e90c2a5114291d260c9280248849ec056c0434d |
| 2026-21004 | f6f3a72fb6d8eb34b899b0622352e4731dba6933df8758d29d33892b506ef0d3 |
| 2026-21009 | fef5a519e603980115d1b3abfb075b430c16055d2c4a4d08e06df4a0284bc05d |
| 2026-21010 | 395264f54a8acf3bdce3a436d7c25a736877f1b7636607f54d58be350358f9a7 |
| 2026-21019 | 60f3c21c633777f389ed06026e0aa11e7aba71d4fffbbdd6dc2a92476d0acdd6 |
| 2026-21020 | 66a9fe433d3df835334511dd2ec58f2025db167777a13e117c687174ebe2614e |
| 2026-21024 | 5e6f268a47a11441e484500a392dd988f1f2a9fa6a808ab42a1dee3d980949b2 |
| 2026-21030 | 63ff1235f3ed5d023e63da25a3dabd33c835ed6232860004c19fad3a91ac495c |
| 2026-21031 | aaf919adbb96355267990953453a921fd651234192f246a5b02ef9f8b8faea02 |

## Section structure verified

Before writing this protocol, the following section structure was verified on
a sample of fetched documents:

- `SUMMARY:` — the agency's plain-language summary (used in E142)
- `DATES:` — effective dates, comment deadlines
- `ADDRESSES:` — where to submit comments
- `FOR FURTHER INFORMATION CONTACT:` — agency contact
- `SUPPLEMENTARY INFORMATION:` — the agency's detailed explanation (used in E143)
- Then the CFR amendments (the actual regulatory text)

The `SUPPLEMENTARY INFORMATION:` section is the last major narrative section
before the CFR amendments. It is typically 10,000–500,000 characters.

## Population note

Only documents with a non-empty `abstract` field are fetched for full text.
The `abstract` field is populated for all final rules with a `SUMMARY` section,
which is the vast majority. Documents without `abstract` are skipped.

21 of 50 attempted documents failed due to API rate limits (HTTP 429).
The 29 successfully fetched documents constitute the corpus.