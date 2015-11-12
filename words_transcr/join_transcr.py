"""
Tool joins transcription to comma-separated input words list.

Transcription is read from XML datafile grabbed from Oxford Word Practice CD.

Input data expect to have CSV format without header. We expect word to be transcribed in first column,
transcription in UTF-16 format is joined as last column.
"""

import sys
import csv

from lib.trans_db import TranscriptDB


if __name__ == "__main__":
    transcript_path = "data/extrawordlist-intermediate.xml"

    db = TranscriptDB()
    db.read(transcript_path, filter_unit=1)

    reader = csv.reader(sys.stdin)
    writer = csv.writer(sys.stdout)
    for row in reader:
        word = row[0]
        row.append("/" + word + "/")
        writer.writerow(row)
