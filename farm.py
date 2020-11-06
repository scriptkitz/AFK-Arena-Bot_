from main import API
from multiprocessing import Pool
from db import Database

def dorolls(t):
	token,open_id=t.split(';')
	b=API()
	b.setDevice('ios')
	b.setcmd()
	b.setOpenId(open_id)
	b.setToken(token)
	b.login_and_collect()
	#b.reroll(True)
	#b.questuntil(77)
	b.updateAccount()

if __name__ == "__main__":
	db=Database()
	res=db.getAllAccounts()
	res=['%s;%s'%(x[0],x[1]) for x in res]
	pool = Pool(processes=50)
	pool.map(dorolls,res)