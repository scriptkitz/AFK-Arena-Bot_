# -*- coding: utf-8 -*-
import requests
import json
import random
import time

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class lilithgame(object):
	def __init__(self):
		self.s=requests.Session()
		self.s.verif=False
		self.idfa=self.rndDeviceId()
		
	def log(self,msg):
		print '[%s] %s'%(time.strftime('%H:%M:%S'),msg.encode('utf-8'))

	def makeaccount(self):
		if False:	self.log('[+] our idfa:%s'%(self.idfa))
		r=self.s.post('http://app1.lilithgame.com/api/sdk/login',data={'app_id':'6241329','pack_name':'com.lilithgame.hgames.ios','idfa':self.idfa,'app_version':'1.16.03','sdk_version':'1.2.8','type':'0','app_bundle_id':'com.lilithgame.hgames.ios','player_id':self.idfa,'pass':'','lang':'2','os_version':'10.2','os_type':'ios','device_model':'iPad5,4'},verify=False)
		return json.loads(r.content)
		
	def rndHex(self,n):
		return ''.join([random.choice('0123456789ABCDEF') for x in range(n)])
	
	def rndDeviceId(self):
		s='%s-%s-%s-%s-%s'%(self.rndHex(8),self.rndHex(4),self.rndHex(4),self.rndHex(4),self.rndHex(12))
		return s
		

if __name__ == "__main__":
	a=lilithgame()
	print a.makeaccount()