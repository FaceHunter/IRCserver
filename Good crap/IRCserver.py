import socket
import threading
print "IRCserver started at port 6667"

channelmodes = []
channellist = []
alladdrs = []

userlist = []
usermodes = {}

class IRCserver(threading.Thread):
	
	def __init__(self, (sock, addr)):
		print "__init__"
		self.sock = sock
		self.addr = addr
		print addr
		threading.Thread.__init__(self)
		
	def run(self):
		self.sock.send("NOTICE AUTH :*** Welcome to the FaceRC network\r\n")
		while 1:
			raw_data = self.sock.recv(253)
			print raw_data
			if raw_data.find("NICK") != -1:
					a = raw_data.split("\r\n")
					b = str(a[0]).split("NICK")
					print "nick = "+str(b[1]).strip()
					self.nick = str(b[1]).strip()
		
			if raw_data.find("USER") != -1:
					a = raw_data.split("\r\n")
					b = str(a[1]).split()
					print "realname "+b[1]
					self.username = b[1]
					self.hostname = b[3]
					self.realname = b[4].strip(":")
			try:
				self.nick
				self.username
				self.hostname
			except NameError:
				pass
			else:
				break
		print self.nick+" is logged in with username: "+self.username+" and hostname: "+self.hostname
		usermodes[str(self.nick)] = {"username":self.username, "host":self.hostname, "realname":self.realname, "addr":self.addr}
		alladdrs.append(self.addr)
		userlist.append(self.nick)
		print userlist
		print usermodes
		self.sendtoall("NOTICE AUTH :"+self.nick+" joined the network!\r\n")
		self.ircmain()
	
	def ircmain(self):
		print "entering main"
		while 1:
			data = self.sock.recv(253)
			print data


				
				
				
	def sendtoall(self, text):
		for x in alladdrs:
			sockets = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			print x[0]
			print x[1]
			sockets.sendto(text, (x[0],x[1]))
				
				
				
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6667))
s.listen(2)
threads = []

while True:
	rh = IRCserver(s.accept())
	rh.daemon = True
	rh.start()
	threads.append(rh)
	print threads