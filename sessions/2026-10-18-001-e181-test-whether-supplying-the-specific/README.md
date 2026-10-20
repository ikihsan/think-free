# Session 2026-10-18-001-e181-test-whether-supplying-the-specific

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-18
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `space-bunny-free`
- **Started:** 2026-10-18T00:24:58+00:00
- **Duration:** 3440.9s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

E181: test whether supplying the specific missing fact closes the 0.4000 evidence gap E177 measured, as a paired three-arm comparison on the same EVID rows

## Summary

E181 measured the mechanism F136 left open: does supplying the missing fact close the 0.4000 evidence gap? Four paired arms on E177's own EVID population, all answered and scored in one session with leak assertions on every input. Question alone 0.5000, + the extracted missing fact 0.5714, + the entire comment thread 0.6429, placebo 0.4000. Every paired comparison is null (exact McNemar p = 1.0) and floor-vs-whole-thread is 0 rows for and 2 against, so neither supplying the fact nor pasting the thread moves the rate: the elicitation route closes (D119, F139) and F136's population gap is left standing but unexplained. Two numbers survive the kill: an extracted fact is 6.7% of the thread's tokens, and the comments name the deciding fact on 14/30 = 0.4667 with 10 of 16 nulls carrying the remedy itself - so the round trip runs to the solution, not to the fact. G4 fired (the same reader disagreed with itself on 4 of 10 of E177's answers one day later), so no absolute level here is comparable with E177's. K1 fired, so no gate is evaluated and every arm is labelled exploratory. Repaired two evidence defects found on the way: .gitignore could not track EXPERIMENTS/*/raw/*.jsonl at all (109 files, 199 MB untracked, while two protocols promise an auditable capture) and E178's capture holds each comment_id up to three times.

## Next

Ask whether the accepted answer is the best answer or merely the accepted one: read the rows every arm in E181 missed and classify them. One reader, no new fetch, and it is the only explanation the EVID population has left - if the missed rows are contestable resolutions, the gap is a disagreement about answers and no context pipeline will close it.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md | fc7cf3e03579 | 4041 |
| EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md | c4427d5629de | 12764 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/01-79723342.txt | 639bcee3e505 | 2782 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/02-79408101.txt | 2fa7f8e7e5e4 | 2213 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/03-79556333.txt | b0bb8332d90e | 1437 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/04-79817405.txt | 3cce7227f2dc | 1856 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/05-79602687.txt | c7920252e0e2 | 4731 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/06-79843062.txt | 53d355d1df41 | 7829 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/07-79818015.txt | 6b26e972c4cf | 3063 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/08-79871713.txt | 6a2ee97e55f9 | 2127 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/09-79754247.txt | 09c03c668dd4 | 7194 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/10-79368095.txt | 55e3f2eb433a | 2076 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/11-79428308.txt | 3c5bc05b953b | 1672 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/12-79600161.txt | 287f95a5eeee | 6473 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/13-79791886.txt | 636181a8e8f9 | 11689 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/14-79718097.txt | 5519a44cb66a | 13024 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/15-79779187.txt | 74e657f32a3b | 3103 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/16-79380514.txt | a53bb9012152 | 5563 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/17-79335513.txt | 6dab040ab4d5 | 1582 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/18-79665976.txt | 7516d1a154d6 | 1029 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/19-79818917.txt | b05a9b324de9 | 1194 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/20-79663905.txt | 433427cc9a58 | 11943 |
| EXPERIMENTS/181-fact-supply-closes-gap/population.json | 3173a2199217 | 5636 |
| EXPERIMENTS/181-fact-supply-closes-gap/prep.py | 7fc649584119 | 9389 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md | fc7cf3e03579 | 4041 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-2.md | 45e4a5e17c8b | 4647 |
| EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md | c4427d5629de | 12764 |
| EXPERIMENTS/181-fact-supply-closes-gap/READER-INSTRUCTION.md | bd07af6bed83 | 2892 |
| EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md | 493d49eb22a9 | 10650 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-index.json | a5ff832f5199 | 5313 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/001.txt | 206934da2f9f | 2610 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/002.txt | 71f0511f28ce | 2798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/003.txt | 4ee564f2d3d4 | 3852 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/004.txt | fb776fa2a1de | 2731 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/005.txt | 5795d33b52c9 | 422 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/006.txt | 0154d6041731 | 543 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/007.txt | 71b612a44175 | 2956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/008.txt | 5303482ef022 | 529 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/009.txt | 557c3963eb4f | 1517 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/010.txt | 8da0f86c2287 | 1624 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/011.txt | ddebdecf53b1 | 2007 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/012.txt | 0441e24a5320 | 1638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/013.txt | da4d22f35245 | 1072 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/014.txt | 4c73e3784bd3 | 1193 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/015.txt | 59caf9c396f3 | 1568 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/016.txt | ff0549353d19 | 1195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/017.txt | 1286fbe3d6cd | 716 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/018.txt | 48a5d4388b86 | 839 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/019.txt | 88bcba1878be | 3063 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/020.txt | 6e27f4bffbe9 | 819 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/021.txt | 8f917abf9877 | 1508 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/022.txt | 384e8196b73c | 1611 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/023.txt | 78891ab3a189 | 5987 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/024.txt | 001d34b30d2f | 1722 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/025.txt | efa58bfad589 | 6992 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/026.txt | 51245729dc83 | 7206 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/027.txt | 57a368f6782a | 9689 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/028.txt | cf4c17efd1ce | 7103 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/029.txt | dd39d42061ea | 851 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/030.txt | ba58a9335cb0 | 962 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/031.txt | bd72c8637ca1 | 2652 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/032.txt | 4462012bc5be | 956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/033.txt | 032bfd08fa1b | 642 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/034.txt | 981dfcb1aa11 | 747 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/035.txt | 98441dedb80e | 915 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/036.txt | 94d444b70e7a | 754 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/037.txt | 98dec235e4cd | 4676 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/038.txt | b3ee11d4dfdc | 4788 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/039.txt | a336c1fa1e58 | 6978 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/040.txt | e8090663e80d | 4798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/041.txt | 0fbbb8a14511 | 638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/042.txt | 8bfa0f8ca673 | 760 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/043.txt | fa0d8c39ed4d | 2037 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/044.txt | 8f71471ba9d0 | 863 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/045.txt | cb57fc36c06d | 1045 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/046.txt | 929498439c73 | 6635 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/047.txt | 958f95d32ab5 | 914 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/048.txt | 3a92f5d06f11 | 1078 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/049.txt | dfd619ba7df7 | 1723 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/050.txt | 66f42db171d9 | 725 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/051.txt | 8ac3937427b6 | 848 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/052.txt | b13b3b81090f | 1547 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers-data.json | 19a33cf2a57b | 40381 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers.jsonl | e437e77187ca | 42242 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/01-79723342.txt | 09381ebc83b4 | 1938 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/02-79408101.txt | b1761f15d4e4 | 1701 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/03-79556333.txt | b0bb8332d90e | 1437 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/04-79817405.txt | 3cce7227f2dc | 1856 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/05-79602687.txt | e49315fa010c | 4013 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/06-79843062.txt | addcb2b9a6d5 | 3225 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/07-79818015.txt | 2558abe72964 | 2129 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/08-79871713.txt | 5eaae59108dd | 1757 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/09-79754247.txt | 944de4673cc5 | 3280 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/10-79368095.txt | 66d94cf93a0e | 1084 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/11-79428308.txt | 4d6abbb2509d | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/12-79600161.txt | e5678befe29e | 5219 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/13-79791886.txt | 87f8097bacbd | 6417 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/14-79718097.txt | 93b2cab9d6cb | 9874 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/15-79779187.txt | 0319f687130d | 2973 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/16-79380514.txt | 082e99016086 | 2843 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/17-79335513.txt | 7fcf160a2a1f | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/18-79665976.txt | 7516d1a154d6 | 1029 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/19-79818917.txt | b05a9b324de9 | 1194 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/20-79663905.txt | 3eebb6228ea0 | 7195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-21-79666817.txt | 7e46cc997301 | 7183 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-22-79385315.txt | be5412c3211e | 2256 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-23-79513015.txt | e05580d50849 | 2622 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-24-79776559.txt | 7a4dc9fb115e | 2221 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-25-79686551.txt | 110482758752 | 2282 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-26-79606837.txt | 68a557fa3306 | 7028 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-27-79358893.txt | 5a3419e9781c | 1104 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-28-79567126.txt | a2318bb5507f | 1850 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-29-79721071.txt | 2b3dd35294f6 | 1397 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-30-79339258.txt | f300635bf27f | 1752 |
| EXPERIMENTS/181-fact-supply-closes-gap/facts.jsonl | cfe3e947543c | 7080 |
| EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py | 4f6217f86af9 | 1947 |
| EXPERIMENTS/181-fact-supply-closes-gap/make_inputs.py | c142f995939d | 5402 |
| EXPERIMENTS/181-fact-supply-closes-gap/population.json | 8899012e14b7 | 8016 |
| EXPERIMENTS/181-fact-supply-closes-gap/prep.py | d22f7a75df2d | 10591 |
| EXPERIMENTS/181-fact-supply-closes-gap/raw/se.jsonl | cb1af9c0fc4d | 1292 |
| EXPERIMENTS/181-fact-supply-closes-gap/result.json | 93f3143b6014 | 2089 |
| EXPERIMENTS/181-fact-supply-closes-gap/score/001.txt | 39da0b2f39ca | 4728 |
| EXPERIMENTS/181-fact-supply-closes-gap/score/002.txt | ab317bb0b85f | 3428 |
| EXPERIMENTS/181-fact-supply-closes-gap/score/003.txt | 0c1a21e05a57 | 4730 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md | fc7cf3e03579 | 4041 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-2.md | 45e4a5e17c8b | 4647 |
| EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md | c4427d5629de | 12764 |
| EXPERIMENTS/181-fact-supply-closes-gap/READER-INSTRUCTION.md | bd07af6bed83 | 2892 |
| EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md | 493d49eb22a9 | 10650 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-index.json | a5ff832f5199 | 5313 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/001.txt | 206934da2f9f | 2610 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/002.txt | 71f0511f28ce | 2798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/003.txt | 4ee564f2d3d4 | 3852 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/004.txt | fb776fa2a1de | 2731 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/005.txt | 5795d33b52c9 | 422 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/006.txt | 0154d6041731 | 543 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/007.txt | 71b612a44175 | 2956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/008.txt | 5303482ef022 | 529 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/009.txt | 557c3963eb4f | 1517 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/010.txt | 8da0f86c2287 | 1624 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/011.txt | ddebdecf53b1 | 2007 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/012.txt | 0441e24a5320 | 1638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/013.txt | da4d22f35245 | 1072 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/014.txt | 4c73e3784bd3 | 1193 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/015.txt | 59caf9c396f3 | 1568 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/016.txt | ff0549353d19 | 1195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/017.txt | 1286fbe3d6cd | 716 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/018.txt | 48a5d4388b86 | 839 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/019.txt | 88bcba1878be | 3063 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/020.txt | 6e27f4bffbe9 | 819 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/021.txt | 8f917abf9877 | 1508 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/022.txt | 384e8196b73c | 1611 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/023.txt | 78891ab3a189 | 5987 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/024.txt | 001d34b30d2f | 1722 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/025.txt | efa58bfad589 | 6992 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/026.txt | 51245729dc83 | 7206 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/027.txt | 57a368f6782a | 9689 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/028.txt | cf4c17efd1ce | 7103 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/029.txt | dd39d42061ea | 851 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/030.txt | ba58a9335cb0 | 962 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/031.txt | bd72c8637ca1 | 2652 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/032.txt | 4462012bc5be | 956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/033.txt | 032bfd08fa1b | 642 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/034.txt | 981dfcb1aa11 | 747 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/035.txt | 98441dedb80e | 915 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/036.txt | 94d444b70e7a | 754 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/037.txt | 98dec235e4cd | 4676 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/038.txt | b3ee11d4dfdc | 4788 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/039.txt | a336c1fa1e58 | 6978 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/040.txt | e8090663e80d | 4798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/041.txt | 0fbbb8a14511 | 638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/042.txt | 8bfa0f8ca673 | 760 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/043.txt | fa0d8c39ed4d | 2037 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/044.txt | 8f71471ba9d0 | 863 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/045.txt | cb57fc36c06d | 1045 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/046.txt | 929498439c73 | 6635 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/047.txt | 958f95d32ab5 | 914 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/048.txt | 3a92f5d06f11 | 1078 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/049.txt | dfd619ba7df7 | 1723 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/050.txt | 66f42db171d9 | 725 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/051.txt | 8ac3937427b6 | 848 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/052.txt | b13b3b81090f | 1547 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers-data.json | 19a33cf2a57b | 40381 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers.jsonl | e437e77187ca | 42242 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/01-79723342.txt | 09381ebc83b4 | 1938 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/02-79408101.txt | b1761f15d4e4 | 1701 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/03-79556333.txt | b0bb8332d90e | 1437 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/04-79817405.txt | 3cce7227f2dc | 1856 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/05-79602687.txt | e49315fa010c | 4013 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/06-79843062.txt | addcb2b9a6d5 | 3225 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/07-79818015.txt | 2558abe72964 | 2129 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/08-79871713.txt | 5eaae59108dd | 1757 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/09-79754247.txt | 944de4673cc5 | 3280 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/10-79368095.txt | 66d94cf93a0e | 1084 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/11-79428308.txt | 4d6abbb2509d | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/12-79600161.txt | e5678befe29e | 5219 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/13-79791886.txt | 87f8097bacbd | 6417 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/14-79718097.txt | 93b2cab9d6cb | 9874 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/15-79779187.txt | 0319f687130d | 2973 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/16-79380514.txt | 082e99016086 | 2843 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/17-79335513.txt | 7fcf160a2a1f | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/18-79665976.txt | 7516d1a154d6 | 1029 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/19-79818917.txt | b05a9b324de9 | 1194 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/20-79663905.txt | 3eebb6228ea0 | 7195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-21-79666817.txt | 7e46cc997301 | 7183 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-22-79385315.txt | be5412c3211e | 2256 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-23-79513015.txt | e05580d50849 | 2622 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-24-79776559.txt | 7a4dc9fb115e | 2221 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md | fc7cf3e03579 | 4041 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-2.md | 45e4a5e17c8b | 4647 |
| EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md | c4427d5629de | 12764 |
| EXPERIMENTS/181-fact-supply-closes-gap/READER-INSTRUCTION.md | bd07af6bed83 | 2892 |
| EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md | 493d49eb22a9 | 10650 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-index.json | a5ff832f5199 | 5313 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/001.txt | 206934da2f9f | 2610 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/002.txt | 71f0511f28ce | 2798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/003.txt | 4ee564f2d3d4 | 3852 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/004.txt | fb776fa2a1de | 2731 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/005.txt | 5795d33b52c9 | 422 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/006.txt | 0154d6041731 | 543 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/007.txt | 71b612a44175 | 2956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/008.txt | 5303482ef022 | 529 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/009.txt | 557c3963eb4f | 1517 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/010.txt | 8da0f86c2287 | 1624 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/011.txt | ddebdecf53b1 | 2007 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/012.txt | 0441e24a5320 | 1638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/013.txt | da4d22f35245 | 1072 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/014.txt | 4c73e3784bd3 | 1193 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/015.txt | 59caf9c396f3 | 1568 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/016.txt | ff0549353d19 | 1195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/017.txt | 1286fbe3d6cd | 716 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/018.txt | 48a5d4388b86 | 839 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/019.txt | 88bcba1878be | 3063 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/020.txt | 6e27f4bffbe9 | 819 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/021.txt | 8f917abf9877 | 1508 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/022.txt | 384e8196b73c | 1611 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/023.txt | 78891ab3a189 | 5987 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/024.txt | 001d34b30d2f | 1722 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/025.txt | efa58bfad589 | 6992 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/026.txt | 51245729dc83 | 7206 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/027.txt | 57a368f6782a | 9689 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/028.txt | cf4c17efd1ce | 7103 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/029.txt | dd39d42061ea | 851 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/030.txt | ba58a9335cb0 | 962 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/031.txt | bd72c8637ca1 | 2652 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/032.txt | 4462012bc5be | 956 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/033.txt | 032bfd08fa1b | 642 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/034.txt | 981dfcb1aa11 | 747 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/035.txt | 98441dedb80e | 915 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/036.txt | 94d444b70e7a | 754 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/037.txt | 98dec235e4cd | 4676 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/038.txt | b3ee11d4dfdc | 4788 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/039.txt | a336c1fa1e58 | 6978 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/040.txt | e8090663e80d | 4798 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/041.txt | 0fbbb8a14511 | 638 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/042.txt | 8bfa0f8ca673 | 760 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/043.txt | fa0d8c39ed4d | 2037 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/044.txt | 8f71471ba9d0 | 863 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/045.txt | cb57fc36c06d | 1045 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/046.txt | 929498439c73 | 6635 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/047.txt | 958f95d32ab5 | 914 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/048.txt | 3a92f5d06f11 | 1078 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/049.txt | dfd619ba7df7 | 1723 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/050.txt | 66f42db171d9 | 725 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/051.txt | 8ac3937427b6 | 848 |
| EXPERIMENTS/181-fact-supply-closes-gap/ans-input/052.txt | b13b3b81090f | 1547 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers-data.json | 19a33cf2a57b | 40381 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers.jsonl | e437e77187ca | 42242 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/01-79723342.txt | 09381ebc83b4 | 1938 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/02-79408101.txt | b1761f15d4e4 | 1701 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/03-79556333.txt | b0bb8332d90e | 1437 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/04-79817405.txt | 3cce7227f2dc | 1856 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/05-79602687.txt | e49315fa010c | 4013 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/06-79843062.txt | addcb2b9a6d5 | 3225 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/07-79818015.txt | 2558abe72964 | 2129 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/08-79871713.txt | 5eaae59108dd | 1757 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/09-79754247.txt | 944de4673cc5 | 3280 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/10-79368095.txt | 66d94cf93a0e | 1084 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/11-79428308.txt | 4d6abbb2509d | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/12-79600161.txt | e5678befe29e | 5219 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/13-79791886.txt | 87f8097bacbd | 6417 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/14-79718097.txt | 93b2cab9d6cb | 9874 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/15-79779187.txt | 0319f687130d | 2973 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/16-79380514.txt | 082e99016086 | 2843 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/17-79335513.txt | 7fcf160a2a1f | 1322 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/18-79665976.txt | 7516d1a154d6 | 1029 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/19-79818917.txt | b05a9b324de9 | 1194 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/20-79663905.txt | 3eebb6228ea0 | 7195 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-21-79666817.txt | 7e46cc997301 | 7183 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-22-79385315.txt | be5412c3211e | 2256 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-23-79513015.txt | e05580d50849 | 2622 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-24-79776559.txt | 7a4dc9fb115e | 2221 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-25-79686551.txt | 110482758752 | 2282 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-26-79606837.txt | 68a557fa3306 | 7028 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-27-79358893.txt | 5a3419e9781c | 1104 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-28-79567126.txt | a2318bb5507f | 1850 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-29-79721071.txt | 2b3dd35294f6 | 1397 |
| EXPERIMENTS/181-fact-supply-closes-gap/ext/extra-30-79339258.txt | f300635bf27f | 1752 |
| EXPERIMENTS/181-fact-supply-closes-gap/facts.jsonl | cfe3e947543c | 7080 |
| EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py | 4f6217f86af9 | 1947 |
| EXPERIMENTS/181-fact-supply-closes-gap/RESULT.md | 493d49eb22a9 | 10650 |
| EXPERIMENTS/181-fact-supply-closes-gap/result.json | 93f3143b6014 | 2089 |
| EXPERIMENTS/181-fact-supply-closes-gap/verdicts.jsonl | a6908e068a7e | 8288 |
| EXPERIMENTS/181-fact-supply-closes-gap/facts.jsonl | cfe3e947543c | 7080 |
| EXPERIMENTS/181-fact-supply-closes-gap/answers.jsonl | e437e77187ca | 42242 |
| EXPERIMENTS/181-fact-supply-closes-gap/score.py | 6bed98628854 | 10528 |
| EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md | c4427d5629de | 12764 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md | fc7cf3e03579 | 4041 |
| EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-2.md | 45e4a5e17c8b | 4647 |
| EXPERIMENTS/181-fact-supply-closes-gap/READER-INSTRUCTION.md | bd07af6bed83 | 2892 |
| EXPERIMENTS/181-fact-supply-closes-gap/population.json | 8899012e14b7 | 8016 |
| FAILURES.md | f9edbeb31f8e | 101730 |
| FAILURES-findings-43.md | 0f2e71481615 | 12226 |
| FAILURES-findings-44.md | 7a0ace941bbe | 11999 |
| DECISIONS.md | 7c413b1a79ac | 29404 |
| DECISIONS-RECORDS-4.md | f77ddd24b4bb | 5159 |
| STATE.md | 10c5c1ae41bb | 25390 |
| STATE-next-actions.md | 06d3f6a8cc07 | 26535 |
| vendor/MANIFEST.md | 60eb821ce5a5 | 13952 |

## Commands

13 captured, 5 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/prep.py'] | 0 | 1913 |
| 3 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/prep.py'] | 1 | 2295 |
| 4 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/prep.py'] | 0 | 1889 |
| 29 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/prep.py'] | 0 | 2062 |
| 30 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py'] | 1 | 779 |
| 31 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py'] | 1 | 572 |
| 32 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py'] | 0 | 47 |
| 33 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py'] | 0 | 106 |
| 34 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/make_inputs.py'] | 0 | 259 |
| 35 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py'] | 1 | 581 |
| 36 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py'] | 0 | 189 |
| 37 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/score.py'] | 1 | 700 |
| 38 | ['python3', 'EXPERIMENTS/181-fact-supply-closes-gap/score.py'] | 0 | 188 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 131 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | .gitignore |
|   undeclared | EXPERIMENTS/065-view-count-prototype/raw/control-results.jsonl |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/account.csv |
|   undeclared | EXPERIMENTS/066-berka-real-validation/raw/trans.csv |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-a-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra-results.jsonl |
|   undeclared | EXPERIMENTS/071-pip-name-guard-prototype/raw/arm-b-extra2-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-a-results.jsonl |
|   undeclared | EXPERIMENTS/072-npm-view-count-prototype/raw/arm-b-results.jsonl |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 00:24:58 | session_start | E181: test whether supplying the specific missing fact closes the 0.4000 evidence gap E177 measured, as a paired three-arm comparison on the same EVID |
| 2 | 00:26:40 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/prep.py |
| 3 | 00:27:49 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/prep.py |
| 4 | 00:27:59 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/prep.py |
| 5 | 00:28:19 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md |
| 6 | 00:28:20 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/PROTOCOL.md |
| 7 | 00:28:21 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/01-79723342.txt |
| 8 | 00:28:22 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/02-79408101.txt |
| 9 | 00:28:23 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/03-79556333.txt |
| 10 | 00:28:24 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/04-79817405.txt |
| 11 | 00:28:25 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/05-79602687.txt |
| 12 | 00:28:26 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/06-79843062.txt |
| 13 | 00:28:28 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/07-79818015.txt |
| 14 | 00:28:29 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/08-79871713.txt |
| 15 | 00:28:30 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/09-79754247.txt |
| 16 | 00:28:31 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/10-79368095.txt |
| 17 | 00:28:32 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/11-79428308.txt |
| 18 | 00:28:33 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/12-79600161.txt |
| 19 | 00:28:34 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/13-79791886.txt |
| 20 | 00:28:35 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/14-79718097.txt |
| 21 | 00:28:36 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/15-79779187.txt |
| 22 | 00:28:37 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/16-79380514.txt |
| 23 | 00:28:39 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/17-79335513.txt |
| 24 | 00:28:40 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/18-79665976.txt |
| 25 | 00:28:41 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/19-79818917.txt |
| 26 | 00:28:42 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/ext/20-79663905.txt |
| 27 | 00:28:43 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/population.json |
| 28 | 00:28:44 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/prep.py |
| 29 | 00:30:43 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/prep.py |
| 30 | 00:32:20 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py |
| 31 | 00:32:31 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py |
| 32 | 00:32:46 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py |
| 33 | 00:34:00 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py |
| 34 | 00:34:25 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/make_inputs.py |
| 35 | 00:35:12 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py |
| 36 | 00:36:12 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/make_answers.py |
| 37 | 00:37:34 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/score.py |
| 38 | 00:37:39 | command | $ python3 EXPERIMENTS/181-fact-supply-closes-gap/score.py |
| 39 | 01:15:16 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-1.md |
| 40 | 01:15:17 | artifact | wrote EXPERIMENTS/181-fact-supply-closes-gap/AMENDMENT-2.md |
| 459 | 01:22:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E180-pubdev-viewcount/RESULT.md |
| 460 | 01:22:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E180-pubdev-viewcount/analyze.py |
| 461 | 01:22:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E180-pubdev-viewcount/collect.py |
| 462 | 01:22:18 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/E180-pubdev-viewcount/results_updated.json |
| 463 | 01:22:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/commands.log |
| 464 | 01:22:18 | unlogged_change | changed but never declared as an artifact: sessions/2026-10-17-007-fresh-exploration-find-a-concrete-builda/events.jsonl |
| 465 | 01:22:19 | doc_update | updated DECISIONS.md |
| 466 | 01:22:19 | doc_update | updated FAILURES.md |
| 467 | 01:22:19 | doc_update | updated STATE.md |
| 468 | 01:22:19 | session_end | E181 measured the mechanism F136 left open: does supplying the missing fact close the 0.4000 evidence gap? Four paired arms on E177's own EVID populat |

_418 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/events.jsonl
```

> Truncated to 300 lines. Full record: `sessions/2026-10-18-001-e181-test-whether-supplying-the-specific/events.jsonl`
