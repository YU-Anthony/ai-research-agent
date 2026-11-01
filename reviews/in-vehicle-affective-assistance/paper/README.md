# Formatted research-paper draft

- **paper.pdf**: locally compiled review manuscript.
- **paper.tex** + **references.bib**: editable LaTeX/BibTeX source pair.
- **paper-standalone.tex**: single-file LaTeX with all 24 reference entries embedded; no BibTeX run required.
- **template.tex**: neutral article layout, not an official journal/conference template.
- **paper.md**: GitHub-readable article with numeric in-text citations and all 24 references at the end.
- **paper-input.md** + **metadata.json**: generated Pandoc build input; use paper.md for reading.
- **build_paper.py**: reproducible local build from ../manuscript.md and its selected bibliography.
- **build-summary.json**: citation/table build checks; not scientific validation.

## Format

A4, single column, 11-point Latin Modern Roman, 25 mm margins; title and pending-author block, abstract, keywords, numbered sections/subsections, table numbers/captions, page numbers, numeric citations and a BibTeX-generated reference list. Declarations are unnumbered. Authors/affiliations have not been invented. The exploratory-review status remains visible because retrieval and human verification are incomplete.

The target venue has not been specified. This is a conventional academic article format; it is not claimed to conform to IEEE, ACM, Elsevier or any specific journal's submission requirements. A venue-specific class/style should be applied after selecting the venue and checking its author instructions. Do not add a publisher logo, acceptance date, author affiliation, funding or compliance assertion without verification.

## Local build

Requires local Pandoc, XeLaTeX, BibTeX and standard TeX packages (fontspec, natbib, unsrtnat, geometry, longtable, booktabs, xurl, fancyhdr and microtype). No network request or automatic package download is made by the script.

From repository root:

```bash
python reviews/in-vehicle-affective-assistance/paper/build_paper.py
```

The script runs Pandoc and the XeLaTeX/BibTeX/XeLaTeX/XeLaTeX sequence with shell escape disabled. It checks the 24 selected reference keys, absence of unresolved citations/missing glyphs/overflowing lines, and expected table count. Build files are retained in ignored build/ for inspection. Scientific/editorial review is still necessary.

For repeatable content changes, edit ../manuscript.md and ../manuscript-references.bib, then rebuild. Generated paper.md/paper-input.md/metadata.json/references.bib/paper.tex/paper-standalone.tex/PDF are replaced by this known build process. Do not treat them as independent sources of truth.

## Overleaf

Upload paper.tex and references.bib into a new project, set paper.tex as the main file, choose **XeLaTeX**, and use the normal automatic BibTeX compilation. Alternatively, edit the pending-author block directly for a separately maintained author copy; record those changes before regenerating locally. No paid account or external model API is needed by the source itself.

### Single-file alternative

Upload only **paper-standalone.tex**, select it as the main file and choose XeLaTeX. It embeds the generated `thebibliography` environment, so the bibliography is visible in the source and compilation does not require a separate .bib file or BibTeX step. Two XeLaTeX passes resolve citation labels. The build script compiles and verifies this alternative locally. Never treat the Pandoc build input as the reference-complete reading version.

## Still outstanding

Broader database retrieval, remaining eligibility screening, human checking of source interpretations/denominators, publication-version reconciliation, novelty assessment and real author declarations remain pending. The PDF is a formatted working manuscript, not a completed systematic review or an authorized submission. No aiXiv upload was attempted.
