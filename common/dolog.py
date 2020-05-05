# coding=UTF-8
import time
print("日志模块加载成功--dolog.py")
def log(func='',title='',count='',text='',bug=''):
	filename = 'log.txt'
	date = time.strftime("%Y-%m-%d %H:%M:%S")
	with open(filename, 'a') as file_object:
		file_object.write(date)
		file_object.write("\n")
		file_object.write("--- %s --- %s --- %s\n <--%s--> \n_error_log:\n%s\n*******************************\n" %(str(func),str(title),str(count),str(text),str(bug)))
	file_object.close()