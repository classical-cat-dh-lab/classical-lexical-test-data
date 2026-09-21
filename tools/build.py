#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Xinjie Fang
"""Build Latin dictionary test inputs with Python's standard library."""
from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import io
import itertools
import json
from pathlib import Path
import platform
import re
import shutil
import unicodedata as ud
import zlib

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL_SHA256 = 'ea1748a45aaa98dc09ecd3ce8f541241abcba3bab24bb51d6a8a59eb75c2be0b'
ABOVE_CLASSES = {212, 214, 216, 228, 230, 232, 234}
# Fixed-position or class-zero above marks, including all such marks observed
# in the original's Hebrew, Arabic and Lao references.
ABOVE_EXCEPTIONS = set('\u05c1\u05c2\u064b\u064c\u064e\u064f\u0651\u0652\u0670\u0eb1')
SPACING_ABOVE = set('\u00a8\u00af\u00b4\u02c6\u02c7\u02c9\u02ca\u02cb\u02d8\u02d9\u02da\u02dc\u02dd\u0384')
TEACHING_KEEP = set('\u0304\u0308\u00af\u00a8\u02c9')
BASIC_INPUT = re.compile(r'[A-Za-z ]+\Z')


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def above(c):
    return ud.combining(c) in ABOVE_CLASSES or c in ABOVE_EXCEPTIONS | SPACING_ABOVE


def transform(value, marks='preserve', uv='keep', ij='keep', keep_marks=()):
    """Preserve exact text unless a requested operation needs decomposition."""
    if marks == 'preserve' and uv == ij == 'keep':
        return value
    chars = ud.normalize('NFD', value)
    keep = set(keep_marks) | (TEACHING_KEEP if marks == 'teaching' else set())
    if marks != 'preserve':
        chars = ''.join(c for c in chars if c in keep or not (
            (ud.category(c).startswith('M') or c in SPACING_ABOVE)
            if marks == 'all' else above(c)))
    mapping = {}
    for letters, target in [('uv', uv), ('ij', ij)]:
        if target != 'keep':
            for c in letters:
                mapping[ord(c)] = target
                mapping[ord(c.upper())] = target.upper()
    return ud.normalize('NFC', chars.translate(mapping))


def read_lines(path):
    data = Path(path).read_bytes()
    if data.startswith(b'\x1f\x8b'):
        data = gzip.decompress(data)
    if not data.endswith(b'\n') or b'\r' in data or data.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Expected UTF-8 without BOM and LF-terminated lines')
    words = data.decode('utf-8').split('\n')[:-1]
    if any(not w or any(ud.category(c) == 'Cc' for c in w) for w in words):
        raise ValueError('Empty input or control character')
    if words != sorted(set(words)):
        raise ValueError('Inputs must be sorted and exactly unique')
    return data, words


def compress(data):
    buffer = io.BytesIO()
    with gzip.GzipFile(filename='', mode='wb', fileobj=buffer, mtime=0, compresslevel=9) as f:
        f.write(data)
    return buffer.getvalue()


def write_list(out, name, words):
    data = ''.join(w + '\n' for w in sorted(words)).encode('utf-8')
    compressed = compress(data)
    (out / (name + '.txt.gz')).write_bytes(compressed)
    return {'file': name + '.txt.gz', 'count': len(words), 'bytes': len(data),
            'sha256': sha256(data), 'gzip_bytes': len(compressed),
            'gzip_sha256': sha256(compressed)}


def spelling_pairs(uv, ij):
    return itertools.product('uv' if uv == 'all' else [uv],
                             'ij' if ij == 'all' else [ij])


def derive(words, marks, uv='keep', ij='keep', tokens=False, keep_marks=()):
    result = set()
    for word in words:
        for part in word.split() if tokens else [word]:
            for u, i in spelling_pairs(uv, ij):
                value = transform(part, marks, u, i, keep_marks)
                if value:
                    result.add(value)
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def build(source, output):
    raw, words = read_lines(source)
    if sha256(raw) != ORIGINAL_SHA256:
        raise ValueError('Original v1 hash mismatch')
    if output.exists():
        raise ValueError('Choose a new output directory')
    output.mkdir(parents=True)
    profiles = {}
    profiles['original'] = write_list(output, 'original', words)
    # Preserve the frozen gzip bytes, not just its decoded text.
    if Path(source).read_bytes().startswith(b'\x1f\x8b'):
        shutil.copyfile(source, output / 'original.txt.gz')
        gz = (output / 'original.txt.gz').read_bytes()
        profiles['original'].update(gzip_bytes=len(gz), gzip_sha256=sha256(gz))
    simple = derive(words, 'simple', 'all', 'all')
    profiles['simple'] = write_list(output, 'simple', simple)
    teaching = derive(words, 'teaching')
    teaching_only_count = len(teaching - simple)
    teaching.update(simple)
    profiles['teaching'] = write_list(output, 'teaching', teaching)
    del teaching
    special = {w for w in words if BASIC_INPUT.fullmatch(w) is None}
    profiles['special'] = write_list(output, 'special', special)
    counts = Counter(c for w in words for c in set(ud.normalize('NFD', w))
                     if ud.category(c).startswith('M') or c in SPACING_ABOVE)
    inventory = [{'codepoint': f'U+{ord(c):04X}', 'name': ud.name(c, 'UNNAMED'),
                  'combining_class': ud.combining(c), 'input_count': n,
                  'simple_removes': above(c),
                  'teaching_removes': above(c) and c not in TEACHING_KEEP}
                 for c, n in sorted(counts.items())]
    write_json(output / 'mark-inventory.json', inventory)
    write_json(output / 'manifest.json', {
        'schema': 'classical-lexical-test-data/1', 'version': '1.0.0',
        'original_id': 'wiktionary-latin-inputs-v1', 'source_sha256': ORIGINAL_SHA256,
        'python_version': platform.python_version(), 'unicode_version': ud.unidata_version,
        'zlib_version': zlib.ZLIB_RUNTIME_VERSION, 'builder_sha256': sha256(Path(__file__).read_bytes()),
        'profiles': profiles, 'teaching_additions_over_simple': teaching_only_count,
        'simple_empty_source_inputs_omitted': sum(not transform(w, 'simple') for w in words),
        'teaching_empty_source_inputs_omitted': sum(not transform(w, 'teaching') for w in words),
        'above_combining_classes': sorted(ABOVE_CLASSES),
        'above_exceptions': sorted(f'U+{ord(c):04X}' for c in ABOVE_EXCEPTIONS),
        'spacing_above': sorted(f'U+{ord(c):04X}' for c in SPACING_ABOVE),
        'teaching_keep': sorted(f'U+{ord(c):04X}' for c in TEACHING_KEEP),
        'special_rule': 'Original inputs containing any character outside ASCII A-Z, a-z and space',
        'normalization': 'Original/special exact; transformed inputs NFD then filtering/folding then NFC',
    })
    print(json.dumps(profiles, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('release', help='Build the four release datasets from frozen original v1')
    p.add_argument('--source', type=Path, default=ROOT / 'data/original.txt.gz')
    p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('custom', help='Build a separately named custom derivative')
    p.add_argument('--source', type=Path, default=ROOT / 'data/original.txt.gz')
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--marks', choices=['preserve', 'simple', 'teaching', 'all'], default='preserve')
    p.add_argument('--uv', choices=['keep', 'u', 'v', 'all'], default='keep')
    p.add_argument('--ij', choices=['keep', 'i', 'j', 'all'], default='keep')
    p.add_argument('--keep-mark', action='append', default=[], metavar='HEX',
                   help='Retain an additional decomposed code point, e.g. 0301; repeatable')
    p.add_argument('--tokens', action='store_true', help='Split on whitespace only')
    args = parser.parse_args()
    if args.command == 'release':
        build(args.source, args.output)
    else:
        _, words = read_lines(args.source)
        if args.output.exists():
            parser.error('Choose a new output directory')
        keep = [chr(int(x.removeprefix('U+'), 16)) for x in args.keep_mark]
        result = derive(words, args.marks, args.uv, args.ij, args.tokens, keep)
        args.output.mkdir(parents=True)
        receipt = write_list(args.output, 'custom', result)
        receipt.update(marks=args.marks, uv=args.uv, ij=args.ij, tokens=args.tokens,
                       keep_marks=args.keep_mark, source_sha256=sha256(read_lines(args.source)[0]),
                       unicode_version=ud.unidata_version, builder_sha256=sha256(Path(__file__).read_bytes()))
        write_json(args.output / 'manifest.json', receipt)
        print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
