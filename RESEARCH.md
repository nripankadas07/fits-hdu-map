# Research —19 October2026

User: Astronomy archive ingestion maintainers.

Pain: A rejected small FITS needs physical HDU boundaries and padding evidence before array interpretation.

MVP: Map FITS primary/IMAGE header, data and padding byte ranges without loading arrays.

Acceptance: Correct two-HDU layout, zero dimensions, float64 data extent, quoted slash handling, malformed card order/duplicates, truncation and nonzero padding.

Demand is inferred from workflows and adjacent discussions, not verified requests. Discovery path: descriptive GitHub topics, runnable invented examples and chronological project index. No unsolicited outreach or artificial activity.

## Alternatives

Live GitHub search sorted Most stars: `FITS astronomy; Astropy`. Highest-star relevant comparable found: **astropy/astropy**. This is bounded search/reference-follow coverage, not an exhaustive global ranking. Broad/unrelated keyword matches were excluded.

| Repository | Stars observed | Last push UTC | API license |
| --- | ---: | --- | --- |
| [astropy/astropy](https://github.com/astropy/astropy) | 5350 | 2026-10-18T21:02:13Z | BSD-3-Clause |
| [ATTron/astroz](https://github.com/ATTron/astroz) | 276 | 2026-10-16T18:39:23Z | MIT |
| [esheldon/fitsio](https://github.com/esheldon/fitsio) | 150 | 2026-10-17T17:24:30Z | GPL-2.0 |
| [heasarc/cfitsio](https://github.com/heasarc/cfitsio) | 71 | 2026-10-06T02:09:09Z | UNCLASSIFIED |

Astropy and CFITSIO already provide much broader FITS IO and verification; fitsio exposes CFITSIO-backed table/image access. Astroz is a terminal astronomy workflow. No missing HDU-inspection capability is claimed. The precise ranges and strict subset are our interface choice.

Current READMEs, selected relevant source and up to five issue/PR records were read; exact observations and source identities are in [provenance](RESEARCH_PROVENANCE.json). Our clean-install example establishes our behavior only. Established alternatives provide broader capability, docs, examples and communities. Competitor installability, time to first useful result, reliability, support response and performance were not measured. No feature-absence claim. Stars are discovery evidence, not quality/performance. Unclassified licenses are not permission to copy. No competitor code, prose, branding or fixtures are bundled.

Primary technical reference: https://fits.gsfc.nasa.gov/fits_standard.html. NASA's current FITS4 PDF fetch timed out; the official standard landing page and NASA CFITSIO primer were readable. ELF reference is explicitly a draft generic ABI; processor-specific behavior remains outside scope. No technical performance benchmark was conducted.

Portfolio distinction: No FITS HDU mapper was found among all198 owned repositories. Existing media inspectors do not implement astronomical block/card semantics.

Original capability is the bounded implementation/evidence workflow, not a claim to invent the file format or standard algorithm.
