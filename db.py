# make mode tht only persits to disk
# then a funct tha does stuff like (add_to_balance(100, obj), not obj.add...)

from psycopg2 import connect
import logging

def make_schema():
    conn = connect(dbname='notes')
    cur = conn.cursor()
    cur.execute("create table player (name varchar primary key)")
    cur.execute("insert into player (name) values ('john')")
    cur.execute("create table pattern (name varchar primary key, beat_div int, notes boolean[])")
    cur.execute("insert into pattern (name, beat_div, notes) values ('easy-4', 4, '{1,1,1,1}')")
    cur.execute("insert into pattern (name, beat_div, notes) values ('easy-8', 8, '{1,1,1,1,1,1,1,1}')")
    cur.execute("insert into pattern (name, beat_div, notes) values ('12123', 12, '{1,0,0,1,0,0,1,0,1,0,1,0}')")

    cur.execute("create table attempt (id serial primary key, pattern_name varchar, player_name varchar, bpm int, ts timestamp with time zone)")
    cur.execute("create table delta (id serial primary key, attempt_id int references attempt(id), ts int, diff int)")
    cur.execute("create table miss (id serial primary key, attempt_id int, ts int)")
    cur.execute("create table extra (id serial primary key, attempt_id int, ts int)")
    conn.commit()
    conn.close()

def wipe():
    conn = connect(dbname='postgres')
    conn.set_isolation_level(0)
    cur = conn.cursor()
    cur.execute("drop database notes")
    cur.execute("create database notes")
    conn.close()

def get_pattern(name):
    conn = connect(dbname='notes')
    cur = conn.cursor()
    cur.execute("select beat_div, notes from pattern where name='"+name+"'")
    row = cur.fetchone()
    conn.close()
    return (row[0], row[1])
    #return {'name': row[0], 'contents': ('beat_div': row[1], 'notes': row[2])}

def get_patterns():
    conn = connect(dbname='notes')
    cur = conn.cursor()
    cur.execute("select name from pattern")
    rows = cur.fetchall()
    conn.close()
    return [rec[0] for rec in rows]

def write(result, pattern_name, player_name, bpm):
    conn = connect(dbname='notes')
    cur = conn.cursor()
    cur.execute(
        "insert into attempt (pattern_name, player_name, bpm, ts) " +
        "values ('{}','{}',{}, now()) returning id".format(
            pattern_name, player_name, bpm))
    #import pdb;pdb.set_trace()
    attempt_id = cur.fetchone()[0]
    for ts, diff in result['delta']:
        cur.execute("insert into delta (attempt_id, ts, diff) values ({}, {}, {})".format(
        attempt_id, ts, diff))
    for ts in result['miss']:
        cur.execute("insert into miss (attempt_id, ts) values ({}, {})".format(
        attempt_id, ts))
    for ts in result['extra']:
        cur.execute("insert into extra (attempt_id, ts) values ({}, {})".format(
        attempt_id, ts))
    conn.commit()
    conn.close()

def get_all_for_pattern(name):
    conn = connect(dbname='notes')
    cur = conn.cursor()
    cur.execute("select ts, diff from delta where attempt_id in (select id from attempt where pattern_name='{}')".format(name))
    rs = cur.fetchall()
    print(rs)
            
if __name__ == '__main__':
    wipe()
    make_schema()
    #print(get_all_for_pattern('easy-4'))

#calc which  timestamps per pattern are difficult
#fin note in song with the most errors
