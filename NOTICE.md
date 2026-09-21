# Attribution and licenses

The datasets contain lexical material derived from **English Wiktionary
contributors**, made available through **Kaikki / Wiktextract**, developed by
**Tatu Ylonen and contributors**. Source attribution and contributor-history
links are supplied in [the source-page index](provenance/source-pages.txt.gz),
with capture identifiers in [source.json](provenance/source.json).

The selection, extraction policy, bounded recoveries, derivative organization and
accompanying documentation are by **Xinjie Fang, Classical Cat Digital Humanities
Lab**, 2026. This is an independent derived dataset; no endorsement by Wikimedia,
Wiktionary or Kaikki is implied.

## Data and documentation — CC BY-SA 4.0

`data/`, `provenance/`, Markdown documentation, citation metadata and checksum
manifests are distributed under the **Creative Commons Attribution-ShareAlike
4.0 International License**, whose full text is in [LICENSE](LICENSE) and whose
[official legal text is available online](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en).
This includes the Lab's contributions to the adapted data and documentation.
The selected upstream reuse route is CC BY-SA 4.0 under
[Wikimedia's terms](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content).
The upstream availability of a GFDL route does not require users to select it here.

When redistributing, retain the source credits, source/provenance links and license
notice, and identify further changes. Share adapted material under the applicable
ShareAlike terms. The following compact notice may accompany copies, with links
to this repository and the source index:

> Derived from English Wiktionary contributors via Kaikki / Wiktextract.
> Selected and transformed by Xinjie Fang, Classical Cat Digital Humanities Lab.
> Data and documentation: CC BY-SA 4.0. Source credits and modifications are
> documented in NOTICE.md and docs/SOURCES.md.

No exclusive right is asserted over individual words or facts. The license applies
to the rights in the material that actually exist and can be licensed. The license
contains a disclaimer of warranties and limitation of liability.

## Software — AGPL-3.0-only

Original Python programs in `tools/` and `tests/` are copyright 2026 Xinjie Fang
and licensed under **GNU Affero General Public License version 3 only**.
See [the full license](LICENSES/AGPL-3.0-only.txt). This software license does not
relicense source lexical material or change the CC BY-SA license of derived lists.
Repository configuration is provided under the same software license.

## Changes from the upstream source

The original selected Latin-related lexical strings from structured fields,
removed field-specific metadata and reconstruction/bracket formatting, recovered
bounded malformed table cells, admitted historical/domain/script/alias cases,
added single-sided affix variants without their boundary hyphen, and sorted and
deduplicated exact inputs. It retains case, quantity, accents and u/v/i/j spelling.

The simple and teaching views apply the [documented Unicode transforms](docs/DATASETS.md).
The special view selects complete original strings by character content.
No morphological paradigms or linguistic answers were generated.

License texts are unmodified SPDX License List distributions of the respective
licenses. The legal texts themselves retain their publishers' notices.
