from psycopg2 import connect

def make_schema():
	conn = connect(dbname='notes')
	cur = conn.cursor()
	cur.execute("create table player (id serial primary key, name varchar)")
	cur.execute("insert into player (name) values ('john')")
	cur.execute("create table pattern (id serial primary key, name varchar, beat_div int, notes boolean[])")
	cur.execute("insert into pattern (name, beat_div, notes) values ('easy-4', 4, '{1,1,1,1}')")

	cur.execute("create table attempt (pattern_id int, player_id int, bpm int)")
	cur.execute("create table delta (attempt_id int, diff int)")
	cur.execute("create table miss (attempt_id int, ts int)")
	cur.execute("create table extra (attempt_id int, ts int)")
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
	row = cur.fetchall()[0]
	conn.close()
	return (row[0], row[1])
	#return {'name': row[0], 'contents': ('beat_div': row[1], 'notes': row[2])}

def get_patterns():
	conn = connect(dbname='notes')
	cur = conn.cursor()
	cur.execute("select id, name from pattern")
	rows = cur.fetchall()
	conn.close()
	ret = {}
	for i in rows:
		ret[i[1]] = i[0]
	return ret

if __name__ == '__main__':
	wipe()
	make_schema()
	print(get_pattern('easy-4'))
