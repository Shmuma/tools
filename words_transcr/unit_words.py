"""
Tool dumps given unit words from xml transcription DB
"""

import csv
import sys
import argparse
from lib.trans_db import TranscriptDB


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("db", type=str, help="Database file name")
    parser.add_argument("unit", type=int, help="Unit to dump")

    args = parser.parse_args()

    db = TranscriptDB()
    count = db.read(args.db, filter_unit=args.unit)
    writer = csv.writer(sys.stdout)

    for entry in db.sorted_entries():
        row = [entry.word, "", entry.ipa_utf8]
        writer.writerow(row)

