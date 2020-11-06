from google.protobuf.json_format import MessageToJson

import common_pb2
import down_pb2
import up_pb2

def md5(i):
	import hashlib
	m = hashlib.md5()
	m.update('df@s!h36%323&'+i)
	return m.hexdigest()

msg=up_pb2.up_msg()
msg.seq=100
msg.repeat=0
#msg.req_sdk_login.platform = 1#common_pb2.t_platform_lilith
msg.req_sdk_login.open_id = "5400409"
msg.req_sdk_login.token = "y9ITTBOuBZzUxSGT7KxrkwTHIRGJekM4"
msg.req_sdk_login.is_debug = False

jsonObj = MessageToJson(msg.req_sdk_login)
print jsonObj
print md5(jsonObj)