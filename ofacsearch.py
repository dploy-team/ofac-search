import sys
from peewee import *
import sqlite3
import fuzzy
from soundex import Difference

from similarity.jarowinkler import JaroWinkler


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

    return rows;


def GetScore(src_name, input_name):

    jarowinkler = JaroWinkler()


    for src_name_part in src_name.split():
        total_score_input_name_part = 0
        for input_name_part in input_name.split():
            winkler_part = jarowinkler.similarity(input_name_part, src_name_part)
            difference = Difference(input_name_part, src_name_part)

            combined_score = ((winkler_part * 100) + (difference * 100)) / 2
            total_score_input_name_part += combined_score
            
        avg_score_input_name = total_score_input_name_part / len(src_name.split()) / len(input_name.split()) 
        
    full_inputted_jaro = jarowinkler.similarity(input_name, src_name) * 100
    score = full_inputted_jaro
    if (avg_score_input_name > full_inputted_jaro):
        score = avg_score_input_name

    return score
    

def search(name, min_score):
    input_name = name
    min_score = float(min_score)
    
    tables = ['sdn', 'consolidated']
    hits = []
    for table in tables:
        hits.extend(search_db(table))

    results = []
    for hit in hits:
        src_name = hit[0].upper()
        ofac_id = str(hit[1])
        score = GetScore(src_name, input_name)
        
        if(score > min_score):
            print(src_name+'==='+str(score))
            results.append(OfacResult(score, src_name, ofac_id).__dict__)
    return results
if __name__ == '__main__':
    
    src= 'RODRIGUEZ OREJUELA, Gilberto Jose'
    name='RODRIGUEZ OREJUELA, Gilberto Jose'

    search('OREJUELA', 10)