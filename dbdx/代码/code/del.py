'''
kill运行request脚本启动的所有进程
'''

import os
import _thread

#kill tcpdump进程
def delTcpdump(filename):
	pid1=os.popen('ps -ef | grep '+filename + ".cap")
	pid2=pid1.read().split()[42]
	command="sudo kill " + pid2
	os.system('echo %s | sudo -S %s' % ("jx", command))
	print(command)

#kill request进程
def delRequest():
	pid1=os.popen('ps -ef | grep request.py')
	pid2=pid1.read().split()[1]
	command="sudo kill " + pid2
	os.system('echo %s | sudo -S %s' % ("jx", command))
	print(command)

delTcpdump("server1")
delTcpdump("server2")
delTcpdump("server3")
delTcpdump("server4")
delRequest()
