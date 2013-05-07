#coding=utf-8

import sqlite3
import datetime
from handler4votes import * 

def get_time():
	now = datetime.datetime.now()
	return now.strftime('Table%Y%m%d%H%M%S')



def handler_saveDB(item,liststore,textbuffer,dic):
	tablename=dic['dbname']
	text_output(textbuffer,'Writing to the DataBase Table %s ...'%tablename)
	conn = sqlite3.connect('votes.db')
	c=conn.cursor()
	
	
	c.execute('SELECT count(*) FROM sqlite_master WHERE type="table" AND name="%s"'%tablename)
	r=c.fetchone()

	if r[0]==1:
		c.execute('drop table %s'%tablename)

	c.execute("create table %s (id text, name text, votes text, more text)"%tablename)
	text_output(textbuffer,' %s is created  '%tablename)
	#c.execute("""insert into tablename values ('9','Lee','3','0x02:9 1 2 3')""")
	dic=liststore2dic(liststore)


	for e in dic:
		row= dic[e].split(':')
		format=[tablename]
		for col in row:
			format.append(col)
		c.execute("insert into %s values (\"%s\",\"%s\",\"%s\",\"%s\")"%tuple(format))


	conn.commit()
	c.close()
	conn.close()
	text_output(textbuffer,'Finish writing to the DataBase \n')

def handler_loadDB(item,liststore,textbuffer,dic):
	text_output(textbuffer,'Loading from the DataBase Table %s ...'%dic['dbname'])
	conn = sqlite3.connect('votes.db')
	c=conn.cursor()
#t = (symbol,)
#c.execute('select * from stocks where symbol=?', t)
	tablename=dic['dbname']
	c.execute('select * from %s'%tablename)
	for row in c:
		liststore.append(list(row))
	c.close()
	conn.close()
	text_output(textbuffer,'Finish loading from the DataBase \n')

def handler_listtables(item,textbuffer,dic=None):
	text_output(textbuffer,'Listing the table names ... \n')
	conn = 	sqlite3.connect('votes.db')
	c=conn.cursor()
	c.execute('select name from sqlite_master where type="table" order by name')
	fall = c.fetchall()
	#print fall
	for e in fall:
		v=e[0]+'  '
		print v
		text_output(textbuffer,v)

