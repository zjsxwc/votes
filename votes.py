#coding=utf-8
import gtk
import gobject
import utility
from  handler4votes import *
from handler4sqlite import *

gobject.threads_init()

class UI():
	def __init__(self):

####################        MenuBar       ####################################
		window = gtk.Window(type=gtk.WINDOW_TOPLEVEL)
		window.set_title('Votes')
		window.connect('destroy',gtk.main_quit)
		window.set_size_request(600,500)
		window.set_position(gtk.WIN_POS_CENTER)
		#
		vbox = gtk.VBox()

		mb =gtk.MenuBar()
		filemenu = gtk.Menu()
		loadDB = gtk.MenuItem('LoadFromDB')
		#loadDB.connect('activate',)
		saveDB = gtk.MenuItem('SaveToDB')
		#saveDB.connect('activate',)
		exportExcelitem = gtk.MenuItem('ExportToExcel')
		listTables = gtk.MenuItem('ListTables')
		exititem = gtk.MenuItem('Exit')



		exititem.connect("activate", gtk.main_quit)

		filemenu.append(loadDB)
		filemenu.append(saveDB)
		filemenu.append(exportExcelitem)
		filemenu.append(listTables)
		filemenu.append(exititem)

		item4filemenu=gtk.MenuItem('Operate')
		item4filemenu.set_submenu(filemenu)
		mb.append(item4filemenu)

		item4help = gtk.MenuItem('Help')
		helpmenu = gtk.Menu()
		help=gtk.MenuItem('?')
	
		about = gtk.MenuItem('about')
		about.connect('activate',helpDialog,window,'''Author:\t王超\nEmail:\tzjsxwc@163.com''') 
		helpmenu.append(help)
		helpmenu.append(about)
		item4help.set_submenu(helpmenu)
		mb.append(item4help)
		mb.set_size_request(400,25)

		vbox.pack_start(mb,False)
		#
		hbox = gtk.HBox()
		vbox.pack_start(hbox,False)

#########################    ToolButton            #############################
		button = gtk.Button('Initialize')
		buttonInit = button
		#buttonXX=button
		#button.set_sensitive(False) 
		hbox.pack_start(button,False)
		button = gtk.Button('Listening')
		button.set_sensitive(False)
		buttonListen = button
		hbox.pack_start(button,False)
		#exbutton = utility.create_image_button('excel.jpg')
		#hbox.pack_start(exbutton,False)

		confbutton = gtk.Button('Configure')
		hbox.pack_end(confbutton,False)
		ret_dic={'isAnonymous':False,'adresses_of_handsets':'1','serialport':'COM3 4800','dbname':'Table_noname'}
		
########################      TreeList                     ###############################

		storemodel = gtk.ListStore(str,str,str,str)
		#storemodel.append(['-','-','','--'])
		#buttonXX.connect_object('clicked',liststore2dic,storemodel)
		sw,treeselection,treeview= utility.create_treeview_scrolledwindow(storemodel)
		sw.set_size_request(600,260)
		vbox.pack_start(sw,False)

		confbutton.connect('clicked',create_confDialog,window,ret_dic,treeview)
########################       add remove   clear           ###############################
		hbox = gtk.HBox()
		vbox.pack_start(hbox,False)
		#label = gtk.Label(' ')
		#label.set_size_request(410,4)
		#hbox.pack_start(label,False)
		button = gtk.Button('Clear')
		button.connect_object('clicked',clear_liststore,storemodel)
		hbox.pack_end(button,False)
		#
		button = gtk.Button('Remove')
		button.connect_object('clicked',remove_row,storemodel,treeselection)
		hbox.pack_end(button,False)
		#
		button = gtk.Button('Add')
		hbox.pack_end(button,False)
		button.connect_object('clicked',add_new_row,storemodel)
########################            TextView                   #################################
		sw,textview,textbuffer = utility.create_textview_scrolledwindow()
		textbuffer.set_text('Welcome to Votes!\n')
		sw.set_size_request(600,150)
		vbox.pack_start(sw,False) 
		#buttonXX.connect_object('clicked',text_output,textbuffer,'test \n')

#########################################################
		window.add(vbox)





		buttonInit.connect('clicked',button_handler_initialize_the_handsets,buttonListen,textbuffer,ret_dic)#ret_dic['adresses_of_handsets'].split()
		buttonListen.connect('clicked',button_handler_listen_the_handsets,buttonInit,textbuffer,storemodel,ret_dic)
		#exbutton.connect('clicked',handler4excel,storemodel,textbuffer)

		saveDB.connect('activate',handler_saveDB,storemodel,textbuffer,ret_dic)
		loadDB.connect('activate',handler_loadDB,storemodel,textbuffer,ret_dic)
		exportExcelitem.connect('activate',handler4excel,storemodel,textbuffer)
		listTables.connect('activate',handler_listtables,textbuffer,ret_dic)
		help.connect('activate',helpDialog,window,'''\t\t使用说明 \n本程序使用了gtk、xlwt、gobject、\npyserial、sqlite等库实现 ''',buttonInit,buttonListen) 
		window.show_all()




if __name__=='__main__':

	ui=UI()

	gtk.threads_enter()
	gtk.main()
	gtk.threads_leave()
# unfinish:

# 菜单(导入数据，导出数据库[新建数据]，help[about])
#数据库
#excel导出
#多线程 +串口-->textview输出 轮询通信  设置选择串口\波特率
#button[Initialize\Listening]按下后变灰、多线程、timeout

