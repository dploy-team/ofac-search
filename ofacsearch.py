"""
For each name part to name part comparison, a Jaro-Winkler score and a Difference (Soundex) score are taken.
The Difference function only returns a 1, 2, 3, or 4 (4 being the best match between the comparison string and the source string), so we replace these values with the following to make them more compatible with the Jaro-Winkler results: 1=0, 2=.333333, 3=.666667, 4 = 1.

The Jaro-Winkler score and our final Difference score are combined using the following equation: Name part score = ((JaroWinkler2 × 100) + (Difference × 100)) ÷ 2.
The scores returned for each of the input name parts are then averaged by the number of source name parts.
Then we take the total of name part scores divided by the number of name parts in the inputted name string.
Next a new Jaro-Winkler score is calculated by comparing the full inputted name string against the full name in the database (meaning the name parts are recombined into full strings).
This score is multiplied by 100
before being compared to the previous score we got by scoring name parts separately.
The greater score of these two comparisons is kept.
"""

import sys
from peewee import *
import sqlite3
import fuzzy
from soundex import ParsedDifference

from similarity.jarowinkler import JaroWinkler
import string


class OfacResult:
    score = 0
    name = ""
    ofac_id = 0

    def __init__(self, s, n, o):
        self.score = s
        self.name = n
        self.ofac_id = o

    def default(self, o):
        return o.__dict__


def search_db(table):
    conn = None
    conn = sqlite3.connect('ofac.db')
    cur = conn.cursor()
    cur.execute("SELECT sdn_name, id FROM "+table)
    rows = cur.fetchall()

    return rows


def CreateDict(src_name, src_name_part, input_name_part, avg, jaro, diff):
    return {
        "full_name": src_name,
        "name_part": src_name_part,
        "input_name_part": input_name_part,
        "score_avg": avg,
        "jaro_winkler": jaro,
        "difference": diff
    }


def Average(lst):
    return sum(lst) / len(lst)


def GetScore(src_name, input_name, min_score):
    src_name = src_name.translate(str.maketrans('', '', string.punctuation))
    input_name = input_name.translate(
        str.maketrans('', '', string.punctuation))
    jarowinkler = JaroWinkler()

    result = []

    total_score_scr_part = 0
    for input_name_part in input_name.split():
        column = []
        for src_name_part in src_name.split():
            winkler_part = jarowinkler.similarity(
                input_name_part, src_name_part)
            difference = ParsedDifference(input_name_part, src_name_part)

            avg = (winkler_part + difference) / 2

            column.append(avg)
        result.append(max(column))

    full_inputted_jaro = jarowinkler.similarity(input_name, src_name)
    score = Average(result)
    if (full_inputted_jaro > score):
        score = full_inputted_jaro
    return score * 100


def search(name, min_score):
    input_name = name.upper()
    min_score = float(min_score)

    tables = ['sdn', 'consolidated']
    hits = []
    for table in tables:
        hits.extend(search_db(table))

    results = []
    for hit in hits:
        src_name = hit[0].upper()
        ofac_id = str(hit[1])
        score = GetScore(src_name, input_name, min_score)
        if(score > min_score):
            print(src_name+'==='+str(score))
            results.append(OfacResult(score, src_name, ofac_id).__dict__)
    return results


# if __name__ == '__main__':

    # src = 'RODRIGUEZ OREJUELA, Gilberto Jose'
    # name = 'RODRIGUEZ OREJUELA, Gilberto Jose'

    # search('bin laden', 90)
