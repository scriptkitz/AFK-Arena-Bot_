from main import API

a=API()
a.setDevice('ios')
a.setOpenId('5189683')
a.setToken('0V36drBk4KzR1tG6QpFCUu5tzxACZ0RY')
a.login_and_collect(126)
#a.reroll(True)
#a.update_rating()
#a.questuntil(50)
print a.doquest(86)
#a.showallaccounts()