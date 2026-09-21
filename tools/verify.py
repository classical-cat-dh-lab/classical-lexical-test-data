#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Xinjie Fang
"""Verify every dataset against an independent set-level reference transform."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import unicodedata as ud


def verify(directory):
    manifest = json.loads((directory / 'manifest.json').read_text())
    original_bytes = gzip.decompress((directory / 'original.txt.gz').read_bytes())
    assert hashlib.sha256(original_bytes).hexdigest() == manifest['source_sha256']
    assert manifest['source_sha256'] == 'ea1748a45aaa98dc09ecd3ce8f541241abcba3bab24bb51d6a8a59eb75c2be0b'
    original = original_bytes.decode().splitlines()
    inventory = json.loads((directory / 'mark-inventory.json').read_text())
    remove = {kind: {chr(int(r['codepoint'][2:], 16)) for r in inventory if r[kind + '_removes']}
              for kind in ['simple', 'teaching']}
    def stripped(word, kind):
        return ud.normalize('NFC', ''.join(c for c in ud.normalize('NFD', word) if c not in remove[kind]))
    simple = set()
    for u, i in [('u', 'i'), ('u', 'j'), ('v', 'i'), ('v', 'j')]:
        folded = set()
        for word in original:
            value = ud.normalize('NFD', stripped(word, 'simple'))
            value = re.sub('[uv]', u, value)
            value = re.sub('[UV]', u.upper(), value)
            value = re.sub('[ij]', i, value)
            value = re.sub('[IJ]', i.upper(), value)
            if value:
                folded.add(ud.normalize('NFC', value))
        simple.update(folded)
    del folded
    results = {}
    for name, rec in manifest['profiles'].items():
        compressed = (directory / rec['file']).read_bytes()
        data = gzip.decompress(compressed)
        words = data.decode('utf-8').split('\n')[:-1]
        actual = set(words)
        assert data.endswith(b'\n') and not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data
        assert words == sorted(actual) and len(words) == rec['count'] and '' not in actual
        assert all(not any(ud.category(c) == 'Cc' for c in w) for w in words)
        assert hashlib.sha256(data).hexdigest() == rec['sha256'] and len(data) == rec['bytes']
        assert hashlib.sha256(compressed).hexdigest() == rec['gzip_sha256']
        assert len(compressed) == rec['gzip_bytes']
        if name == 'original':
            assert data == original_bytes
        elif name == 'simple':
            assert actual == simple
            assert all(stripped(w, 'simple') == w for w in words)
        elif name == 'teaching':
            expected = {stripped(w, 'teaching') for w in original} - {''}
            expected.update(simple)
            assert actual == expected and simple <= actual
            assert all(stripped(w, 'teaching') == w for w in words)
            del expected
        elif name == 'special':
            assert actual == {w for w in original if any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ' for c in w)}
        else:
            raise AssertionError('Unknown dataset')
        results[name] = {'count': len(words), 'format_hash_and_complete_set': 'pass'}
        del actual, words
    assert set(results) == {'original', 'simple', 'teaching', 'special'}
    print(json.dumps({'result': 'pass', 'datasets': results}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    verify(parser.parse_args().directory)
