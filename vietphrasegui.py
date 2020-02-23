#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
import Pmw
import os
import chinesetext
import cStringIO
import time
import shutil

class Vietphrase:
    def __init__(self, parent):
        self.master = parent         # store the parent
        top = Frame(parent)          # frame for all class widgets
        top.pack(side='top')         # pack frame in parent's window
        font = 'times 16 bold'
        default_chinese_text_file = "chinese.txt"
        self.chinese_text_file = default_chinese_text_file
        self.master.bind('<Control-o>', self.open_chinese_text_file)
        self.master.bind('<Control-O>', self.open_chinese_text_file)
        self.master.bind('<Control-p>', self.control_p)
        self.master.bind('<Control-n>', self.control_n)
        self.master.bind('<Control-P>', self.up)
        self.master.bind('<Control-N>', self.down)
        self.master.bind('<Control-f>', self.next) # forward
        self.master.bind('<Control-b>', self.previous) # back
#        self.master.bind('<Control-F>', self.next) # forward
#        self.master.bind('<Control-B>', self.previous) # back
        self.master.bind('<Right>', self.next)
        self.master.bind('<Left>', self.previous)
        self.master.bind('<Control-c>', self.focus_to_chinese_combination)
        self.master.bind('<Control-C>', self.focus_to_chinese_combination)
#Balloon Help
        self.tooltip = Pmw.Balloon(self.master)
#
        top_part = Frame(top)        
        top_part.pack(side='top')   
#
        left_top_part = Frame(top_part)        
        left_top_part.pack(side='left')
        info_text_label = Label(left_top_part, text="Thông tin phụ trợ: text tiếng Trung, dữ liệu tra từ điển, clipboard để dịch...")
        info_text_label.pack(side='top', fill='x')
        self.info_text = Pmw.ScrolledText(left_top_part, text_width=85, text_height=7, vscrollmode='static', hscrollmode='none', text_font='times 14')
        self.info_text.pack(side='top')
        self.info_text.importfile(self.chinese_text_file)
        self.tooltip.bind(self.info_text, "Bấm Ctrl-N/Ctrl-P để cuộn xuống/lên thông tin ở đây!")
        chinesetext.import_data()
        self.chap = chinesetext.refine_chinese_text(content=self.info_text.getvalue().encode('utf-8'))
        self.num_of_pars = len(self.chap.paragraphs)
#
        right_top_part = Frame(top_part)        
        right_top_part.pack(side='left')
#
        open_chinese_text_file_button = Button(right_top_part, text="Open", command=self.open_chinese_text_file)
        open_chinese_text_file_button.pack(side='top', fill='x')
        self.tooltip.bind(open_chinese_text_file_button, "Chương trình mặc định lấy text tiếng Trung từ 'chinese.txt' - Ctrl-O")
#
        paste_clipboard_button = Button(right_top_part, text="Manipulate\nclipboard", command=self.use_clipboard)
        paste_clipboard_button.pack(side='top', fill='x')
        self.tooltip.bind(paste_clipboard_button, "Paste clipboard vào 'Thông tin phụ trợ', 'chương hóa' clipboard, lưu thông tin phụ trợ vào tệp 'chinese.txt'")
#
#        save_info_text_button = Button(right_top_part, text="Save ", command=self.save_info_text)
#        save_info_text_button.pack(side='top', fill='x')
#        self.tooltip.bind(save_info_text_button, "Lưu 'Thông tin phụ trợ' vào tệp 'chinese.txt' - Ctrl-S")
#        self.master.bind('<Control-s>', self.save_info_text)
        backup_vietphrase_button = Button(right_top_part, text="Save ", command=self.backup_vietphrase)
        backup_vietphrase_button.pack(side='top', fill='x')
        self.tooltip.bind(backup_vietphrase_button, "Back up vietphrase - Ctrl-S")
        self.master.bind('<Control-s>', self.backup_vietphrase)
#
        save_as_button = Button(right_top_part, text="Save as", command=self.save_as)
        save_as_button.pack(side='top', fill='x')
        self.master.bind('<Control-S>', self.save_as)
        self.tooltip.bind(save_as_button, "Lưu các đoạn đang dịch lại - Ctrl-Shift-S")
#
        bottom_part = Frame(top)        
        bottom_part.pack(side='top')   
#
        left_bottom_part = Frame(bottom_part)        
        left_bottom_part.pack(side='left')
        self.par_selector = Pmw.Counter(left_bottom_part,
                labelpos='n', label_text='Đoạn hiện tại\ntrên tổng số đoạn:', entry_width=3,
                entryfield_value=1,
                entryfield_modifiedcommand=self.par_changed,
                entryfield_validate={'validator' : 'integer',
                                       'min' : 1, 'max' : 999})                
        self.par_selector.pack(side='top')
#
        self.cc_for_vp_text = Pmw.EntryField(left_bottom_part, labelpos='n', label_text="Chinese combination", modifiedcommand=self.show_all_ccombis, entry_font='times 16', entry_foreground='red')
        self.cc_for_vp_text.pack(side='top', fill='x')
        self.vp_of_cc_text = Pmw.EntryField(left_bottom_part, labelpos='n', label_text="Vietphrase for\nChinese combination", entry_font='times 16', entry_foreground='blue')
        self.vp_of_cc_text.pack(side='top', fill='x')
#
        self.addvp_button = Button(left_bottom_part, text="Thêm entry vietphrase", command=self.add_vietphrase_entry)
        self.addvp_button.pack(side='top', fill='x')
        self.addvp_button.bind('<Return>', self.add_vietphrase_entry)
        self.master.bind('<Control-a>', self.add_vietphrase_entry)
        self.master.bind('<Control-A>', self.add_vietphrase_entry)
        self.tooltip.bind(self.addvp_button, "Ctrl-A")
#
        self.add_proper_name_button = Button(left_bottom_part, text="Thêm tên riêng ứng với\nHán-Việt của cụm tiếng Trung", command=self.add_proper_name, bg='red')
        self.add_proper_name_button.pack(side='top', fill='x')
#
        self.add_relative_name_button = Button(left_bottom_part, text="Thêm tên gọi quan hệ", command=self.add_relative_name, bg='white')
        self.add_relative_name_button.pack(side='top', fill='x')
        self.add_relative_name_button.bind('<Return>', self.add_relative_name)
        self.master.bind('<Control-r>', self.add_relative_name)
        self.tooltip.bind(self.add_relative_name_button, "Ctrl-R")
        
#
        self.add_vietphrase_hanviet_button = Button(left_bottom_part, text="Thêm vietphrase ứng với\nhán-việt của cụm tiếng Trung", command=self.add_vietphrase_hanviet, bg='yellow')
        self.add_vietphrase_hanviet_button.pack(side='top', fill='x')
        self.add_vietphrase_hanviet_button.bind('<Return>', self.add_vietphrase_hanviet)
        self.master.bind('<Control-h>', self.add_vietphrase_hanviet)
        self.tooltip.bind(self.add_vietphrase_hanviet_button, "Ctrl-H")        
#
        self.add_proper_name_button.pack(side='top', fill='x')
        self.add_proper_name_button.bind('<Return>', self.add_proper_name)
        self.master.bind('<Control-H>', self.add_proper_name)
        self.tooltip.bind(self.add_proper_name_button, "Ctrl-Shift-H")        
#
        self.updatevp_button = Button(left_bottom_part, text="Cập nhật entry vietphrase", command=self.update_vietphrase_entry)
        self.updatevp_button.pack(side='top', fill='x')
        self.updatevp_button.bind('<Return>', self.update_vietphrase_entry)
        self.master.bind('<Control-u>', self.update_vietphrase_entry)
        self.tooltip.bind(self.updatevp_button, "Ctrl-U")
#
        self.check_dics_button = Button(left_bottom_part, text="Tra từ điển Thiều Chửu\nLạc Việt, Chinese-English", command=self.check_dics)
        self.check_dics_button.pack(side='top', fill='x')
        self.check_dics_button.bind('<Return>', self.check_dics)
        self.master.bind('<Control-d>', self.check_dics)
        self.tooltip.bind(self.check_dics_button, "Ctrl-D")        
#
        self.check_tc_data_button = Button(left_bottom_part, text="Tra Thiều Chửu", command=self.check_tc_data)
        self.check_tc_data_button.pack(side='top', fill='x')
        self.check_tc_data_button.bind('<Return>', self.check_tc_data)
#
        self.check_lv_data_button = Button(left_bottom_part, text="Tra Lạc Việt", command=self.check_lv_data)
        self.check_lv_data_button.pack(side='top', fill='x')
        self.check_lv_data_button.bind('<Return>', self.check_lv_data)
#
        self.check_ce_data_button = Button(left_bottom_part, text="Tra Chinese-English", command=self.check_ce_data)
        self.check_ce_data_button.pack(side='top', fill='x')
        self.check_ce_data_button.bind('<Return>', self.check_ce_data)
#        
        right_bottom_part = Frame(bottom_part)        
        right_bottom_part.pack(side='left')   
#
        chinese_par_label = Label(right_bottom_part, text="Tiếng Trung")
        chinese_par_label.pack(side='top')
        self.chinese_par_text = Pmw.ScrolledText(right_bottom_part, text_width=60, text_height=3, vscrollmode='static', hscrollmode='none', text_font='times 16', text_foreground='red')
        self.chinese_par_text.pack(side='top')
        self.tooltip.bind(self.chinese_par_text, "Bấm Ctrl-Shift-N/P để cuộn xuống/lên thông tin ở đây!")
#
        vietphrase_par_label = Label(right_bottom_part, text="Vietphrase")
        vietphrase_par_label.pack(side='top')
        self.vietphrase_par_text = Pmw.ScrolledText(right_bottom_part, text_width=60, text_height=4, vscrollmode='static', hscrollmode='none', text_font='times 16', text_state='disable', text_foreground='blue')
        self.vietphrase_par_text.pack(side='top')
        self.tooltip.bind(self.vietphrase_par_text, "Bấm Ctrl-Shift-N/P để cuộn xuống/lên thông tin ở đây!")
#
        hanviet_par_label = Label(right_bottom_part, text="Hán Việt")
        hanviet_par_label.pack(side='top')
        self.hanviet_par_text = Pmw.ScrolledText(right_bottom_part, text_width=60, text_height=3, vscrollmode='static', hscrollmode='none', text_foreground='red', text_font='times 16 italic')
        self.hanviet_par_text.pack(side='top')
        self.tooltip.bind(self.hanviet_par_text, "Bấm Ctrl-Shift-N/P để cuộn xuống/lên thông tin ở đây!")
#
        vietphrase_hanviet_par_label = Label(right_bottom_part, text="Vietphrase {Hán Việt}")
        vietphrase_hanviet_par_label.pack(side='top')
        self.vietphrase_hanviet_par_text = Pmw.ScrolledText(right_bottom_part, text_width=60, text_height=6, vscrollmode='static', hscrollmode='none', text_font='times 16')
        self.vietphrase_hanviet_par_text.pack(side='top')
        self.tooltip.bind(self.vietphrase_hanviet_par_text, "Bấm Ctrl-Shift-N/P để cuộn xuống/lên thông tin ở đây!")
#
        parnum = chinesetext.readparnum()
        self.par_selector.component('entryfield').setvalue(str(parnum))
        self.update_num_of_par(); self.par_changed()

    def open_chinese_text_file(self, event=None):
        self.chinese_text_file = str(tkFileDialog.askopenfilename(initialdir=".", title="Mở tệp chứa text tiếng Trung", filetypes=(("Text files", "*.txt"), ("All files", "*"))))
        if (self.chinese_text_file != "") and (self.chinese_text_file != "()"): #Lần đầu gọi askopenfilename bấm Cancel thì trả ra tuple (), lần 2 thì trả string "" 
            self.info_text.clear()
            self.info_text.importfile(self.chinese_text_file)
            self.chaptermize_info_text()

    def chaptermize_info_text(self, event=None):
        self.chap = chinesetext.refine_chinese_text(content=self.info_text.getvalue().encode('utf-8'))
        self.num_of_pars = len(self.chap.paragraphs)
        self.update_num_of_par()
        self.par_changed()

    def save_info_text(self, event=None):
        filename = 'chinese.txt'
        fout = open(filename,'w')
        fout.write(self.info_text.getvalue().encode('utf-8'))
        fout.close()
        
    def save_as(self, event=None):
        content = '\n'.join(self.chap.paragraphs)
        filename = str(tkFileDialog.asksaveasfilename(initialdir=".", title="Lưu text tiếng Trung đang dịch", filetypes=(("Text files", "*.txt"), ("All files", "*"))))
        if (filename != "") and (filename != "()"):
            fout = open(filename,'w'); fout.write(content); fout.close()
        
    def update_num_of_par(self):
        self.par_selector.configure(entryfield_validate = {'validator' : 'integer',
                                                           'min' : 1, 'max' : self.num_of_pars})
        self.par_selector.configure(label_text='Đoạn hiện tại\ntrên tổng số %s đoạn:' % self.num_of_pars)

    def par_changed(self, event=None):
        try:
            current_par_num = int(self.par_selector.component('entryfield').getvalue())-1
            if current_par_num >= self.num_of_pars:
                current_par_num = 0
        except:
            current_par_num = 0
        self.par_selector.component('entryfield').setvalue(str(current_par_num+1))
        chinese_par_text = self.chap.paragraphs[current_par_num]
        self.chinese_par_text.setvalue(chinese_par_text)
        self.hanviet_par_text.setvalue(self.chap.cn_to_hanviet(chinese_par_text))
        chinesetext.vpdebug = True
        self.vietphrase_hanviet_par_text.setvalue(self.chap.cn_to_vietphrase(chinese_par_text))
        chinesetext.vpdebug = False
        self.vietphrase_par_text.setvalue(self.chap.cn_to_vietphrase(chinese_par_text))
        #save the "end" index of vietphrase_par_text for keyboard scrolling
        self.vietphrase_par_text_end = int(self.vietphrase_par_text.component('text').index("1.end")[2:])

    def action_displaying_in_info_text(self, cc, vp, action="chinesetext.add_vietphrase_entry(cc, vp)"):
# https://stackoverflow.com/questions/22822267/python-capture-print-output-of-another-module/22823751
# for python3 :(
#        f = io.StringIO()
#        with contextlib.redirect_stdout(f):
#            chinesetext.add_vietphrase_entry(cc, vp)
#        output = f.getvalue()
        stdout_ = sys.stdout #Keep track of the previous value.
        stream = cStringIO.StringIO()
        sys.stdout = stream
        eval(action)
        sys.stdout = stdout_
        output = stream.getvalue()
        self.info_text.setvalue(output)
    
    def add_vietphrase_entry(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8'); vp = self.vp_of_cc_text.getvalue().encode('utf-8')
#
        action = "chinesetext.add_vietphrase_entry(cc, vp)"
        self.action_displaying_in_info_text(cc, vp, action)
        self.actualize()

    def add_proper_name(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        vp = chinesetext.VnText(self.chap.cn_to_hanviet(cc)).to_proper_name()
        action = "chinesetext.add_vietphrase_entry(cc, vp)"
        self.action_displaying_in_info_text(cc, vp, action)
        self.actualize()

    def add_vietphrase_hanviet(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        vp = chinesetext.hanviet_combi(cc)
#        chinesetext.add_vietphrase_entry(cc, vp)
        action = "chinesetext.add_vietphrase_entry(cc, vp)"
        self.action_displaying_in_info_text(cc, vp, action)
        self.actualize()

    def add_relative_name(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        vp = self.chap.cn_to_hanviet(cc)
#        chinesetext.add_vietphrase_entry(cc, vp)
        action = "chinesetext.add_vietphrase_entry(cc, vp)"
        self.action_displaying_in_info_text(cc, vp, action)
        self.actualize()

    def update_vietphrase_entry(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8'); vp = self.vp_of_cc_text.getvalue().encode('utf-8')
        action = "chinesetext.update_vietphrase_entry(cc, vp)"
        self.action_displaying_in_info_text(cc, vp, action)
        self.actualize()

    def actualize(self, event=None):
        chinesetext.import_data()
        self.chap.update_data()
        self.par_changed()
    
    def show_all_ccombis(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        self.info_text.setvalue(self.chap.show_all_ccombis(cc))
        
    def clear_info_text(self, event=None):
        self.info_text.clear()

    def check_dics(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        self.info_text.setvalue(chinesetext.check_dics(cc))
        
    def check_tc_data(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        self.info_text.setvalue(chinesetext.check_tc_data(cc))
        
    def check_lv_data(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        self.info_text.setvalue(chinesetext.check_lv_data(cc))
        
    def check_ce_data(self, event=None):
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        self.info_text.setvalue(chinesetext.check_ce_data(cc))
        
    def up(self, event=None):
        self.chinese_par_text.component('text').yview_scroll(-1, "units")
        self.vietphrase_par_text.component('text').yview_scroll(-1, "units")
        self.hanviet_par_text.component('text').yview_scroll(-1, "units")
        self.vietphrase_hanviet_par_text.component('text').yview_scroll(-1, "units")

    def control_p(self, event=None):
        self.info_text.component('text').yview_scroll(-1, "units")
    
    def control_n(self, event=None):
        self.info_text.component('text').yview_scroll(1, "units")
    
    def down(self, event=None):
        self.chinese_par_text.component('text').yview_scroll(1, "units")
        self.vietphrase_par_text.component('text').yview_scroll(1, "units")
        self.hanviet_par_text.component('text').yview_scroll(1, "units")
        self.vietphrase_hanviet_par_text.component('text').yview_scroll(1, "units")
    
    def next(self, event=None):
        current_par_num = int(self.par_selector.component('entryfield').getvalue())
        if current_par_num == self.num_of_pars:
            self.par_selector.component('entryfield').setvalue("1")
        else:
            self.par_selector.increment()

    def focus_to_chinese_combination(self, event=None):
        self.cc_for_vp_text.clear()
        clip_text = self.master.clipboard_get()
        self.cc_for_vp_text.setvalue(clip_text)
        cc = self.cc_for_vp_text.getvalue().encode('utf-8')
        tmp = self.chap.show_vietphrase(cc)
        self.vp_of_cc_text.setvalue(tmp)
        self.vp_of_cc_text.component('entry').focus_set()
        self.vp_of_cc_text.component('entry').xview_moveto(1.0)
        
    def paste_clipboard(self, event=None):
        clip_text = self.master.clipboard_get()
        self.info_text.setvalue(clip_text)

    def use_clipboard(self, event=None):
        self.paste_clipboard()
        self.chaptermize_info_text()
        self.save_info_text()
        self.par_selector.component('entryfield').setvalue("1")

    def previous(self, event=None):
        current_par_num = int(self.par_selector.component('entryfield').getvalue())
        if current_par_num == 1:
            self.par_selector.component('entryfield').setvalue(str(self.num_of_pars))
        else:
            self.par_selector.decrement()
        
    def quit(self, event=None):
#save current paragraph
        current_par_num = int(self.par_selector.component('entryfield').getvalue())
        ofile = open('parnum','w'); ofile.write("%s\n" % current_par_num); ofile.close()
        print "Chuan bi thoat"
        print current_par_num
        #call parent's quit
#        self.master.quit()

    def backup_vietphrase(self, event=None):
#save current paragraph
        current_par_num = int(self.par_selector.component('entryfield').getvalue())
        ofile = open('parnum','w'); ofile.write("%s\n" % current_par_num); ofile.close()
        non_volatile_vietphrase = '/home/long/Dropbox/courses/python/vietphrase/vietphrase'
        volatile_vietphrase = 'vietphrase'
        nvol_size = os.path.getsize(non_volatile_vietphrase)
        vol_size = os.path.getsize(volatile_vietphrase)
        nvol_mtime = os.path.getmtime(non_volatile_vietphrase)
        vol_mtime = os.path.getmtime(volatile_vietphrase)
        self.message = """Size of '%s': %s bytes
  Time of last modification: %s 
Size of '%s': %s bytes
  Time of last modification: %s
  Number of vietphrase entries: %s""" % (non_volatile_vietphrase, nvol_size, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(nvol_mtime)), volatile_vietphrase, vol_size, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(vol_mtime)), chinesetext.import_vietphrase_data())
        if (nvol_size < vol_size) and (nvol_mtime < vol_mtime):
            self.message = """%s
Need to backup: %s => %s""" % (self.message, volatile_vietphrase, non_volatile_vietphrase)
            shutil.copyfile(volatile_vietphrase, non_volatile_vietphrase)
            self.message = """%s
...Done!!!""" % self.message
        self.info_text.setvalue(self.message)

if __name__ == '__main__':
    root = Tk() # root (main) window
    root.title("Vietphrase")
# https://code.activestate.com/lists/python-list/698842/
    img = Image("photo", file='Python-icon.png')
    root.call('wm', 'iconphoto', root._w, img)
    Pmw.initialise(root)        
    app = Vietphrase(root)
        
    def quit(event=None):
        app.backup_vietphrase()
        print app.message
        try:
            shutil.copyfile('parnum', '/home/long/Dropbox/courses/python/vietphrase/parnum')
            shutil.copyfile('chinese.txt', '/home/long/Dropbox/courses/python/vietphrase/chinese.txt')
            print "'chinese.txt', 'parnum' backed up successfully!!!"
        except:
            print "Error backing up 'chinese.txt', 'parnum'!!!"
        root.destroy()

    root.bind('<Control-Q>', quit); root.bind('<Control-q>', quit)
       
    root.mainloop()

