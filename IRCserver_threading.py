import socket
import threading
print "IRCserver started"
channels = {}
channel_list = []
users = {}

class IRCconnection(threading.Thread):
	
	def __init__(self, (sock, addr)):
		print "__init__"
		self.sock = sock
		self.addr = addr
		threading.Thread.__init__(self)
		
	def run(self):
		self.sock.send("NOTICE AUTH :*** oh hello\r\n")
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
		users[self.nick] = {"username":self.username, "host":self.hostname, "realname":self.realname}
		print users
		self.ircmain()
	
	def ircmain(self):
		while 1:
			data = self.sock.recv(253)
			print data
			if data.find("JOIN") != -1:
				a = data.split("JOIN ")
				b = a[1].strip(":")
				c = b.replace("\r\n", "")
				self.sock.send(":"+self.nick+"!"+self.nick+"@"+self.hostname+" JOIN "+c+"\r\n")
				if c in channel_list:
					channels[c]["number"] = channels[c]["number"] + 1
					channels[c]["users_in_chan"].append(self.nick)
					pass
				else:
					self.sock.send(":localhost MODE "+c+" +nt\r\n")
					# self.channels.append({"name":c, "names": [self.nick], "modes":"+nt"})
					channels[c] = {"names":self.nick, "modes":"+nt", "users_in_chan":[self.nick], "topic":"default topic", "number":1}
				self.sock.send(":localhost 332 "+self.nick+" "+c+" :"+str(channels[c]["topic"])+"\r\n")
				derp = str(channels[c]["users_in_chan"]).strip("[]'")
				print derp
				nick = self.nick
				channel = c
				print channel
				self.sock.send(":localhost 353 FaceHunt = "+channel+" :"+str(derp).strip("'")+"\r\n")
				self.sock.send(":localhost 315 "+self.nick+" "+c+" :End of /WHO list.\r\n")
				channel_list.append(c)
				print channel_list
				print channels
				
			if data.find("LIST") != -1:
				self.sock.send("localhost 321 "+self.nick+" Channel :Users  Name\r\n")
				for x in channel_list:
					self.sock.send(":localhost 322 "+self.nick+" "+x+" "+str(channels[x]["number"])+" "+str(channels[x]["topic"])+"\r\n")

			if data.find("WHO") != -1:
				for x in channels[c]["users_in_chan"]:
					#:irc.siglost.com 352 FaceHunt #FaceHunter FaceHunter Oh.God.Why * FaceHunter G~ :0 FaceHunter
					self.sock.send(":localhost 352 "+self.nick+" "+c+" "+x+" "+users[x]["host"]+" * "+x+" H~ :0 "+users[x]["realname"]+"\r\n")
				self.sock.send(":localhost 315 "+self.nick+" "+c+" :End of /WHO list.\r\n")
			
			if data.find("NICK") != -1:
				a = data.split("\r\n")
				b = str(a[0]).split("NICK")
				print "nick = "+str(b[1]).strip()
				oldnick = self.nick
				self.nick = str(b[1]).strip()
				# :FaceHunt!~username@124DE4BB.C03EAC25.3A3F4334.IP NICK :ndsjkadn
				self.sock.send(":"+oldnick+"!"+self.username+"@"+self.hostname+" NICK :"+self.nick+"\r\n")

				
				
				
				
				
				
				
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 5050))
s.listen(2)
threads = []

while True:
    rh = IRCconnection(s.accept())
    rh.daemon = True
    rh.start()
    threads.append(rh)