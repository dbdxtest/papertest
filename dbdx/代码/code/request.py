'''
该脚本用于统计每秒钟，到指定服务器的指定端口的数据包的数量
'''

import csv
import _thread
import time
import os

#将列表[时间戳,端口号,数据包数量]写入到服务器对应的csv文件中
def write_csv(filename,data):
	with open('result/'+filename+'.csv','a',newline='') as f:
		write=csv.writer(f,dialect='excel')
		write.writerow(data)

#利用cap文件的固定格式，读取cap文件中指定端口数据包的数量
def getPktsNum(filename):
	with open('request/'+filename+'.cap','rb') as f:
		content=f.read()
	start=24
	PNum={}
	while start<len(content):
		# 防止数据包被截断
		if(start+16>len(content)):
			break
		data_len=content[start+8]+content[start+9]*256
		new_start=start+16+data_len
		# 防止数据包被截断
		if(new_start>len(content)):
			break
		#去除arp包
		if(data_len==42 and content[start+16+14+2]==8 and content[start+16+14+3]==0):
			start=new_start
			continue
		IP_start=start+16+14
		IPheader_len=(content[IP_start]-64)*4
		TCP_start=start+16+14+IPheader_len
		dst_port=content[TCP_start+2]*256+content[TCP_start+3]
		if dst_port in PNum:
			PNum[dst_port]=PNum[dst_port]+1
		else:
			PNum[dst_port]=1
		start=new_start
	return PNum

#将1s内的统计数据写入到服务器对应的csv文件中
def write(filename, PNum):
	t=int(round(time.time()*1000))
	if(PNum=={}):
		write_csv(filename,[t,0,0])
		print([t,0,0])
	else:
		for i in PNum.items():
			i_list=list(i)
			i_list.insert(0,t)
			write_csv(filename,i_list)
			print(i_list)
	write_csv(filename,[])
	print()

#针对某一服务器，对1s内的数据包进行统计
def getPNum(PNum_old,PNum_new):
	PNum={}
	for i in PNum_new.items():
		i_list=list(i)
		key=i_list[0]
		if((key in PNum_old)==True):
			PNum[key]=PNum_new[key]-PNum_old[key]
		else:
			PNum[key]=PNum_new[key]
	return PNum

#服务器主节点端口与服务器的对应关系
def match(ens):
	if(ens=='ens224'):
		filename='server1'
	elif(ens=='ens256'):
		filename='server2'
	elif(ens=='ens161'):
		filename='server3'
	else:
		filename='server4'
	return filename

#运行tcpdump命令，生成cap文件
def execCmd(ens, ip):
	filename=match(ens)
	command = "sudo tcpdump -i " + ens + " dst host " + ip +  " -w request/" + filename + ".cap" 
	os.system('echo %s | sudo -S %s' % ('jx', command))
	print(command)

#主程序，用前n秒的数据包统计数据减去前n-1秒的数据包统计数据，从而获得第n秒的统计数据
_thread.start_new_thread(execCmd, ("ens224", "100.127.61.1",))
_thread.start_new_thread(execCmd, ("ens256", "100.127.62.1",))
_thread.start_new_thread(execCmd, ("ens161", "100.127.63.1",))
_thread.start_new_thread(execCmd, ("ens193", "100.127.64.1",))
PNum1_old=getPktsNum('server1')
PNum2_old=getPktsNum('server2')
PNum3_old=getPktsNum('server3')
PNum4_old=getPktsNum('server4')
i=1
while True:
	time.sleep(1)
	print(i)
	i=i+1
	PNum1_new=getPktsNum('server1')
	PNum2_new=getPktsNum('server2')
	PNum3_new=getPktsNum('server3')
	PNum4_new=getPktsNum('server4')
	PNum1=getPNum(PNum1_old,PNum1_new)
	PNum2=getPNum(PNum2_old,PNum2_new)
	PNum3=getPNum(PNum3_old,PNum3_new)
	PNum4=getPNum(PNum4_old,PNum4_new)
	write('server1', PNum1)
	write('server2', PNum2)
	write('server3', PNum3)
	write('server4', PNum4)
	PNum1_old=PNum1_new
	PNum2_old=PNum2_new
	PNum3_old=PNum3_new
	PNum4_old=PNum4_new
	
