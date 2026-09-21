# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (c) 2026 Xinjie Fang
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import unicodedata as ud

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build import BASIC_INPUT, compress, derive, transform


class TransformTests(unittest.TestCase):
    def test_stacked_marks(self):
        self.assertEqual(transform('a\u0304\u0301\u0306', 'teaching'), 'ā')
        self.assertEqual(transform('ǟ', 'teaching'), 'ǟ')
        self.assertEqual(transform('ǟ', 'simple'), 'a')
        self.assertEqual(transform('ǘ', 'teaching'), 'ü')

    def test_all_above_categories(self):
        self.assertEqual(transform('c͛tum Achille͡us C̅ ā ä ã č å', 'simple'),
                         'ctum Achilleus C a a a c a')

    def test_letters_below_marks_and_case_survive(self):
        self.assertEqual(transform('Węḥ æ œ ß ø ð', 'simple'), 'Węḥ æ œ ß ø ð')
        self.assertEqual(transform('ḥaraṯ', 'simple'), 'ḥaraṯ')
        self.assertEqual(transform('ḥaraṯ', 'all'), 'harat')

    def test_foreign_above_marks(self):
        self.assertEqual(transform('שׁ بُّ ກັ', 'simple'), 'ש ب ກ')
        self.assertEqual(transform('שָ', 'simple'), 'שָ')

    def test_four_spellings(self):
        self.assertEqual(derive(['Jūlius vivit'], 'simple', 'all', 'all'),
                         {'Iulius uiuit', 'Juljus ujujt', 'Ivlivs vivit',
                          'Jvljvs vjvjt'})

    def test_source_exactness_and_canonical_equivalence(self):
        text = 'a\u0304'
        self.assertEqual(transform(text), text)
        self.assertEqual(transform(text, 'teaching'), 'ā')
        self.assertEqual(transform('ā', 'teaching'), 'ā')

    def test_singletons_and_punctuation(self):
        self.assertEqual(transform('¯´˘', 'simple'), '')
        self.assertEqual(transform('¯´˘', 'teaching'), '¯')
        self.assertEqual(transform('-a J. Ⅳ ^', 'simple'), '-a J. Ⅳ ^')
        self.assertEqual(derive(['a b', 'b', '¯'], 'simple', tokens=True), {'a', 'b'})

    def test_special_is_broad(self):
        for value in ['mālum', 'æ', 'J.', '-a', 'Ⅳ', 'abc2']:
            self.assertIsNone(BASIC_INPUT.fullmatch(value))
        self.assertIsNotNone(BASIC_INPUT.fullmatch('bellum pulchrum'))

    def test_custom_mark_retention(self):
        self.assertEqual(transform('á̆', 'simple', keep_marks=['\u0301']), 'á')

    def test_gzip_reproducible(self):
        data = 'mālum\n'.encode()
        self.assertEqual(compress(data), compress(data))
        self.assertEqual(gzip.decompress(compress(data)), data)
        self.assertEqual(compress(data)[4:8], bytes(4))

    def test_idempotence(self):
        for value in ['ǟ', 'a\u0304\u0301', 'Jūlius', 'Węḥ', 'بُّ', '¯']:
            for marks in ['simple', 'teaching', 'all']:
                for uv, ij in [('keep', 'keep'), ('u', 'i'), ('v', 'j')]:
                    actual = transform(value, marks, uv, ij)
                    self.assertEqual(transform(actual, marks, uv, ij), actual)
                    self.assertEqual(ud.normalize('NFC', actual), actual)

    def test_custom_cli_and_overwrite_refusal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'source.txt'
            source.write_text('Jūlius\nā b\n', encoding='utf-8')
            output = root / 'result'
            command = [sys.executable, str(Path(__file__).resolve().parents[1] / 'tools/build.py'),
                       'custom', '--source', str(source), '--output', str(output),
                       '--marks', 'simple', '--uv', 'u', '--ij', 'i', '--tokens']
            first = subprocess.run(command, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(gzip.decompress((output / 'custom.txt.gz').read_bytes()), b'Iulius\na\nb\n')
            self.assertEqual(json.loads((output / 'manifest.json').read_text())['count'], 3)
            second = subprocess.run(command, capture_output=True)
            self.assertNotEqual(second.returncode, 0)


if __name__ == '__main__':
    unittest.main()
