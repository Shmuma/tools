import unittest

from trans_db import TranscriptDB, TranscriptEntry


class TestTranscriptDB(unittest.TestCase):
    def test_parse_units(self):
        cases = [("1", [1]),
                 ("1, 22", [1, 22]),
                 ("1,2,3", [1, 2, 3])]

        for text, valid in cases:
            self.assertEqual(TranscriptDB.parse_units(text), set(valid))

    def test_extract_synonym(self):
        self.assertEqual(TranscriptDB.extract_synonym("text"), ("text", None))
        self.assertEqual(TranscriptDB.extract_synonym("text (= synonym)"), ("text", "synonym"))

    def test_parse(self):
        db = TranscriptDB()
        count = db.parse("""
        <exercise  template="wordlist">
        <word str="ATM" unit="79">
                <ipa><![CDATA[%eI %ti: "em]]></ipa>
        </word>
        </exercise>
        """)

        self.assertEqual(count, 1)


if __name__ == '__main__':
    unittest.main()
