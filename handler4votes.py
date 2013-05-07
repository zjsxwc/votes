#coding=utf-8
import gtk
import time
import thread
import serial
import xlwt


def add_new_row(liststore):
	l=len(liststore)
	if l==0:
		liststore.append(['0','-','0',' '])
		return 0
	l-=1
	iter=liststore.get_iter(l)

	cid=liststore.get_value(iter,0)
	cid=str(1+int(cid))
	liststore.append([cid,'-','0',' '])


def clear_liststore(liststore):
	liststore.clear()

def remove_row(liststore,treeseletion):
	model,iter = treeseletion.get_selected()
	print 'model:',model
	print 'liststore:',liststore
	liststore.remove(iter)


def text_output(textbuffer,text):
	textbuffer.insert(textbuffer.get_end_iter(),'>>>  '+text)
	#textbuffer.place_cursor(textbuffer.get_end_iter())
################################          Excel output                ###########

def liststore2dic(liststore):#liststore  等价 storemodel
	dic={}
	for path in range(len(liststore)):
		iter = liststore.get_iter(path)
		for column in range(4):
			value = liststore.get_value(iter,column) 
			#print value
			if column==0:
				head=value
				dic[head]=str(value)
			else:
				dic[head]+=':'+value
		print dic
	return dic

def dic_save_to_excel(dic=None,excelname=None,):
	exfile = xlwt.Workbook()
	table = exfile.add_sheet('the_vote_stores',cell_overwrite_ok=True )

	table.write(0,0,u'编号')
	table.write(0,1,u'名字')
	table.write(0,2,u'票数')
	table.write(0,3,u'具体')

	i=1
#table.write(0,0,'test')
	for e in dic:
		row= dic[e].split(':')
		j=0
		for c in row:
			table.write(i,j,c)
			j+=1
		i+=1

	exfile.save(excelname)

def handler4excel(w,liststore,textbuffer,):
	text_output(textbuffer,'Writing to the Excel ...')
	dic=liststore2dic(liststore)
	filename='votes.xls'
	dic_save_to_excel(dic,filename)
	text_output(textbuffer,'Finish the Excel output in * %s *\n\n'%filename)




#################################################################################
def create_confDialog(button,wParent=None,ret_dic=None,treeview=None):
	d=gtk.Dialog(title='Configuration',parent=wParent,flags=0,)
	d.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
	d.add_button(gtk.STOCK_OK, gtk.RESPONSE_ACCEPT)
	d.set_size_request(200,300)
	d.set_transient_for(wParent)
	#

	#ret_dic={'isAnonymous':False,'adresses_of_handsets':'',}

	togbutton = gtk.ToggleButton("Press to Anonymous")
	togbutton.set_active(ret_dic['isAnonymous'])
	d.vbox.pack_start(togbutton,False)
	#
	hbox=gtk.HBox()
	label=gtk.Label('Handset Adresses:')
	
	hbox.pack_start(label,False)
	entryha = gtk.Entry()
	entryha.set_text(ret_dic['adresses_of_handsets'])
	hbox.pack_start(entryha,True)
	#
	d.vbox.pack_start(hbox,False)

	#
	hbox=gtk.HBox()
	label=gtk.Label('Serial Port:')
	
	hbox.pack_start(label,False)
	entrysp = gtk.Entry()
	entrysp.set_text(ret_dic['serialport'])
	hbox.pack_start(entrysp,True)
	d.vbox.pack_start(hbox,False)

	#
	hbox=gtk.HBox()
	label=gtk.Label('DB Table name:')
	
	hbox.pack_start(label,False)
	entrydbname = gtk.Entry()
	entrydbname.set_text(ret_dic['dbname'])
	hbox.pack_start(entrydbname,True)
	d.vbox.pack_start(hbox,False)


	#
	d.vbox.show_all()
	dret = d.run()
	
	if dret == gtk.RESPONSE_ACCEPT:
		ret_dic['isAnonymous']=togbutton.get_active()
		ret_dic['adresses_of_handsets']=entryha.get_text()
		ret_dic['serialport']=entrysp.get_text()
		ret_dic['dbname']=entrydbname.get_text()

	d.destroy()
	tc=treeview.get_column(3)
	print ret_dic
	if ret_dic['isAnonymous']:
		tc.set_visible(False)
	else:
		tc.set_visible(True)
	return ret_dic

##############################################串口通信按钮######################################################
def getX():
	ser.write('\x01')
	t=[]
	for i in range(23):
		tt=ser.read(1)
		t.append(tt)
	return t

def send(adr,cmd):#send(ser,adr,cmd)
#ser.write(str(adr)+str(cmd))
	time.sleep(0.1)
def get(adr):#get(ser,adr)
#x = ser.read()          # read one byte
#s = ser.read(10)        # read up to ten bytes (timeout)
	return "1 0000"  #返回 “id+空格+内容”

def thread_initialize_the_handsets(adresses_of_handsets,buttonL,textbuffer):

	#ser = serial.Serial('/dev/ttyS1', 19200, timeout=1) ser = serial.Serial('COM1', 19200, timeout=1)
	for adr in adresses_of_handsets :
		send(adr,'initialize')
		ret=get(adr)
		gtk.threads_enter()
		text_output(textbuffer,"%s:%s\n"%(str(adr),str(ret)))		
		gtk.threads_leave()

	#ser.close() 
	gtk.threads_enter()
	buttonL.set_sensitive(True)
	text_output(textbuffer,'Finish initializing the handsets\n')
	gtk.threads_leave()
	thread.exit()



def get_iter_ret(ls,cid):
	for i in range(len(ls)):
		ite = ls.get_iter(i)
		iid=ls.get_value(ite,0)
		if iid==cid:
			return ite
	return None




def thread_listen_the_handsets(adresses_of_handsets,buttonL,buttonI,textbuffer,liststore,dic):
	#ser = serial.Serial('/dev/ttyS1', 19200, timeout=1) ser = serial.Serial('COM1', 19200, timeout=1)
	print dic['serialport']
	ss=dic['serialport'].split()
	_port=ss[0]
	_port=int(_port[-1])-1
	_baudrate=int(ss[1])
	ser = serial.Serial()
	ser.port=_port
	ser.timeout=1
	ser.baudrate=_baudrate
	ser.setXonXoff(True)

	#handset_adr='\\'+'x'+port_s
	for adr in adresses_of_handsets :
		#send(adr,'listen')
		#ret=get(adr)
		ser.open()
		_addr=chr(int(adr))
		ser.write(_addr)
		stemp=''


		stt=ser.read(23)
		print "Stt: ",stt
		if len(stt)>1:
			ret=str(ord(stt[2]))+' '+stt 
		else:
			gtk.threads_enter()
			text_output(textbuffer,"%s:timeout\n"%(str(adr),))	
			gtk.threads_leave()
			ser.close()
			continue


		
		

		ser.close()
		print 'RET :  ',ret

		retsplite=ret.split()
		cid=retsplite[0]

		print liststore
		iterret=get_iter_ret(liststore,cid)

		lock=False
		if iterret==None:
			print "%s No id"%adr
			lock = True
		if not lock:

			nv=liststore.get_value(iterret,2)
			nv=int(nv)
			print nv
			nv+=1
			nv=str(nv)

			ret = '(ADV.'+adr+' votes Cand.'+ret+' )  '
			more=liststore.get_value(iterret,3)
			more+=ret

			
			gtk.threads_enter()
			text_output(textbuffer,"%s:%s\n"%(str(adr),str(ret)))	
			liststore.set_value(iterret, 3, more)
			liststore.set_value(iterret, 2, nv)
			#parse(str(ret))-->liststore  liststore.update id,adr:more  liststore to dic ,dic[id].more=
			gtk.threads_leave()

	#ser.close() 
	gtk.threads_enter()
	buttonI.set_sensitive(True)
	text_output(textbuffer,'Finish listening the handsets\n')
	gtk.threads_leave()
	thread.exit()



def button_handler_initialize_the_handsets(buttonI,buttonL,textbuffer,dic):
	adresses_of_handsets=dic['adresses_of_handsets'].split()
	buttonI.set_sensitive(False) 
	text_output(textbuffer,'Start to initialize the handsets\n')
	thread.start_new_thread(thread_initialize_the_handsets,(adresses_of_handsets,buttonL,textbuffer))



def button_handler_listen_the_handsets(buttonL,buttonI,textbuffer,liststore,dic):
	adresses_of_handsets=dic['adresses_of_handsets'].split()
	buttonL.set_sensitive(False)
	text_output(textbuffer,'Start to listen the handsets\n')
	thread.start_new_thread(thread_listen_the_handsets,(adresses_of_handsets,buttonL,buttonI,textbuffer,liststore,dic))























##############################################################################################

def helpDialog(item,wParent=None,text=None,bi=None,bL=None):
	#bL.set_sensitive(True)
	#bi.set_sensitive(True)
	d=gtk.Dialog(title='Help',parent=wParent,flags=0,)
	#d.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT)
	d.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
	d.set_size_request(200,300)
	d.set_transient_for(wParent)

	sw = gtk.ScrolledWindow()
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	sw.set_size_request(200,200)
	textview = gtk.TextView()
	textbuffer = textview.get_buffer()
	textbuffer.set_text(text)
	textview.set_editable(False)
	sw.add(textview)
	d.vbox.pack_start(sw,False)


	d.vbox.show_all()
	dret = d.run()
	d.destroy()


