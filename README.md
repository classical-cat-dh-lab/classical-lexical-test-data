# Classical Lexical Test Data

Reusable Latin dictionary inputs for compatibility, regression and stress testing.
This first edition contains a frozen Wiktionary-derived original and three useful
views of it. Each line is an equal input: lemmas, inflections, principal parts,
participles, compounds and phrases carry no separate labels or relationships.

The collection models a person making a good-faith lookup in a Latin dictionary.
It includes historical and uncommon spellings, scientific names, reconstructions,
affixes and borderline references. It supplies **inputs, not expected answers**:
a dictionary miss is not a failed test, and an included spelling is not a claim of
linguistic correctness. Coverage is bounded by the captured source and extraction
rules; this is not every possible Latin form.

## Choose a dataset

| Dataset | Distinct inputs | Gzip size | Purpose |
| --- | ---: | ---: | --- |
| [original](data/original.txt.gz) | 2,074,758 | 4.86 MiB | Frozen source spellings |
| [simple](data/simple.txt.gz) | 3,036,169 | 6.89 MiB | Above marks removed; four spelling folds combined |
| [teaching](data/teaching.txt.gz) | 4,126,749 | 9.60 MiB | Simple set plus macron/diaeresis source forms |
| [special](data/special.txt.gz) | 1,014,233 | 2.49 MiB | Original inputs with non-basic characters |

The simple file contains the deduplicated union of four spelling conventions:
`u+i`, `u+j`, `v+i`, and `v+j`. The teaching file contains the whole simple file
plus original-spelling forms with macrons and diaereses retained. The special file
is a deliberately overlapping subset of the original, selected by character content.
See [dataset definitions](docs/DATASETS.md) for exact rules and examples.

All files are gzip-compressed UTF-8, without BOM or header, one input per
LF-terminated line, sorted by Unicode code point and exactly deduplicated.
Multiword inputs remain on one line. Read compressed files directly or decompress
them with any gzip utility. [Usage](docs/USAGE.md) covers behavioral comparisons,
load measurements and reproducible sampling.

## Build and verify

Python 3.11 or later and its standard library are sufficient; no installation,
network access or API key is needed. Run from this repository:

```sh
python3 -m unittest discover -s tests -v
python3 tools/build.py release --output build
python3 tools/verify.py build
```

The original is the immutable build seed. [Build instructions](docs/BUILDING.md)
explain custom mark retention, any single spelling convention, removal of all
combining marks and optional whitespace tokenization. The bundled derivatives
have complete-set verification in addition to their checksums.

## Source, license and citation

Lexical material comes from **English Wiktionary contributors**, extracted and
distributed through **Kaikki / Wiktextract**, developed by **Tatu Ylonen and
contributors**. Selection, recovery, test-input policy and derivative tools are
maintained by **Xinjie Fang, Classical Cat Digital Humanities Lab**.

- Data, provenance and documentation: [CC BY-SA 4.0](LICENSE).
- Original Python tools and tests: [AGPL-3.0-only](LICENSES/AGPL-3.0-only.txt).
- Read [NOTICE](NOTICE.md) for upstream credit, changes and reuse attribution.
- [Source provenance](docs/SOURCES.md) records the snapshot and source-page index.
- [CITATION.cff](CITATION.cff) supplies dataset citation metadata.

Version 1.0.0 is archived at [doi:10.5281/zenodo.22880153](https://doi.org/10.5281/zenodo.22880153).
Use the [all-versions DOI](https://doi.org/10.5281/zenodo.22880152) when referring
to the collection across editions. Cite the version DOI for reproducible tests.

The software license does not replace the data license. No restriction is asserted
over individual words or facts beyond rights that actually apply. For fixes and
new profiles, see [CONTRIBUTING](CONTRIBUTING.md).
