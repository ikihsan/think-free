# Coordinator scouting: test the research method

Retrieved 2026-10-03. This is additional scouting, not one of the six independent role reports. No findings are sent to the initial investigators.

## Accessibility and document structure

**Source-supported observation:** W3C describes how complex PDF layouts can produce incorrect reading order even after conversion from authoring tools, requiring repair and verification through assistive technology. This is evidence of a real technical problem, not evidence that no solution exists.

- https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3.html (page says updated 2025-07-15; directly opened)

**Counterevidence to a generic new remediation tool:** PAVE 2.0 already presents a guided remediation process. Its CHI 2025 paper reports a 19-participant comparison against Acrobat. The abstract and selected full-text methods, observations, and limitations have been inspected; reported outcomes are not independently reproduced and are not market-size claims. The study uses one document in two variants and acknowledges that its conformance score has not established actual screen-reader reading experience. Participants' intended future use is not retained adoption.

- https://arxiv.org/abs/2503.22216 (submitted 2025-03-28; abstract directly opened)
- https://arxiv.org/html/2503.22216v1 (selected sections inspected; especially sections 5 and 7)
- https://www.pave-pdf.org/ (existing tool and workflow)
- https://pave-pdf.org/help (existing remediation capabilities and limitations)
- https://github.com/visionably/outloud (additional open-source prior-art lead, repository opened; code not yet audited)

**Decision:** Do not propose a generic PDF checker/remediator as an invention. A distinct mechanism or demonstrable accessibility improvement would need to be established first, with actual assistive-technology users. Not selected for initial prototyping on this evidence.

## Manufacturing interoperability

**Source-supported observation:** NIST describes gaps between syntactic checks and semantic product/manufacturing information, representational differences across geometric models, and lengthy standards processes. The page includes older fiscal-year plans; it must not be treated as a complete current inventory of unresolved work.

- https://www.nist.gov/programs-projects/digital-thread-manufacturing (directly opened)

**Counterevidence to a generic validator:** NIST's STEP File Analyzer and Viewer already handles entity/attribute reporting, semantic and graphical PMI, and recommended-practice checks. The software page documents a Windows/Excel dependency and moves newer releases to GitHub. These are possible adoption constraints, not proof that a cross-platform rewrite would create a substantial new capability.

- https://www.nist.gov/services-resources/software/step-file-analyzer-and-viewer (directly opened)
- https://github.com/usnistgov/SFA (source repository opened; implementation not audited)

**Decision:** Retain as a domain worth investigating only with a precise semantic failure and reproducible corpus. Do not build another generic CAD file viewer.

## Scientific-data reproducibility

NASA's public policies establish reproducibility and data sharing as goals, but policy alone does not identify a specific unmet need. This search did not yield a candidate strong enough to test. Dataset reuse requires checking the source's individual license, not assuming every NASA-linked artifact is public domain.

- https://science.nasa.gov/researchers/science-information-policy_faq/ (search result inspected)
- https://science.data.nasa.gov/about/license (search result inspected)

## Queries

- site.w3.org WAI PDF techniques reading order limitations tagged PDF
- site.nist.gov manufacturing CAD interoperability repair geometry STEP challenges
- site.nasa.gov open source scientific data missing metadata uncertainty reproducibility
- site.nist.gov "STEP File Analyzer" GitHub source
- PAVE 2.0 accessible PDF source code github
- site.github.com "tagged PDF" "repair" accessibility

## Methodological lesson

Standards bodies provide reproducible definitions and sometimes public test cases. They also often provide existing software that invalidates an apparently new proposal. A problem statement plus a standards citation is insufficient to justify building. No originality or user-adoption claim is made by this scouting pass.
