# Dataset definitions — version 1.0.0

Let **O** be the frozen original, **P(x)** the simple mark transform, **T(x)** the
teaching mark transform, and **F(x)** the four complete-string spelling folds.
Empty transformed strings are omitted; all sets use exact string equality.

| File | Definition |
| --- | --- |
| `original.txt.gz` | O, unchanged from `wiktionary-latin-inputs-v1` |
| `simple.txt.gz` | Union of F(P(x)) for every x in O |
| `teaching.txt.gz` | Simple set union {T(x) for every x in O} |
| `special.txt.gz` | Original strings containing a character outside ASCII A–Z, a–z and space |

These are views for different tests, not disjoint partitions. Their counts must
not be added to estimate coverage. A transformed view can contain new spellings
and collapse different originals. Always retain the original for source-spelling
behavior tests.

The simple transform turns 19 original mark-only strings into empty strings; the
teaching transform does so for 16. These empty results are omitted, while their
original spellings remain available in the original and special files.

## Mark policy

Transforms first apply Unicode NFD, remove selected marks, and return NFC. This
handles both precomposed letters and stacked marks; a literal regular expression
over precomposed vowels would miss such cases. No NFKD compatibility expansion,
case folding, transliteration or alphabet filter is performed.

- **Simple:** remove above marks, including macron, diaeresis, acute, grave,
  circumflex, breve, inverted/double breve, tilde, caron, ring, overline, above
  ties and above abbreviation letters. Recognized spacing accent signs are also
  removed. Below marks, overlay marks, ligatures and base letters survive.
- **Teaching:** remove the same marks except U+0304 COMBINING MACRON and U+0308
  COMBINING DIAERESIS. Their spacing equivalents U+00AF, U+00A8 and U+02C9 also
  survive where present. Every simple input is then included in the collection.
- **Original and special:** no Unicode transformation at all.

Examples: `a` + macron + acute + breve becomes `ā` in teaching and `a` in simple;
`ǟ` (diaeresis and macron) survives teaching and becomes `a` in simple; `ǘ` becomes
`ü` in teaching. `ę`, `ḥ`, `æ`, `œ`, `ø`, `w` and `W` survive both transforms.
Below macron, as in `ṯ`, remains a below mark. Thus “simple” means the stated
above-mark policy, not ASCII-only text or an assertion about writing systems.
Literal ASCII punctuation such as `^` is not interpreted as an attached accent.

The classifier uses Unicode combining classes 212, 214, 216, 228, 230, 232 and
234, with explicit exceptions for fixed-position marks in the source's Hebrew,
Arabic and Lao references and a spacing-sign table. The exact tables are recorded
in [manifest.json](../data/manifest.json); every observed mark, its frequency and
its disposition are in [mark-inventory.json](../data/mark-inventory.json).
This is a versioned input transform, not a universal visual-position detector for
unseen scripts. See [Unicode's combining-class definitions](https://www.unicode.org/reports/tr44/#Canonical_Combining_Class_Values).

## Spelling folds

Each of the four simple conventions replaces **all** u/v characters with its
selected target and **all** i/j characters with its selected target, preserving
case. Mapping is performed on decomposed base letters. It does not attempt to
infer consonantal versus vocalic use. `Jūlius vivit`, for example, contributes
`Iulius uiuit`, `Juljus ujujt`, `Ivlivs vivit` and `Jvljvs vjvjt`.

This is four global conventions, not every independent per-letter substitution.
Mixed source spellings remain available in the original. The additional marked
forms in teaching preserve source u/v and i/j; they are not mechanically folded
into marked `v` or `j`. Custom builds can request those combinations explicitly.

## Special-character subset

The broad character predicate captures macrons and other diacritics, historical
letters, ligatures, non-Latin scripts, digits, punctuation and standalone symbols.
Hyphens and abbreviation periods are included. This set deliberately includes
ordinary macron forms as well as rarities: “special” describes character coverage,
not invalidity. Its strings are byte-identical members of the original.
Users seeking a narrower subset can filter the original using their own character
policy, guided by the supplied mark inventory.

## Original extraction policy

Latin entry titles and literal lexical forms, source romanizations, usable link
text/targets, explicit heads, structured lexical references, Latin translation
and descendant objects throughout the raw archive, and qualifying aliases supplied
the inputs. Meanings, POS and morphological roles do not separate equal strings.

Reconstruction stars and bracket delimiters were removed, optional letters joined,
and bounded malformed table cells recovered. Source grammar/phonetic metadata and
empty placeholders were excluded in their field context. Single-sided affixes
also supplied a hyphen-free variant; internal hyphens were retained. There is no
period, w-letter, script, foreign-label or non-mainstream spelling exclusion.
No inflection generator or arbitrary prose tokenizer was used.
