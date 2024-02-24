'''
清空csv文件
'''
import csv

def del_cap(filename):
	open('result/'+filename+'.csv','w').close()
	
del_cap('server1')
del_cap('server2')
del_cap('server3')
del_cap('server4')
