'''
SMTP Mail Client
Authors: Ben Liepert & Gezim Saciri
'''

import socket
import sys
from tkinter import *

def RunClient(lTo, sFrom, lCCs, lBCCs, sSubject, sBody):
	'''
	Parameters: lTo: the destination address(es), sFrom: the source address, lCCs: The CC address(es)
		lBCCS: The BCC address(es), sSubject: The subject text, sBody: The text body
	Function: This function handles the initalization of the host and port number, and calls
		subsequent funcitons in order to establish a connection with the SMTP server and send
		an email to it
	Returns: Nothing
	'''
	host = 'mail.denison.edu' # server host
	port = 25 			      # SMTP port
	socket = EstablishConnection(host,port)

	SendHELO('saciri_g1', socket)
	SendMAIL_FROM(sFrom, socket)
	SendRCPT_TO(lTo, lCCs, lBCCs, socket)
	SendDATA(socket)
	SendBody(lTo, sFrom, lCCs, lBCCs, sSubject, sBody, socket)

	socket.close()

def EstablishConnection(host, port):
	'''
	Parameters: host: The host address of the SMTP server, port: The port number for the SMTP server
	Function: A connection will be attempted with the host and port number, and the response code
		from the server will be printed
	Returns: The connection to the socket
	'''
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server = (host, port)
	s.connect(server)
	data = s.recv(100).decode()
	HandleResponse(data)
	return s

def SendHELO(sHostName,s):
	'''
	Parameters: sHostName: The email address we are sending the email from, s: The socket connection
	Function: The client will now send a HELO message in compliance with SMTP protocol and will print
		out the response from the server
	Returns: Nothing
	'''
	sHELO = "HELO "
	sMessage = sHELO + sHostName + "\n"
	s.sendall(sMessage.encode())
	data = s.recv(100).decode()
	HandleResponse(data)

def SendMAIL_FROM(sTo,s):
	'''
	Parameters: sTo: The email address that we are sending the email from, s: The socket connection
	Function: The client will now send the MAIL FROM:_ message and print out the response code from
		the server
	Returns: Nothing
	'''
	sRCPT= "MAIL FROM: "
	sMessage = sRCPT + sTo + "\n"
	s.sendall(sMessage.encode())
	data = s.recv(100).decode()
	HandleResponse(data)

def SendRCPT_TO(lTo, lCCs, lBCCs, s):
	'''
	Parameters: lTo: A list of the email address(es) that the mail is sent to
	lCCs: A list of the email address(es) that are CC'd, lBCCs: A list of the
	email address(es) that are BCC'd, s: The socket connection
	Function: The client will now send the RCPT TO:_ message for every address and print out
		the response code from the server
	Returns: Nothing
	'''
	lRecipients = lTo + lCCs + lBCCs
	for address in lRecipients:
		sMessage = "RCPT TO: " + address + "\n"
		s.sendall(sMessage.encode())
		data = s.recv(100).decode()
		HandleResponse(data)

def SendDATA(s):
	'''
	Parameters: s: The socket connection
	Function: This function sends DATA\n, which tells the server that the message body
		is about to be sent.
	Returns: Nothing
	'''
	sMessage = "DATA\n"
	s.sendall(sMessage.encode())
	data = s.recv(100).decode()
	HandleResponse(data)

def SendBody(lTo, sFrom, lCCs, lBCCs, sSubject, sBody, s):
	'''
	Parameters: lTo: The address the message is being sent to, sFrom: The address
		the message is being sent from lCCs: The CC address(es) lBCCs: The BCC address(es)
		sSubject: The subject line of the email, sBody: The text of the email message
		s: The socket connection
	Function: This function sends the message body, which includes the CC's, BCC's, the subject
		and the actual message, then prints the response code
	Returns: Nothing
	'''
	sMessage = 'From: "" <' + sFrom + ">\n"

	# Build 'To' header. Should be of the format 'To: "" <email@random.org>, "" <email2@random.org>' etc.
	sMessage += 'To: "" <'
	for i in range(len(lTo)-1):
		sMessage += lTo[i] + '>, "" <'
	sMessage += lTo[-1] + '>\n'

	# Build 'CC' header in the same was the 'To' header was built above.
	if len(lCCs) > 0:
		sMessage += 'CC: "" <'
		for i in range(len(lCCs)-1):
			sMessage += lCCs[i] + '>, "" <'
		sMessage += lCCs[-1] + '>\n'

	# BCC's do not require a header in the SMTP protocol, they are only listed in 'RCPT TO:' commands earlier on.

	sMessage += "subject: " + sSubject + "\n"
	sMessage += sBody + "\n.\n"
	s.sendall(sMessage.encode())
	data = s.recv(100).decode()
	HandleResponse(data)

def HandleResponse(data):
	'''
	Parameters: data: The response code from the server
	Function: This function will analyze the response code and print out the
		corresponding message for that code, or just give a general error
	Returns: Nothing
	'''
	lData = data.split()
	sResponseCode = lData[0]

	if sResponseCode == '220':
		print("220: Connection Established")
	elif sResponseCode == "221":
		print("221: Incorrect message handling, closing connection")
	elif sResponseCode == "250":
		print("250: Requested action OK")
	elif sResponseCode == "354":
		print("354: Begin message input")
	elif sResponseCode == "501":
		print("501: Incorrect message syntax, please check host or port number")
	elif sResponseCode == "554":
		print("504: Transaction failed, please retry")
	else:
		print("Unexpected error, please try again. Response code: %s" % sResponseCode)

class MyFirstGUI:
	def __init__(self, master):
		'''
		Parameters: self, master
		Function: This initalizes the GUI with several fields to input user data
		Returns: Nothing
		'''
		self.master = master
		master.title("SMTP Client")

		self.info_Label = Label(master, text = "Please separate multiple To/CC/BCC addresses with space. ").grid(row=0, column=1, sticky = 'SW')

		self.to_Label = Label(master, text = "To: ").grid(row=1, column=0, sticky = 'SW')

		self.to_Entry = Entry(master, width = 70)
		self.to_Entry.grid(row=1,column=1, padx=(10,15))

		self.from_Label = Label(master, text = "From: ").grid(row=2, column=0, sticky = 'SW')

		self.from_Entry = Entry(master, width = 70)
		self.from_Entry.grid(row=2,column=1, padx=(10,15))

		self.cc_label = Label(master, text = "CC: ").grid(row=3, column=0, sticky = 'SW')

		self.cc_Entry = Entry(master, width = 70)
		self.cc_Entry.grid(row=3,column=1, padx=(10,15))

		self.bcc_Label = Label(master, text = "BCC: ").grid(row=4, column=0, sticky = 'SW')

		self.bcc_Entry = Entry(master, width = 70)
		self.bcc_Entry.grid(row=4,column=1, padx=(10,15))

		self.subject_Label = Label(master, text = "Subject: ").grid(row=5, column=0, sticky = 'SW')

		self.subject_Entry = Entry(master, width = 70)
		self.subject_Entry.grid(row=5,column=1, padx=(10,15))

		self.body_Label = Label(master, text = "Body: ").grid(row=6, column=0, sticky = 'SW')

		self.body_text = Text(master)#, width = 75)
		self.body_text.grid(row=6,column=1, padx = (10,15))

		self.clear_button = Button(master, text="Clear All", command=self.clear).grid(row=7,column=1, padx =  (0,495))
		self.send_button = Button(master, text="Send", command=self.send).grid(row=7,column=1, padx =  (500,0))

	def clear(self):
		'''
		Parameters: self
		Function: When the clear button is clicked, it clears the input of the
			text boxes in the UI
		Returns: Nothing
		'''
		self.from_Entry.delete(0,END)
		self.to_Entry.delete(0, END)
		self.from_Entry.delete(0, 'end')
		self.cc_Entry.delete(0, 'end')
		self.bcc_Entry.delete(0, 'end')
		self.subject_Entry.delete(0, 'end')
		self.body_text.delete(1.0,END)

	def send(self):
		'''
		Parameters: self
		Function: When the send button is clicked, it enters the input for each
			box into the program
		Returns: Nothing
		'''
		sTo = self.to_Entry.get()
		sFrom = self.from_Entry.get()
		sCC = self.cc_Entry.get()
		sBCC = self.bcc_Entry.get()
		sSubject = self.subject_Entry.get()
		sBody = self.body_text.get(1.0,END)

		lTo = sTo.split()
		lCCs = sCC.split()
		lBCCs = sBCC.split()

		if(len(lTo) < 1):
			self.NoTo()

		elif(len(sFrom.split()) > 1):
			# tried to put more than one email in 'from' line
			self.TooManyFrom()

		elif(len(sFrom.split()) != 1):
			# tried to put no email in 'from' line
			self.NoFrom()

		else:
			RunClient(lTo, sFrom, lCCs, lBCCs, sSubject, sBody)

	def NoTo(self):
		print("You forgot a 'To' address!")

	def TooManyFrom(self):
		print("Too many 'from' addresses!")

	def NoFrom(self):
		print("You forgot the 'from' address!")

def RunUI():
	'''
	Parameters: none
	Function: This runs the GUI by calling subsequent functions
	Returns: Nothing
	'''
	root = Tk()
	root.grid_columnconfigure(0, weight=1)
	root.geometry('{}x{}'.format(650, 500))
	root.resizable(width=False, height=False)
	my_gui = MyFirstGUI(root)
	root.mainloop()

def main():
	#RunUI()

	#RunClient(lTo, sFrom, lCCs, lBCCs, sSubject, sBody):
	# TESTING
	to = "saciri_g1@denison.edu"
	From = "liepert_b1@denison.edu"
	subject = "I'm sorry"
	message = "message"
	RunClient([to], From , [], [], subject, message)

main()
