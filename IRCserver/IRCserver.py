import socket
import threading
import traceback
print "IRCserver started at port 6667"

allsocks = []
userlist = {}

class IRCserver(threading.Thread):
	
	def __init__(self, (sock, addr)):
		print "__init__"
		allsocks.append(sock)
		self.sock = sock
		self.addr = addr
		print addr
		threading.Thread.__init__(self)
		
	def run(self):
		self.sock.send("NOTICE AUTH :*** Welcome to the FaceRC network\r\n")
		self.ok = False
		while 1:
			raw_data = self.sock.recv(253)
			datas = raw_data.split("\r\n")
			for data in datas:
				if data.startswith("NICK"):
						a = data.split("\r\n")
						b = str(a[0]).split("NICK")
						print "nick = "+str(b[1]).strip()
						self.nick = str(b[1]).strip()
			
				if data.startswith("USER"):
						a = data.split("\r\n")
						b = str(a[0]).split()
						print "realname "+b[1]
						self.username = b[1]
						self.hostname = b[3]
						self.realname = b[4].strip(":")
						print "breaking"
						self.ok = True
						break
			if self.ok:
				break
			
		print "trying now"
		try:
			self.nick
			self.username
			self.hostname
			print "ALLOK"
		except NameError:
			print "uh oh"
			print traceback.print_exc()
			
		print self.nick+" is logged in with username: "+self.username+" and hostname: "+self.hostname
		userlist[str(self.nick)] = {"username":self.username, "host":self.hostname, "realname":self.realname, "socket":self.socket}
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
		for x in allsocks:
			x.send(text)
				
				
				
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 6667))
s.listen(2)
threads = []

while True:
	rh = IRCserver(s.accept())
	rh.daemon = True
	rh.start()
	threads.append(rh)