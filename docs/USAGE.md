# Using the inputs

Start with **simple** for broad spelling and throughput tests, **teaching** when
macrons or diaereses are accepted, **original** for source-spelling fidelity, and
**special** for character handling. Selecting a smaller view is a test choice,
not an instruction to reject other inputs in a product.

## Compare an original tool and a port

Pin both executable versions, dictionary-data versions, invocation options,
encoding, platform and locale. Feed each exact input to both tools under the same
conditions. Capture output bytes, diagnostic bytes and exit status separately.
Compare ordering, multiplicity and whitespace unless the tool's declared behavior
explicitly permits a narrower comparison. Keep misses and errors visible.

The list itself is not an oracle. A miss may be correct, while a successful lookup
may still differ from the original implementation. Linguistic correctness needs a
separate, independently adjudicated set of expected answers. Do not infer accuracy
from the number of hits on this dataset.

Read gzip directly with the standard library:

```python
import gzip

with gzip.open("data/original.txt.gz", "rt", encoding="utf-8", newline="") as source:
    for line in source:
        input_text = line.removesuffix("\n")
        # Pass input_text to the tool as data, preserving internal spaces.
```

Use a tool's stdin, API field, or explicit argument array. Some inputs contain
punctuation or begin with a hyphen; do not interpolate them into executable shell
text. Follow the tool's documented argument boundary when necessary.

## Stress and throughput measurements

Distinguish process startup from steady-state parsing, cold from warm caches,
and sequential from concurrent operation. Report dataset ID and decoded SHA-256,
input count, throughput, latency distribution, failures and maximum resource use.
Normalize only when that is the behavior under test, and record that transform.

A tool that already strips marks or folds letters can still behave differently
before and after its normalization step. These views let a test isolate that
behavior. For a pure core-parser throughput test, the simple set avoids repeatedly
replaying many quantity variants; the original tests the broader input path.

Sorted input is convenient for reproducibility but creates strong prefixes and
cache locality. For an additional shuffled run, record the shuffle method, runtime
and seed. For reproducible subsets across languages, use a specified hash predicate
over each full UTF-8 input rather than a language runtime's default random hash.

## Phrases and custom tokenization

A space belongs to an input. The distributed lists do not split phrases.
`tools/build.py custom --tokens --output custom` provides whitespace splitting
and exact deduplication when a consumer needs it. It retains punctuation and
does not parse compound words, strip sentence punctuation or infer word boundaries.
Token lists are optional builds rather than an additional default download.
