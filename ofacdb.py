
"""
MIT License

Copyright (c) 2016 Sparrow A.I., LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# Contact: Scott Condie (scott@sparrowai.com)



from peewee import *
import csv
from elasticsearch import Elasticsearch
from playhouse.shortcuts import model_to_dict, dict_to_model
import wget
import os, shutil


database = SqliteDatabase("ofac.db")         # async doesn't seem to work with sqlite3, so synchronous for now

class BaseModel(Model):
    class Meta:
        database = database


class SDN(BaseModel):
    ent_num = IntegerField()
    sdn_name = CharField()
    sdn_type = CharField()
    program = CharField()
    title = CharField()
    call_sign = CharField()
    vess_type = CharField()
    tonnage = CharField()
    grt = CharField()
    vess_flag = CharField()
    vess_owner = CharField()
    remarks = CharField()


class Consolidated(BaseModel):
    ent_num = IntegerField()
    sdn_name = CharField()
    sdn_type = CharField()
    program = CharField()
    title = CharField()
    call_sign = CharField()
    vess_type = CharField()
    tonnage = CharField()
    grt = CharField()
    vess_flag = CharField()
    vess_owner = CharField()
    remarks = CharField()


def populate_db(filename, dbclass, keys):
    dbclass.truncate_table()
    with open(filename, 'r') as fh:
        reader = csv.reader(fh, delimiter=',')

        for row in reader:
            newrow = []
            for ii in row:
                if ii == "-0- ":
                    newrow.append("")
                else:
                    newrow.append(ii)

            vals = dict(zip(keys,newrow))
            try:
                new_entry = dbclass.create(**vals)
                new_entry.save()
            except:
                print('')


def import_files():
    print('WGET ->> https://www.treasury.gov/ofac/downloads/sdn.csv')
    if (os.path.exists('files/SDN.csv')):
        os.remove('files/SDN.csv')
    sdn_url = 'https://www.treasury.gov/ofac/downloads/sdn.csv'
    wget.download(sdn_url, 'files/SDN.csv')
    
    print('WGET ->> https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv')
    if (os.path.exists('files/cons_prim.csv')):
        os.remove('files/cons_prim.csv')
    sdn_url = 'https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv'
    wget.download(sdn_url, 'files/cons_prim.csv')

    print ('Downloaded!')

    print('Deleting tables...')

    tables = [SDN, Consolidated]
    for tt in tables:
        try:
            tt.delete()
        except OperationalError:
            print("Table doesn't exist")
    

    print('Pupulating DB...')
    

    # Populate the db 
    database.connect()
    database.create_tables(tables)

    #  SDN file
    sdn_file = "files/SDN.csv"
    sdn_keys = ["ent_num", "sdn_name", "sdn_type", "program", "title", "call_sign", "vess_type", "tonnage", "grt", "vess_flag","vess_owner", "remarks"]
    populate_db(sdn_file, SDN, sdn_keys)

    # Consolidated file
    cons_file = "files/cons_prim.csv"
    cons_keys = ["ent_num", "sdn_name", "sdn_type", "program", "title", "call_sign", "vess_type", "tonnage", "grt", "vess_flag","vess_owner", "remarks"]
    populate_db(cons_file, Consolidated, cons_keys)

    print('Done!')





