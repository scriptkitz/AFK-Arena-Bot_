# -*- coding: utf-8 -*-
from google.protobuf import text_format
from websocket import create_connection
import common_pb2
import down_pb2
import time
import base64
import os
import up_pb2
import websocket
import inspect
from lilithgame import lilithgame
from db import Database

class API(object):
	def __init__(self):
		self.cli_version="1.32"
		self.app_version="1.32.02"
		self.up_pb2=up_pb2
		self.down_pb2=down_pb2
		self.common_pb2=common_pb2
		self.seq=100
		self.lilithgame=lilithgame()
		self.db=Database()
		self.cmd=True

	def getRND(self):
		return base64.b64encode(os.urandom(16))

	def getWS(self):
		if hasattr(self,'ws'):
			self.ws.close()
		self.ws = create_connection("ws://hgame-tva-slb-gs.lilithgame.com:10000",header={'Upgrade':'websocket','Connection':'Upgrade','Sec-WebSocket-Key':self.getRND(),'Sec-WebSocket-Protocol':'game_10001','Sec-WebSocket-Version':'13'})

	def setCollectRewards(self):
		self.canrewards=True

	def setcmd(self):
		self.cmd=False
		
	def setOpenId(self,id):
		self.open_id=str(id)

	def setToken(self,token):
		self.token=token

	def setDevice(self,device):
		self.device=self.common_pb2.ios if device=='ios' else self.common_pb2.android
		self.log('[!] our OS is:%s'%(device))

	def log(self,msg):
		if hasattr(self,'cmd') and self.cmd==False:	return
		print '[%s] %s'%(time.strftime('%H:%M:%S'),msg.encode('utf-8'))
	
	def makeplain(self,i):
		return self.up_pb2.up_msg().FromString(i.decode('hex'))

	def getplainresponse(self,i):
		return self.down_pb2.down_msg().FromString(i)

	def login(self,platform,open_id,svr_id,uid,htoken):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_reconnect.platform = self.common_pb2.t_platform_lilith
		msg.req_reconnect.open_id = open_id
		msg.req_reconnect.svr_id = svr_id
		msg.req_reconnect.uid = uid
		msg.req_reconnect.htoken = htoken
		msg.req_reconnect.cli_version = self.cli_version
		return self.callAPI(msg.SerializeToString())

	def req_sdk_login(self,svr_id=False,is_debug=False):
		if not hasattr(self,'open_id'):
			self.log('[-] open_id missing...')
			exit(1)
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=1
		msg.req_sdk_login.platform = self.common_pb2.t_platform_lilith
		msg.req_sdk_login.open_id = self.open_id
		msg.req_sdk_login.token = self.token
		msg.req_sdk_login.is_debug = is_debug
		msg.sign = '11d649752599549c94edf172e1b51e2c'
		if svr_id:	msg.req_sdk_login.svr_id = svr_id
		res= self.callAPI(msg.SerializeToString())
		self.htoken=res.reply_sdk_login.htoken
		self.svr_id=res.reply_sdk_login.svr_id
		self.log('[!] using server %s'%(self.svr_id))
		if False:	self.log('htoken:%s svr_id:%s'%(self.htoken,self.svr_id))
		return res

	def req_heartbeat(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_heartbeat.hb_cnt = 0
		msg.req_heartbeat.hb_delay = 0
		msg.req_heartbeat.timeout_cnt = 0
		msg.req_heartbeat.timeout_length = 15000
		return self.callAPI(msg.SerializeToString())

	def req_tutorial(self,ids):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		for id in ids:
			msg.req_tutorial.new_tutorials.append(id)
		return self.callAPI(msg.SerializeToString())

	def query_assist_summaries(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.query_assist_summaries.Clear()
		return self.callAPI(msg.SerializeToString())

	def get_acc_users(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_acc.get_acc_users.Clear()
		return self.callAPI(msg.SerializeToString())

	def update_rating(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_rating.update_rating.status=self.common_pb2.have_rated
		msg.req_rating.update_rating.add_count=0
		msg.req_rating.update_rating.action=self.common_pb2.second_day_reward
		return self.callAPI(msg.SerializeToString())

	def next_chapter(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.next_chapter.Clear()
		return self.callAPI(msg.SerializeToString())

	def req_open_panel(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.req_open_panel.Clear()
		return self.callAPI(msg.SerializeToString())

	def req_daily_login(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_daily_login.recv_reward=1
		return self.callAPI(msg.SerializeToString())

	def recv_reward(self,challenge_id,task_id):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_challenge.recv_reward.challenge_id=challenge_id
		msg.req_challenge.recv_reward.task_id=task_id
		return self.callAPI(msg.SerializeToString())

	def req_red_dot(self,_type,id):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_red_dot.rm.type=_type
		msg.req_red_dot.rm.id=id
		return self.callAPI(msg.SerializeToString())

	def req_tavern_draw(self,tavern_id):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_tavern.req_tavern_draw.tavern_id=tavern_id
		return self.callAPI(msg.SerializeToString())

	def req_recv_todo_reward(self,req_recv_todo_reward):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_task.req_recv_todo_reward=req_recv_todo_reward
		return self.callAPI(msg.SerializeToString())

	def req_recv_chest(self,req_recv_chest):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_task.req_recv_chest=req_recv_chest
		return self.callAPI(msg.SerializeToString())

	def req_recv_line_reward(self,req_recv_line_reward):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_task.req_recv_line_reward=req_recv_line_reward
		return self.callAPI(msg.SerializeToString())

	def query_reward(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.query_reward.Clear()
		return self.callAPI(msg.SerializeToString())

	def draw_rewards(self):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.draw_rewards.Clear()
		return self.callAPI(msg.SerializeToString())

	def req_up_level(self,hero_id,up_level):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_unit.req_up_level.hero_id=hero_id
		msg.req_unit.req_up_level.up_level=up_level
		return self.callAPI(msg.SerializeToString())

	def req_wear_best_equip(self,req_wear_best_equip):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_unit.req_wear_best_equip=req_wear_best_equip
		return self.callAPI(msg.SerializeToString())

	def start_battle(self,stage_id):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.start_battle.stage_id=stage_id
		idx=0
		self.heroes.reverse()
		for h in self.heroes:
			if idx>4:	break
			if False:	self.log('slot:%s hero_id:%s'%(idx,h))
			new_lineup = msg.req_stage.start_battle.lineup.add()
			new_lineup.slot=idx+1
			new_lineup.hero_id=h
			idx+=1
		return self.callAPI(msg.SerializeToString(),True)

	def end_battle(self,battle):
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_stage.end_battle.result = self.common_pb2.victory
		rounds=msg.req_stage.end_battle.rounds.add()
		rounds.round = 1
		rounds.result = self.common_pb2.victory
		rounds.self_team.slot_heroes.MergeFrom(battle.reply_stage.start_battle.start_battle_info.input.self_teams[0].slot_heroes)
		rounds.oppo_team.Clear()
		rp=common_pb2.round_op()
		map1={}
		map1[255]=common_pb2.battle_ops()
		map1[255].ops.append(0)
		rp.operations.MergeFrom(map1)
		rounds.round_op.MergeFrom(rp)
		smap1={}
		for i in self.heroes:
			smap1[i]=common_pb2.hero_stat()
			smap1[i].hp_pct=10000
			smap1[i].mp_pct=10000
			smap1[i].param=0
			smap1[i].damage=10000
			smap1[i].kill=0
			smap1[i].heal=0
			smap1[i].defend=0
		rounds.self_stats.MergeFrom(smap1)
		pmap1={}
		pmap1[1]=common_pb2.hero_stat()
		pmap1[1].hp_pct=0
		pmap1[1].mp_pct=1061
		pmap1[1].param=0
		pmap1[1].damage=99
		pmap1[1].kill=0
		pmap1[1].heal=0
		pmap1[1].defend=332
		rounds.oppo_stats.MergeFrom(pmap1)
		msg.req_stage.end_battle.cli_ver='cli:afkarena_v1.16.04.44921;bcv:2.0'
		msg.req_stage.end_battle.param=37283
		return self.callAPI(msg.SerializeToString())

	def showtasks(self,tasks):
		for i in tasks.daily_todolists._values:
			if i.target_progress>=1 and not hasattr(i,'last_reward_time'):
				self.req_recv_todo_reward(i.id)
		for i in tasks.weekly_todolists._values:
			if i.target_progress>=1 and not hasattr(i,'last_reward_time'):
				self.req_recv_todo_reward(i.id)
		for i in tasks.line_tasklists._values:
			if i.target_progress>=1 and not hasattr(i,'last_reward_time'):
				self.req_recv_line_reward(i.line)

	def showchallanges(self,challanges):
		for i in challanges._values:
			if hasattr(i,'tasks'):
				for j in i.tasks._values:
					if j.progress>=1:
						self.recv_reward(j.challenge_id,j.task_id)

	def showunits(self,heroes):
		self.log('[!] have %s units'%(len(heroes)))
		self.heroes=[]
		used=set()
		isAllLvl1=True
		for i in heroes:
			if i.level<>1:
				isAllLvl1=False
				break
		for i in heroes:
			if i.tid in used:	continue
			if not isAllLvl1 and i.level==1:	continue
			#if i.level<50:	continue
			self.log('id:%s rank:%s level:%s quality:%s'%(i.id,i.rank,i.level,i.quality))
			self.heroes.append(i.id)
			used.add(i.tid)

	def req_login(self):
		if not hasattr(self,'device'):
			self.device=self.common_pb2.ios
		msg=self.up_pb2.up_msg()
		msg.seq=self.seq
		msg.repeat=0
		msg.req_login.platform=self.common_pb2.t_platform_lilith
		msg.req_login.os=self.device
		msg.req_login.open_id=self.open_id
		msg.req_login.svr_id=self.svr_id
		msg.req_login.htoken=self.htoken
		msg.req_login.cli_version=self.cli_version
		msg.req_login.time_zone=2
		msg.req_login.lang=self.common_pb2.en
		msg.req_login.push_id="jpush-191e35f7e00af97c8e4"
		msg.req_login.idfa="00000000-0000-0000-0000-000000000000"
		msg.req_login.google_aid=""
		msg.req_login.android_id=""
		msg.req_login.os_version="10.2"
		msg.req_login.app_version=self.app_version
		msg.req_login.device="iPad5,4"
		msg.req_login.channel_id="self-lilith-0.7"
		msg.req_login.package="com.lilithgame.hgames.ios"
		msg.req_login.name="New Player"
		msg.req_login.ip="0.0.0.0"
		msg.sign='MD5'
		res= self.callAPI(msg.SerializeToString())
		self.user=res.reply_login.user_info
		self.cur_stage=res.reply_login.user_info.stage.cur_stage
		if False:	self.log('[!] cur_stage:%s'%(self.cur_stage))
		self.showunits(res.reply_login.user_info.heroes._values)
		if hasattr(self,'canrewards'):	self.showtasks(res.reply_login.user_info.task_info)
		if hasattr(self,'canrewards'):	self.showchallanges(res.reply_login.user_info.challenges)
		self.log('uid:%s level:%s gold:%s diamonds:%s'%(res.reply_login.user_info.uid,res.reply_login.user_info.level,res.reply_login.user_info.gold,res.reply_login.user_info.rmb))
		return res

	def callAPI(self,data,needSecond=False):
		if not hasattr(self,'ws'):	self.getWS()
		self.ws.send_binary(data)
		result = self.ws.recv()
		self.seq+=1
		if self.cmd:	self.log(MessageToDict(up_pb2.up_msg().FromString(i.replace(' ','').decode('hex'))))
		res= self.getplainresponse(result)
		if self.cmd:	self.log(text_format.MessageToString(res))
		if 'err_stage_battle_gs_limit' in text_format.MessageToString(res):
			self.log('[!] Your team isnt\'t strong enough yet!')
			return None
		if needSecond:
			try:
				while(inspect.stack()[1][3] not in text_format.MessageToString(res)):
					result = self.ws.recv()
					res= self.getplainresponse(result)
			except KeyboardInterrupt:
				exit(1)
		if True:	self.log('%s(): %s'%(inspect.stack()[1][3],res.reply_seq))
		return res
		#self.ws.close()
		
	def login_and_collect(self,svr_id=False):
		self.req_sdk_login(svr_id)
		self.req_login()
		self.query_assist_summaries()
		self.req_heartbeat()
		self.query_reward()
		self.draw_rewards()
		
	def questuntil(self,max):
		if not hasattr(self,'cur_stage'):
			self.log('..missing..')
			exit(1)
		done=0
		while(done<max):
			self.doquest(self.cur_stage+done)
			done+=1
		
	def doquest(self,stage_id):
		self.log('[!] finishing quest:%s'%(stage_id))
		battle=self.start_battle(stage_id)
		if not battle:
			self.log('[!] do not have battle data..')
			return
		self.req_heartbeat()
		return self.end_battle(battle)

	def addAccountToDb(self):
		return self.db.addAccount(self.user.uid,self.user.level,self.user.gold,self.user.rmb,self.token,self.open_id)

	def updateAccount(self):
		return self.db.updateAccount(self.user.level,self.user.gold,self.user.rmb,self.open_id)

	def showallaccounts(self):
		res=self.get_acc_users()
		#for i in res.reply_acc.user_summaries._values:
		#	print i.uid
		
	def reroll(self,isNew=False):
		if not isNew:
			lilith=self.lilithgame.makeaccount()
			app_token=lilith['app_token']
			app_uid=lilith['app_uid']
			if False:	self.log('app_token:%s app_uid:%s'%(app_token,app_uid))
			self.setOpenId(str(app_uid))
			self.setToken(app_token)
			self.req_sdk_login()
			self.req_login()
		#fishy?
		self.log('[!] doing reroll..')
		self.req_tutorial([1,2,3,4,5,6,7])
		self.doquest(1)
		self.doquest(2)
		self.doquest(3)
		self.doquest(4)
		self.doquest(5)
		self.doquest(6)
		self.doquest(7)
		self.doquest(8)
		self.doquest(9)
		self.doquest(10)
		self.doquest(11)
		self.doquest(12)
		return
		#orig
		self.req_tutorial([1])
		self.query_assist_summaries()
		self.doquest(1)
		self.req_tutorial([1,2])
		self.doquest(2)
		self.req_tutorial([1,2,3])
		self.doquest(3)
		self.req_up_level(1003,1)
		self.req_wear_best_equip(1003)
		self.req_tutorial([1,2,3,4])
		self.doquest(4)
		self.req_tutorial([1,2,3,4,5])
		self.req_tutorial([1,2,3,4,5,6])
		self.doquest(5)
		self.doquest(6)
		self.req_up_level(1003,1)
		self.req_up_level(1001,5)
		self.req_up_level(1002,5)
		self.req_up_level(1000,5)
		self.doquest(7)
		self.doquest(8)
		self.req_up_level(1003,5)
		#self.doquest(9)
		self.req_up_level(1001,5)
		self.req_wear_best_equip(1001)
		self.req_wear_best_equip(1003)
		self.req_wear_best_equip(1002)
		self.req_wear_best_equip(1000)
		self.doquest(10)
		self.doquest(11)
		self.doquest(12)
		self.next_chapter()
		self.query_assist_summaries()
		self.req_open_panel()
		self.req_tutorial([1,2,3,4,5,6,7])
		self.req_tavern_draw(1)
		self.req_open_panel()
		self.req_daily_login()
		self.req_red_dot(self.common_pb2.activity,7)
		self.req_red_dot(self.common_pb2.activity,7)
		self.recv_reward(3,21)
		self.req_open_panel()
		self.req_recv_todo_reward(1)
		self.req_recv_todo_reward(4)
		self.req_recv_todo_reward(6)
		self.req_recv_chest(1)
		self.req_recv_chest(2)
		self.req_recv_line_reward(1)
		self.req_recv_line_reward(1)
		self.req_recv_line_reward(1)
		self.req_recv_line_reward(2)
		self.req_recv_line_reward(3)
		self.req_recv_line_reward(1)
		self.req_recv_line_reward(2)
		self.req_recv_line_reward(1)
		self.req_recv_line_reward(17)
		self.req_recv_line_reward(5)
		self.req_open_panel()
		self.req_tavern_draw(1)
		self.req_tavern_draw(1)
		self.req_tavern_draw(1)
		self.req_tavern_draw(1)

if __name__ == "__main__":
	a=API()
	a.setOpenId('3414156')
	a.setToken('QShls0NoQPFe2fLOkzf86PZxwCWBuF2k')
	a.login_and_collect()