# Building datasets

Use Python 3.11+ with only its standard library. The recorded release runtime is
in [the manifest](../data/manifest.json). Decoded UTF-8 hashes are the primary
dataset identities. Gzip uses level 9, no filename and a zero timestamp; compressed
bytes may differ across zlib implementations even when decoded hashes match.
Unicode database versions are recorded, so custom builds remain attributable.

## Reproduce the distributed views

```sh
python3 -m unittest discover -s tests -v
python3 tools/build.py release --output build
python3 tools/verify.py build
```

Choose an output directory that does not exist. The builder refuses to overwrite
it. It verifies the frozen original hash before creating files, and writes its
manifest last. An interrupted directory without a manifest is incomplete.
The output contains the four gzip files, a manifest and a mark inventory.
The original gzip is copied exactly when supplied as gzip.

Compare the `sha256` fields with the distributed manifest to establish dataset
identity. The verifier checks every member of every set, sorted uniqueness, line
format, checksums, the teaching superset and special subset. It uses a separate
reference transform driven by the declared mark inventory. Unit tests cover the
meaning of that policy, including stacked marks and marks that must remain.

For a byte-level check of the downloaded package, run from its root:

```sh
shasum -a 256 -c SHA256SUMS
```

## Custom views

One spelling convention:

```sh
python3 tools/build.py custom --marks simple --uv u --ij i --output custom/ui
```

Only the marked teaching transform, without the simple union:

```sh
python3 tools/build.py custom --marks teaching --output custom/marked
```

Remove all combining marks, including below and overlay marks:

```sh
python3 tools/build.py custom --marks all --output custom/all-marks-removed
```

Retain an extra mark by decomposed Unicode code point, or split phrases:

```sh
python3 tools/build.py custom --marks teaching --keep-mark 0301 --output custom/acute
python3 tools/build.py custom --marks preserve --tokens --output custom/tokens
```

`--uv` accepts `keep`, `u`, `v`, or `all`; `--ij` accepts `keep`, `i`, `j`, or
`all`. `--marks` accepts `preserve`, `simple`, `teaching`, or `all`.
`--keep-mark` is repeatable. Any nonempty custom result is sorted and deduplicated.
Custom output is `custom.txt.gz` plus a manifest naming the exact source hash,
options and builder. Custom data is not automatically a new official release.

The immutable original list is the provided raw material for these builds.
The tools here reproduce derivatives **from that seed**. They do not recreate the
historical raw-to-original extraction. The 2.9 GB Kaikki archive is not bundled;
its rotating download URL is not a promise that the pinned capture remains hosted.
See [source provenance](SOURCES.md) for the extraction boundary and snapshot hashes.
