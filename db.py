# -*- coding: utf-8 -*-
import sqlite3
import os.path

class Database(object):
	def __init__(self):
		self.sqlite_file='accounts.db'
		if not os.path.isfile(self.sqlite_file):
			self.createDb()

	def createDb(self):
		conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()
		c.execute('''CREATE TABLE "data" ("uid"	INTEGER NOT NULL,"level"	INTEGER NOT NULL,"gold"	INTEGER NOT NULL,"rmb"	INTEGER NOT NULL,"app_token"	TEXT NOT NULL,"app_uid"	INTEGER NOT NULL,PRIMARY KEY("app_token","app_uid"));''')
		conn.commit()
		conn.close()

	def addAccount(self,uid,level,gold,rmb,app_token,app_uid):
		conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()
		c.execute("INSERT OR IGNORE INTO data (uid,level,gold,rmb,app_token,app_uid) VALUES (%s,%s,%s,%s,'%s',%s)"%(int(uid),int(level),int(gold),int(rmb),app_token,int(app_uid)))
		conn.commit()
		conn.close()

	def updateAccount(self,level,gold,rmb,app_uid):
		conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()
		c.execute("UPDATE data SET level=%s,gold=%s,rmb=%s where app_uid='%s'"%(int(level),int(gold),int(rmb),app_uid))
		conn.commit()
		conn.close()

	def getAccount(self,udid):
		conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()
		c.execute("select * from data where app_uid='%s'"%(udid))
		all_rows = c.fetchall()
		conn.close()
		return all_rows

	def getAllAccounts(self,limit=None):
		conn = sqlite3.connect(self.sqlite_file)
		c = conn.cursor()
		if limit:
			c.execute("select app_token,app_uid from data where rmb>%s"%(limit))
		else:
			c.execute("select app_token,app_uid from data")
		all_rows = c.fetchall()
		conn.close()
		return all_rows

if __name__ == '__main__':
	db=Database()
	db.createDb()