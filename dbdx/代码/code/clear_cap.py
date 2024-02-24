'''
清空cap文件
'''

import csv

def del_cap(filename):
	open('request/'+filename+'.cap','w').close()
	
del_cap('server1')
del_cap('server2')
del_cap('server3')
del_cap('server4')
