from main import API

a=API()
a.setDevice('ios')
a.setOpenId('5400409')
a.setToken('y9ITTBOuBZzUxSGT7KxrkwTHIRGJekM4')
a.getWS()
a.login_and_collect()
exit(1)
#a.reroll(True)
#a.update_rating()
#a.questuntil(50)
print a.doquest(78)
#a.showallaccounts()