# coding=utf-8
"""
Transcription database. Can read transcription in Oxford Word Practice format and query it.
"""

import xml.etree.ElementTree as ElementTree


class TranscriptDB:
    """
    Transcript DB
    """
    def __init__(self):
        """
        Create empty transcription DB
        """
        # maps word to it's entry object
        self.db = {}

    def read(self, file_name, filter_unit=None):
        """
        Reads XML data from filename, appending it to database
        :param file_name: xml filename to read
        :param filter_unit: if specified, only words from this unit will be read
        :return: count of entries loaded
        """
        tree = ElementTree.parse(file_name)
        return self._process_tree(tree.getroot(), filter_unit)

    def parse(self, data, filter_unit=None):
        root = ElementTree.fromstring(data)
        return self._process_tree(root, filter_unit)

    def _process_tree(self, root, filter_unit=None):
        count = 0
        for word in root:
            if word.tag != "word":
                continue
            if "unit" in word.attrib:
                units = self.parse_units(word.attrib["unit"])
            else:
                print "Word %s has no unit!" % word.attrib["str"]
                units = set()

            if filter_unit is not None and filter_unit not in units:
                continue
            w_text, synonym = self.extract_synonym(word.attrib["str"])
            ipa = unicode(word[0].text).strip("/")
            entry = TranscriptEntry(word=w_text, synonym=synonym, units=units, ipa=ipa)
            count += 1
            self.db[w_text] = entry
        return count

    def sorted_entries(self):
        return map(lambda v: v[1], sorted(self.db.iteritems(), key=lambda v: v[0]))

    def entries(self):
        return self.db.values()

    @staticmethod
    def parse_units(units):
        """
        Parses comma-separated list of integer units into set(int)
        :param units:
        :return:
        """
        res = set()
        for v in units.split(","):
            res.add(int(v.strip()))
        return res

    @staticmethod
    def extract_synonym(word_text):
        """
        Extracts synonym from text in "word (= synonym)"
        :param word_text:
        :return: pair of word,synonym
        """
        pos = word_text.find("(= ")
        if pos < 0:
            return word_text, None
        end_pos = word_text.find(")")
        return word_text[:pos-1], word_text[pos+3:end_pos]


class TranscriptEntry:
    """
    Transcript entry
    """
    def __init__(self, word, synonym, units, ipa):
        self.word = word
        self.synonym = synonym
        self.units = units
        self.ipa = ipa
        self.ipa_utf8 = decode_transcription(ipa)

    def __str__(self):
        return u"word=%s, synonym=%s, units=%s, ipa=%s" % (self.word, self.synonym, self.units, self.ipa)


def decode_transcription(s):
    """
    Decode Oxford transcription encoding into UTF-8 IPA characters
    :param s:
    :return:
    """
    decoded = '/' + ''.join(map(_decode_char, s)) + '/'

    decoded = decoded.replace(u'(r)', ' ' + unichr(876))

    return decoded.encode("utf-8")

def _decode_char(c):
    table = {
        u'&': u'æ',
        u'"': u"ˈ",
        u'I': u'ɪ',
        u'S': u'ʃ',
        u'%': u'ˌ',
        u'O': u'ɔ',
        u':': u'ː',
        u'@': u'ə',
        u'Q': u'ɒ',
        u'U': u'ʊ',
        u'T': u'θ',
        u'Í': u'tʃ',
        u'Z': u'ʒ',
        u'V': u'ʌ',
        u'A': u'ɑ',
        u'Ù': u'dʒ',
        u'3': u'ɜ',
        u'N': u'ŋ',
        u'2': u'',
        u'D': u'ð',
    }

    if c in table:
        return table[c]
    return c
