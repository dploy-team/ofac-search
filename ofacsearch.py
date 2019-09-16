import sys
from pyjarowinkler import distance
from peewee import *
import sqlite3

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
    cur.execute("SELECT sdn_name, ent_num FROM "+table)
    rows = cur.fetchall()

    return rows;

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
        # print(src_name)
        
        winkler = distance.get_jaro_distance(input_name, src_name, winkler=True, scaling=0.1)
        diff = 0
        src_name_part_nysiis = fuzzy.nysiis(src_name)
        input_name_nysiis = fuzzy.nysiis(input_name)
        if (input_name_nysiis and src_name_part_nysiis):
            diff = distance.get_jaro_distance(src_name_part_nysiis, fuzzy.nysiis(input_name) )

        score = ( (winkler * 100) + (diff * 100)) / 2
        if(score > min_score):
            results.append(OfacResult(score, src_name, ofac_id).__dict__)
    return results
if __name__ == '__main__':
    search('Wagner', 70)
