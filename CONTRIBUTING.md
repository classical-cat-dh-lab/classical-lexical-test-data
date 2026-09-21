# Contributing

Report a reproducible extraction or transform issue with the dataset version,
exact input spelling, expected policy behavior and source link where available.
Distinguish a dictionary miss from a dataset defect. A word's period, rarity,
letter `w`, foreign label or scientific use is not by itself a removal reason.

Frozen versions are never edited in place. Policy changes and new source captures
produce a new version, with counts, checksums and documented changes. A custom
profile need not become another default downloadable dataset.

For code changes, use the standard library, add a focused regression test for the
changed behavior, run the tests in README.md and verify complete derived sets if
the transformation policy changes. Keep the original byte-identical.

Contributions to data and documentation use CC BY-SA 4.0; contributions to software
use AGPL-3.0-only, as described in NOTICE.md. Retain upstream source credit.
