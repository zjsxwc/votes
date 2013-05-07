#coding=utf-8
import gtk

def create_image_button(imagename=None):
#imagename为同目录图标名，如"excel.jpg"
	pixbufanim = gtk.gdk.PixbufAnimation(imagename)
	image = gtk.Image()
	image.set_from_animation(pixbufanim)
	button = gtk.Button()
	button.add(image)
	return button

	
def create_treeview_scrolledwindow(storemodel=None,):
# storemodel 是n个list，每个list中含m个元素，n是被投票的人数，m是某个被投票者的属性数，初拟该属性包含：
#候选者自身编号、名字、总被投票票数、拥护者编号共4个，其中拥护者编号以字符串形式表示为“1:xxx;2:xxx;3:xxx;5:xxx;”，表明手持机1、2、3、5投了该人,xxx表示相应发送的附加信息。
#	def create_storemodel():
#		storemodel = gtk.ListStore(str, str, str,str)
#		for act in actresses:
#			storemodel.append([act[0], act[1], act[2],''])
#		return storemodel
#建议storemodel 作为函数参数传递，storemodel变化会反映在sw上
	sw = gtk.ScrolledWindow()
	sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	treeview = gtk.TreeView(storemodel)
	treeview.set_rules_hint(True)
	sw.add(treeview)

	rendererText = gtk.CellRendererText()
	rendererText.set_property('editable', True)
	rendererText.connect('edited',__edited,storemodel,0)
	column = gtk.TreeViewColumn("CandidateID", rendererText, text=0)#text是storemodel的列
	column.set_sort_column_id(0)#id是排序的列
	treeview.append_column(column)

	rendererText = gtk.CellRendererText()
	rendererText.set_property('editable', True)
	rendererText.connect('edited',__edited,storemodel,1)
	column = gtk.TreeViewColumn("Name", rendererText, text=1)#text是storemodel的列
	column.set_sort_column_id(1)#id是排序的列
	treeview.append_column(column)

	rendererText = gtk.CellRendererText()
#	rendererText.set_property('editable', True)
#	rendererText.connect('edited',__edited)
	column = gtk.TreeViewColumn("Votes", rendererText, text=2)#text是storemodel的列
	column.set_sort_column_id(2)#id是排序的列
	treeview.append_column(column)

	rendererText = gtk.CellRendererText()
#	rendererText.set_property('editable', True)
#	rendererText.connect('edited',__edited)
	column = gtk.TreeViewColumn("Advocators", rendererText, text=3)#isAnonymous是 匿名开关，如果选择匿名，那么isAnonymous=4，否则=3
	column.set_sort_column_id(3)#id是排序的列
	treeview.append_column(column)


	treeselection = treeview.get_selection()
	treeselection.set_mode(gtk.SELECTION_SINGLE)

	return sw,treeselection,treeview


def __edited( cell, path, new_text,store,c):
	iter = store.get_iter(path)
	print path,iter
	store.set_value(iter, c, new_text)
	

def create_textview_scrolledwindow():
	sw = gtk.ScrolledWindow()
	sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
	textview = gtk.TextView()
	textbuffer = textview.get_buffer()
	sw.add(textview)
	textview.set_editable(False)
	return sw,textview,textbuffer
	#textbuffer.set_text(string)
