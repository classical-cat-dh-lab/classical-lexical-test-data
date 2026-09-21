# Source provenance

The original was extracted from Kaikki's raw English-Wiktionary JSONL archive:
dump dated **2026-09-02**, extraction dated **2026-09-16**, captured **2026-09-20**.
It was frozen as `wiktionary-latin-inputs-v1` on **2026-09-21**.

[source.json](../provenance/source.json) records the captured archive's SHA-256,
size, record count, extractor revisions and selected-component hashes.
[The source-page index](../provenance/source-pages.txt.gz) contains one English
Wiktionary URL per line. These URLs provide access to source pages and their
contributor histories. They cover Latin entries, host pages of explicit Latin
references, and the inspected neutral alias pages and targets. The index is
deliberately conservative: some inspected alias candidates did not supply a final
input. It is an attribution companion, not a graph connecting individual inputs.

Page URLs refer to live pages, not frozen revisions. The raw capture and component
hashes identify the historical extraction; current pages and Kaikki downloads may
have changed. The original file's decoded SHA-256 is:

```text
ea1748a45aaa98dc09ecd3ce8f541241abcba3bab24bb51d6a8a59eb75c2be0b
```

The [dataset definitions](DATASETS.md) describe the selected fields and recovery
policy. This publication does not include definitions, a quotation corpus, media,
the complete Kaikki raw archive, or a claim that the source contains every Latin
form. No missing paradigms were generated. Apparent foreign material may remain
because the accepted purpose is plausible dictionary input.

## Upstream projects

- [English Wiktionary](https://en.wiktionary.org/): contributor-maintained lexical content.
- [Kaikki raw data](https://kaikki.org/dictionary/rawdata.html): extracted dataset distribution.
- [Wiktextract](https://github.com/tatuylonen/wiktextract): structured extraction software.
- [Wikimedia content licensing](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content): reuse and attribution terms.

For the extraction method, see Tatu Ylonen, 2022,
[“Wiktextract: Wiktionary as Machine-Readable Structured Data”](https://aclanthology.org/2022.lrec-1.140/),
Proceedings of LREC 2022, pages 1317–1325. The software's MIT license does not
replace the license on extracted Wiktionary data. No upstream extractor software
is bundled in this repository.
