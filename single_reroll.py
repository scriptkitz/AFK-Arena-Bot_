from main import API
from multiprocessing import Pool

def dorolls(t=''):
	a=API()
	a.setDevice('ios')
	a.reroll()
	a.update_rating()
	b=API()
	b.setDevice('ios')
	b.setOpenId(a.open_id)
	b.setToken(a.token)
	b.login_and_collect()
	b.addAccountToDb()

if __name__ == "__main__":
	dorolls()