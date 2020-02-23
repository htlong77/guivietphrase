#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sets import Set
cpchar="。"      #chinese-point-char
cxmark = "！"    #chinese-exclamation-mark
coqmark = "“"    #chinese-quotation-marks
ccqmark = "”"    #
caoqmark = "《"  #another chinese quotation mark
cacqmark = "》"  #another chinese quotation mark
cosquote = "‘"   #chinese-single-quote
ccsquote = "’"   #
ccomma = "，"    #chinese-comma
cacomma = "、"   #another chinese comma
ccolon = "："    #chinese-colon
cqmark = "？"    #chinese-question-mark
cellipsis = "……" #chinese-ellipsis
chinese_punc_list= [cpchar, cxmark, coqmark, ccqmark, caoqmark, cacqmark, cosquote, ccsquote,# ccomma, cacomma,
                               ccolon, cqmark, cellipsis, "——"]
class VnText:
    def __init__(self, content=""):
        self.content = content

    def to_proper_name(self):
        vntext = " "+self.content.decode('utf-8').strip()
        tmp = ""
        for i in range(1, len(vntext), 1):
            cur_char = vntext[i]
            if vntext[i-1] == " ":
                cur_char = vnupper(cur_char)
            tmp = tmp + cur_char 
        return "%s" % (tmp.strip().encode('utf-8'))

    def __str__(self):
        return self.content    

"""
Chinese Text
"""
#par_is_called = False;
vpdebug = False
vn_lowercase=u"aàáảãạăằắẳẵặâầấẩẫậbcdđeèéẻẽẹêềếểễệfghiìíỉĩịjklmnoòóỏõọôồốổỗộơờớởỡợpqrstuùúủũụưừứửữựvwxyỳýỷỹỵz"
vn_uppercase=u"AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬBCDĐEÈÉẺẼẸÊỀẾỂỄỆFGHIÌÍỈĨỊJKLMNOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢPQRSTUÙÚỦŨỤƯỪỨỬỮỰVWXYỲÝỶỸỴZ"

class ChineseChapter:    
    def __init__(self, content=""):
        self.content = content

    def to_paragraphs(self):
        self.secs = []
        self.paragraphs = split_to_paragraphs(self.content)
        for par in self.paragraphs:
            tmp = par_split(par)
            self.secs.extend(tmp)

    def reset_act_vpdata(self):
        self.act_vpdata = []

    def reset_act_pndata(self):
        self.act_pndata = []

    def reset_act_hvdata(self):
        self.act_hvdata = {}
        
    def update_act_hvdata(self):
        self.reset_act_hvdata()
        tmp = self.content
# We need to use encode/decode here (https://www.pythoncentral.io/python-unicode-encode-decode-strings-python-2x/)
        ii=0
        for cchar in tmp.decode('utf-8'):
            en_cchar = cchar.encode('utf-8')
            if hvdata.has_key(en_cchar):
               if not self.act_hvdata.has_key(en_cchar):
                   self.act_hvdata.update({en_cchar:hvdata[en_cchar]})
#        print "Number of actually used chinese characters: %s" % len(self.act_hvdata)

    def update_act_vpdata(self):
        self.reset_act_vpdata()
        tmp = self.content
        for (ccombi, vncombi) in vietphrasedata:
            if tmp.find(ccombi) != -1:
                self.act_vpdata.append((ccombi, vncombi))
#        print "Number of actually-kept-for-later-use vietphrase entries: %s" % len(self.act_vpdata)

    def update_act_pndata(self):
        self.reset_act_pndata()
        tmp = self.content
        for (ccombi, vncombi) in pnamedata:
            if tmp.find(ccombi) != -1:
                self.act_pndata.append((ccombi, vncombi))
#        print "Number of fixed proper name entries: %s" % len(self.act_pndata)
#        print "Temporary added entries for proper name:"
#        i = 0
        for (ccombi, vncombi) in pluspnamedata:
            if (ccombi, vncombi) not in self.act_pndata:
                if tmp.find(ccombi) != -1:
#                    i += 1;
                     self.act_pndata.append((ccombi, vncombi))
#                    print "  %s. %s:%s" % (i, ccombi, vncombi)
#        print "Number of proper name entries before 'minus': %s" % len(self.act_pndata)
        todelete = []
        for ccombi in minuspnamedata:
            if tmp.find(ccombi) != -1:
                 todelete.append(ccombi)
#        print "Temporary removed entries for proper name:"
        i = 0
#        ii = 0
        while i<len(self.act_pndata):
            ccombi, vncombi = self.act_pndata[i][0], self.act_pndata[i][1]
            if ccombi in todelete:
#                ii += 1
                del self.act_pndata[i]
#                print "  %s. %s:%s" % (ii, ccombi, vncombi)
            else:
                i += 1
#        print "Number of actually kept proper name entries for later use: %s" % len(self.act_pndata)

    def update_data(self):
        self.update_act_hvdata(); self.update_act_vpdata(); self.update_act_pndata()

    def use_hv_data(self, cntext):
#For chinese text
#    i = 0
        for chinese_char, hvphonetic in self.act_hvdata.items():
#put an extra space for each "han-viet phonetic"
#            if par_is_called and vpdebug:
            if vpdebug:
                cntext = cntext.replace(chinese_char, hvphonetic+"% ")
            else:
                cntext = cntext.replace(chinese_char, hvphonetic+" ")
#        i +=1; print i, chinese_char
        return cntext

    def cn_to_hanviet(self, cntext):
        tmp = self.use_hv_data(cntext)
        tmp = chinese_punc_refine(tmp)
        tmp = latin_punc_refine(tmp)
        return sentence_case(tmp).strip()

    def to_hanviet(self):
        return self.cn_to_hanviet(self.content)

    def to_hanvietfile(self):
        write_to_file('hanviet.txt', self.to_hanviet())

    def use_pn_data(self, cntext):
#For chinese text
#        i = 0
        for (ccombi, vncombi) in self.act_pndata:
#    for (ccombi, vncombi) in self.act_pndata:
            if cntext.find(ccombi) != -1:
#add an extra space for each "vietnamese combination"
#                if par_is_called:
                if vpdebug:
                    cntext = cntext.replace(ccombi, vncombi+"# ")
                else:
                    cntext = cntext.replace(ccombi, vncombi+" ")
#                i +=1; print "%s : '%s' = '%s' " % (i, ccombi, vncombi)    
        return cntext

    def use_vp_data(self, cntext):
#For chinese text
#        i = 0
        for (ccombi, vncombi) in self.act_vpdata:
            if cntext.find(ccombi) != -1:
                vncombi = vncombi.split('/')[0]
#add an extra space for each "vietnamese combination"
#                i += 1
#                if par_is_called:
                if vpdebug:
                    cntext = cntext.replace(ccombi, "%s{%s}| " % (vncombi, hanviet_combi(ccombi)))
                else:
                    cntext = cntext.replace(ccombi, vncombi+" ")
#    print "Number of vietphrase entries finally used: %s" % i
        return cntext

    def cn_to_vietphrase(self, cntext):
        tmp = self.use_pn_data(cntext)
        tmp = self.use_vp_data(tmp)
        tmp = self.use_hv_data(tmp)
        tmp = chinese_punc_refine(tmp)
        tmp = latin_punc_refine(tmp)
        if not vpdebug:
            tmp = vnencode(tmp) #protect some text 
        tmp = remove_dich_lieu_etc(tmp)
        tmp = sentence_case(tmp).strip()
        if not vpdebug:
            return vndecode(tmp) #restore protected text
        else:
            return tmp 
        
    def to_vietphrase(self):
        if os.environ.get('CDEBUG') == "yes":
            nopar = len(self.paragraphs)
            tmp = ""
            for i in range(nopar):
                tmp += "%s/%s: %s\n" % (i+1, nopar, self.cn_to_vietphrase(self.paragraphs[i]))
            return tmp[:-1]
        else:
            return self.cn_to_vietphrase(self.content)

    def to_tangthuvien(self, chapno, chapname):
        vptmp = self.cn_to_vietphrase(self.content)
        hvtmp = self.cn_to_hanviet(self.content)
        return """[FONT="Palatino Linotype"]
[CENTER]
[COLOR="royalblue"][SIZE="5"][B]Quyển 9: Hồng trần Kiếm Tiên[/B][/SIZE][/COLOR]

[FONT="Times New Roman"][SIZE="5"][COLOR="Navy"]Chương %s: %s[/COLOR][/SIZE][/FONT]

[SIZE="4"][COLOR="#ADD8E6"][B]Tác giả: Ngã Cật Tây Hồng Thị[/B][/COLOR][/SIZE]

[/CENTER]

[SPOILER="       VietPhrase       "]
%s
[/SPOILER]
[SPOILER="          Hán Việt        "]
%s
[/SPOILER]
[SPOILER="          Tiếng Trung        "]
%s
[/SPOILER]
Thảo luận: [URL="http://www.tangthuvien.vn/forum/showthread.php?t=146161"]tại đây![/URL]
[/FONT]
""" % (chapno, chapname, vptmp, hvtmp, self.content)
        
    
    def to_vpfile(self):
        write_to_file('vietphrase.txt', "%s" % self.to_vietphrase())

    def show_vietphrase(self, cntext):
        tmp = ""
        for (ccombi, vncombi) in self.act_vpdata:
            if ccombi==cntext:
                tmp = vncombi; break
        return tmp

    def show_all_vps(self, cntext):
        i = 0; tmp = ""
        for (ccombi, vncombi) in self.act_vpdata:
            if cntext.find(ccombi) != -1:
                i += 1; tmp += "%s. %s:%s\n" %(i, ccombi, vncombi)
#                if i==1:
#                    firstvncombi = vncombi
#        if i==1:
#           return firstvncombi
#        else:    
#           return tmp[:-1]
        return tmp[:-1]
 
    def show_all_pns(self, cntext):
        i = 0; tmp = ""
        for (ccombi, vncombi) in self.act_pndata:
            if cntext.find(ccombi) != -1:
                i += 1; tmp += "%s. %s:%s\n" %(i, ccombi, vncombi)
        return tmp[:-1]
 
    def show_all_ccombis(self, cntext):
#        return """Hanviet:
#%s
#Vietphrases:
#%s
#Proper names:
#%s""" % (hanviet_combi(cntext), self.show_all_vps(cntext), self.show_all_pns(cntext))
        return """Hán-Việt:
%s
Vietphrases:
%s""" % (hanviet_combi(cntext), self.show_all_vps(cntext))
    
    def find_cc(self, hvphonetic):
        global pnametoadd
        pnametoadd = []
        ccs = {}
        #determine the length of chinese combination
        cclen = len (hvphonetic.split(" "))
        tmpcc = ''
        tmp = self.content.decode("utf-8")
        for i in range(len(tmp)+cclen-1):
            ccombi = tmp[i:i+cclen].encode("utf-8")
            if hvphonetic == hanviet_combi(ccombi):
                if ccs.has_key(ccombi):
                    ccs[ccombi] += 1
                else:
                    ccs[ccombi] = 1
        for ccombi in ccs:
            tmpcc += "'%s' ===> Number of appearances: %s\n" % (ccombi, ccs[ccombi])       
        tmpcc = tmpcc.strip()
        if tmpcc=='':
            tmpcc = "'%s'... not found!!!" % (hvphonetic)
        if len (ccs)==1:
            cntext = ccs.keys()[0]
            for (ccombi, vncombi) in self.act_vpdata:
                if cntext == ccombi:
                    break
            pnametoadd.append([cntext, hvphonetic, vncombi])
            tmpcc += """\nVietphrases:
%s
Proper names:
%s""" % (self.show_all_vps(cntext), self.show_all_pns(cntext))
        return tmpcc

    def find_ccvp(self, vietphrase):
        ccs = {}
        tmp = ''
        for sec in self.secs:
            if self.cn_to_vietphrase(sec) == vietphrase:
                if ccs.has_key(sec):
                    ccs[sec] += 1
                else:
                    ccs[sec] = 1
        for sec in ccs:
            tmp += "'%s'\n'%s' ===> Number of appearances: %s\n" % (sec, hanviet_combi(sec),  ccs[sec])       
        tmp = tmp.strip()
        if tmp=='':
            tmp = "'%s'... not found!!!" % (vietphrase)
        return tmp

    def paragraph(self, i):
        global vpdebug
        if (i>=0) and (i<=len(self.paragraphs)+1):
            if i == 0:
                i = len(self.paragraphs)
            if i == len(self.paragraphs) + 1:
                i = 1
            tmpp = """===> hanviet\n%s""" % self.cn_to_hanviet(self.paragraphs[i-1])
            vpdebug = True
            tmp = """Paragraph %s/%s: 
===> chinese\n%s
%s
===> vietphrase {hanviet}\n%s""" % (i, len(self.paragraphs), self.paragraphs[i-1], tmpp, self.cn_to_vietphrase(self.paragraphs[i-1]))
            vpdebug = False
            tmp = "%s\n===>vietphrase\n%s" % (tmp, self.cn_to_vietphrase(self.paragraphs[i-1]))
# Doesn't work, see : https://askubuntu.com/questions/389683/how-we-can-change-linux-environment-variable-in-python
# for detail
#            cmd = 'export PARNUM=%s' % (i+1)
#            print cmd
#            failure = os.system(cmd)
#            if failure:
#                print 'export environment variable PARNUM failed'; sys.exit(1)
            ofile = open('parnum','w'); ofile.write("%s\n" % i); ofile.close()
            return tmp
        else:
            return "Enter a number between 1 and %s" % len(self.paragraphs)

    def new_vietphrase_entries(self, minlen):
        repeated_combis = find_repeated_combinations(self.content)
        vietphrase_combis = Set()
        for (ccombi, vncombi) in self.act_vpdata:
            vietphrase_combis.add(ccombi)
        new_combis = repeated_combis.difference(vietphrase_combis)
        i = 0
        for element in new_combis:
            elen = len(element.decode('utf-8'))
            if elen >= minlen:
                i += 1
                print "%s: [%s] |%s|%s|: %s" % (i, elen, element, hanviet_combi(element), self.content.count(element))
        return """Number of repeated combinations (without a punctuation): %s
Number of kept vietphrase entries: %s
Number of combinations that is not vietphrase and have at least %s characters: %s""" % (len(repeated_combis), len(vietphrase_combis), minlen, i)

    def __str__(self):
        return self.content    
        
def find_repeated_combinations(text):
    repeated_combis = Set()
    tmp = text.decode("utf-8")
    pos = 0
    i = 0
    lentmp = len(tmp)
    for pos in range(lentmp-1):
        sublen = 2
        sub = tmp[pos:pos+sublen]
        while tmp.count(sub) > 1:
            subencode = sub.encode('utf-8')
# we do not want combination having a punctuation character
            containpuncchar = False
            for puncchar in chinese_punc_list + [ccomma, cacomma, "\n", "…", "*", "~", " "]:
                if puncchar in subencode:
                    containpuncchar = True
                    break
            if containpuncchar:
                break
            else:
                i += 1
                repeated_combis.add(subencode)
#                print "%s, %s, |%s|(%s), %s" %(pos, i, subencode, tmp.count(sub), hanviet_combi(sub.encode('utf-8')))
            sublen += 1
            if pos+sublen<= lentmp:
                sub = tmp[pos:pos+sublen]
            else:
                break
    return repeated_combis
    
def import_hv_data():
    global hvdata
    hvdata = {}
    hvfile = open("hanvietphonetic","r"); lines=hvfile.readlines(); hvfile.close()
    data = [line.strip().split("=") for line in lines]
    hvdat = {chinese_char: hvphonetic for [chinese_char, hvphonetic] in data}
    hvdata.update(hvdat)
#    print "Number of hanviet entries: %s" % len(hvdata)

def import_vietphrase_data():
    global vietphrasedata
    vietphrasedata = []
    vietphrasefile = open("vietphrase","r"); lines=vietphrasefile.readlines(); vietphrasefile.close()
    data = [line.strip().split("=") for line in lines]
    vietphrasedata.extend(data) 
#    print "Number of vietphrase entries: %s" %  len(vietphrasedata)
    return len(vietphrasedata)

def import_propername_data():
    global pnamedata
    pnamedata = []
    pnamefile = open("propername","r"); lines=pnamefile.readlines(); pnamefile.close()
    data = [line.strip().split("=") for line in lines]
    pnamedata.extend(data) 
#    print "Number of proper name entries: %s" %  len(pnamedata)

def import_pluspropername_data():
    global pluspnamedata
    pluspnamedata = []
    pluspnamefile = open("pluspropername","r"); lines=pluspnamefile.readlines(); pluspnamefile.close()
    data = [line.strip().split("=") for line in lines]
    pluspnamedata.extend(data) 
#    print "Number of plus proper name entries: %s" %  len(pluspnamedata)

def import_minuspropername_data():
    global minuspnamedata
    minuspnamedata = []
    minuspnamefile = open("minuspropername","r"); lines=minuspnamefile.readlines(); minuspnamefile.close()
    data = [line.strip() for line in lines]
    minuspnamedata.extend(data) 
#    print "Number of minus proper name entries: %s" %  len(minuspnamedata)

def import_ce_data():
    global cedata
    cedata = []
    cefile = open("cedict.dic","r"); lines=cefile.readlines(); cefile.close()
    i = 0; ii = 0
    for line in lines:
        if line[0]!="#":
            entry = line.split(' ')
            trad = entry[0].strip(); simp = entry[1].strip()
            man_def = ' '.join(entry[2:]).strip()
            pos = man_def.find(']')
            mandarin = man_def[0:pos].strip()+"]"
            definition = man_def[pos+1:].strip()
            i +=1
            if trad!=simp:
                ii +=1
            #print "%s %s %s %s %s" % (ii, trad, simp, mandarin, definition)
            cedata.append([trad, simp, mandarin, definition])
#    print "Number of 'Chinese to English' entries: %s" %  len(cedata)
    return len(cedata)

def import_lacviet_data():
    global lacvietdata
    lacvietdata = []
    lacvietfile = open("lacviet.dic","r"); lines=lacvietfile.readlines(); lacvietfile.close()
    data = [line.strip().split("=") for line in lines]
    lacvietdata.extend(data) 
#    print "Number of lacviet entries: %s" %  len(lacvietdata)
    return len(lacvietdata)

def import_thieuchuu_data():
    global thieuchuudata
    thieuchuudata = []
    thieuchuufile = open("thieuchuu.dic","r"); lines=thieuchuufile.readlines(); thieuchuufile.close()
    data = [line.strip().split("=") for line in lines]
    thieuchuudata.extend(data) 
#    print "Number of thieuchuu entries: %s" %  len(thieuchuudata)
    return len(thieuchuudata)

def import_dics():
    import_ce_data()
    import_lacviet_data()
    import_thieuchuu_data()

def import_data():
    import_hv_data()
    import_vietphrase_data()
    import_propername_data(); import_pluspropername_data(); import_minuspropername_data()

def chinese_punc_refine(cntext):
    cpchar="。"; npchar=". " # change chinese-point-char "。" to normal-point-char (and add an extra space after the point)
    cxmark = "！"; nxmark ="! " # change chinese-exclamation-mark to normal-exclamation-mark (and add an extra space after that mark)
    coqmark = "“"; noqmark = "«" # change chinese-quotation-marks to normal-quotation-mark (opening/closing quotation mark)
    ccqmark = "”"; ncqmark = "» " # (and add an extra space after the closing double quote)
    caoqmark = "《"; cacqmark = "》" #another chinese quotation mark
    cosquote = "‘"; nosquote = "`" # change chinese-single-quote to normal-single-quote (opening/closing quote)
    ccsquote = "’"; ncsquote = "' " # (and add an extra space after the closing single quote)
    ccomma = "，"; ncomma = ", " # change chinese-comma to normal-comma (and add an extra space after the comma)
    cacomma = "、" #another chinese comma
    ccolon = "："; ncolon = ": " # change chinese-colon to normal-colon (and add an extra space after the colon)
    cqmark = "？"; nqmark = "? " # change chinese-question-mark to normal-question-mark (and add an extra space after that mark)
    cellipsis = "……"; nellipsis = "... " # change chinese-ellipsis to normal-ellipsis (and add an extra space after the ellipsis)

    chinese_punc_refine_list= [(cpchar, npchar), (cxmark, nxmark), (coqmark, noqmark), (ccqmark, ncqmark), (caoqmark, noqmark), (cacqmark, ncqmark), (cosquote, nosquote), (ccsquote, ncsquote), (ccomma, ncomma), (cacomma, ncomma), (ccolon, ncolon), (cqmark, nqmark), (cellipsis, nellipsis), ("——", "-")]
#For chinese text
    for to_change, change_to in chinese_punc_refine_list:
         cntext = cntext.replace(to_change, change_to)
    return cntext

def insert_ccombi_data(ccombi, vncombi, tolist):
#For insert entry "ccombi=vncombi" into the correct place in tolist
    
    print 'Inserting "%s=%s": %s entries ' % (ccombi, vncombi, len(tolist))
    ccombilen = len(ccombi.decode("utf-8"))
    print "Find the correct position to insert..."
    i = 0; inserted=False 
    while (not inserted) and (i<len(tolist)):
        datalen = len(tolist[i][0].decode("utf-8"))
        if datalen < ccombilen:
            tolist.insert(i,[ccombi, vncombi])
            inserted = True; print "success"
            break 
        elif datalen == ccombilen:
#            print "%s %s %s" % (i,tolist[i][0], ccombi.decode("utf-8") < tolist[i][0].decode("utf-8"))                  
            if ccombi.decode("utf-8") < tolist[i][0].decode("utf-8"):
                 tolist.insert(i,[ccombi, vncombi])
                 inserted = True; print "success"
            elif ccombi.decode("utf-8") == tolist[i][0].decode("utf-8"):
                 print "Fail!!! Entry exited."; break
        
        i += 1
    if (i==len(tolist)) and (not inserted):
        tolist.append([ccombi, vncombi])
        inserted = True; print "success"
    return ''.join(tolist[j][0]+"="+tolist[j][1]+"\n" for j in range(len(tolist)))[0:-1]
 
def insert_vp_data(ccombi, vncombi):
    hvcombi = hanviet_combi(ccombi)
    if vncombi.find(hvcombi) == -1:
        vncombi += "/%s" % hvcombi
    return insert_ccombi_data(ccombi, vncombi, vietphrasedata)

def update_vp_data(ccombi, vncombi):
    found = False
    i = 0
    hvcombi = hanviet_combi(ccombi)
    if vncombi.find(hvcombi) == -1:
        vncombi += "/%s" % hvcombi
    print "Updating %s=%s:..." % (ccombi, vncombi)
    for (tmpccombi, tmpvncombi) in vietphrasedata:
        if tmpccombi == ccombi:
            found = True; vietphrasedata[i]=[tmpccombi, vncombi]; print "Entry number %s ===> success" % (i+1)
            break
        i +=1
#    print vietphrasedata[i][1]
    return ''.join(vietphrasedata[j][0]+"="+vietphrasedata[j][1]+"\n" for j in range(len(vietphrasedata)))[0:-1]

def check_vp_data(ccombi):
    found = False
    i = 0
    print "Hanviet: '%s'" % (hanviet_combi(ccombi))
    for (tmpccombi, vncombi) in vietphrasedata:
        if tmpccombi == ccombi:
            found = True
            return """'%s'... found!!! Entry number %s. 
%s""" % (ccombi, i+1, vncombi)
        i += 1
    if not found:
        return "Entry '%s'... not found!!!" % ccombi

def insert_pn_data(ccombi, vncombi):
    return insert_ccombi_data(ccombi, vncombi, pnamedata)

def add_plus_proper_name_entry(ccombi, vncombi):
    ofile = open("pluspropername","r"); tmp = ofile.read().strip(); ofile.close()
    write_to_file('pluspropername', "%s\n%s" %(tmp, plus_proper_name(ccombi, vncombi)))

def add_minus_proper_name_entry(ccombi):
    ofile = open("minuspropername","r"); tmp=ofile.read().strip(); ofile.close()
    write_to_file('minuspropername', "%s\n%s" %(tmp, ccombi))

def add_proper_name_entry(ccombi, vncombi):
    write_to_file('propername', insert_pn_data(ccombi, vncombi))

def add_vietphrase_entry(ccombi, vncombi):
    write_to_file('vietphrase', insert_vp_data(ccombi, vncombi))

def update_vietphrase_entry(ccombi, vncombi):
    write_to_file('vietphrase', update_vp_data(ccombi, vncombi))

def add_proper_name_entry_having_hanviet(pnargv):
    write_to_file('propername', add_proper_name_having_hanviet(pnargv))

def update_vietphrase_entry_having_hanviet(vpargv):
    ccombi = pnametoadd[0][0]
    if vpargv is None:
        vncombi = pnametoadd[0][2]
    else:
        vncombi = vpargv
    write_to_file('vietphrase', update_vp_data(ccombi, vncombi))

def add_vietphrase_entry_having_hanviet(vpargv):
    ccombi = pnametoadd[0][0]
    if vpargv is None:
        vncombi = pnametoadd[0][1]
    else:
        vncombi = vpargv
    write_to_file('vietphrase', insert_vp_data(ccombi, vncombi))

def add_proper_name_having_hanviet(pnargv):
    ccombi = pnametoadd[0][0]
    if pnargv is None:
        vncombi = VnText(pnametoadd[0][1]).to_proper_name()
    else:
        vncombi = pnargv
    return insert_pn_data(ccombi, vncombi)

def plus_proper_name(ccombi, vncombi):
    return "%s=%s" % (ccombi, vncombi)

def check_lv_data(ccombi):
    import_lacviet_data()
    found = False
    i = 0
    for (tmpccombi, vncombi) in lacvietdata:
        if tmpccombi == ccombi:
            found = True
            return """Từ điển Lạc Việt: '%s'... found!!! Entry number %s. 
%s""" % (ccombi, i+1, vncombi.replace("\\n","\n").replace("\\t","\t"))
        i += 1
    if not found:
        return "Từ điển Lạc Việt: Entry '%s'... not found!!!" % ccombi

def check_tc_data(ccombi):
    import_thieuchuu_data()
    found = False
    i = 0
    for (tmpccombi, vncombi) in thieuchuudata:
        if tmpccombi == ccombi:
            found = True
            return """Từ điển Thiều Chửu: '%s'... found!!! Entry number %s. 
%s""" % (ccombi, i+1, vncombi.replace("\\n","\n").replace("\\t","\t"))
        i += 1
    if not found:
        return "Từ điển Thiều Chửu: Entry '%s'... not found!!!" % ccombi

def check_ce_data(ccombi):
    import_ce_data() #https://cc-cedict.org/wiki/
    found = False  
    i = 0
    for (trad, simp, mandarin, definition) in cedata:
        i += 1
        if (trad == ccombi) or (simp == ccombi):
            found = True
            return """Chinese to English Dictionary: '%s'...found!!! Entry number %s:
Traditional: %s
Simplified:  %s
Mandarin:    %s
Definition:
%s"""% (ccombi, i, trad, simp, mandarin, definition.replace("/","\n")[1:-1]) 
    if not found:
        return "Chinese to English Dictionary: Entry '%s'... not found!!!" % ccombi

def check_dics(ccombi):
    return "\n-------------------------\n".join([check_tc_data(ccombi), check_lv_data(ccombi), check_ce_data(ccombi)])
    
def check_homonym_data(cchar):
    import_ce_data()
#    found = False  
    i = 0
    for (trad, simp, mandarin, definition) in cedata:
        i += 1
        if (trad == cchar) or (simp == cchar):
            break
    print "Entry %s : %s : %s %s %s %s" % (i, cchar, trad, simp, mandarin, definition)
    pronunciation = mandarin 
    i = 0; tmp = ''
    for (trad, simp, mandarin, definition) in cedata:
        i += 1
        if (mandarin == pronunciation):
            tmp += """==>Entry number %s:
  Traditional: %s
  Simplified:  %s
  Mandarin:    %s
  Definition:
%s

"""% (i, trad, simp, mandarin, definition.replace("/","\n")[1:-1])
    return tmp.strip()

def hanviet_combi(ccombi):
    hvcombi = ""
    for cchar in ccombi.decode("utf-8"):
        key = cchar.encode("utf-8")
        if hvdata.has_key(key):
            hvcombi += hvdata[key]+" "
        else:
            hvcombi += key
    return hvcombi.strip()

def vnencode(vntext):
    encodetexts = [['«ông','«ô***ô***n***g'], ['tội nghiệt chi khí','tội nghiệt *** khí'], ['mục đích','mục ĐÍCH'], ['đích thật','ĐÍCH thật'], ['chi tiêu','CHI tiêu'], ['chi tiết','CHI tiết'], ['chi nhất mạch','CHI nhất mạch'], ['chi thuật', 'CHI thuật'], ['huống chi', 'huống CHI'], ['đích truyền', 'ĐÍCH truyền'], ['sở trường', 'SỞ trường'], ['sở liệu', 'SỞ liệu'], ['đích thực', 'Đích thực'], ['suy bại chi khí', 'suy bại Chi khí'], ['xoay sở', 'xoay SỞ'], ['trứng', 'TRỨNG'], ['dương liễu', ' dƯƠNG LIỄU'], ['tới được đích', 'tới được ĐÍCH'], ['sở nguyện', 'SỞ nguyện'], ['sở học', 'SỞ học'], ['sở dĩ', 'SỞ dĩ'], ['tùy tâm sở dục', 'tùy tâm SỞ dục'], ['cơ sở', 'cơ SỞ'], ['nói chi', 'NÓI CHI'], ['đích thân', 'ĐÍCH THÂN'], ['sở hữu', 'SỞ HỮU'], ['chi li', 'CHI LI'], ['đích xác', 'ĐÍCH XÁC'], ['khổ sở', 'KHỔ SỞ'], ['cây liễu', 'CÂY LIỄU'], ['chi viện', 'CHI VIỆN'], ['sở đoản', 'SỞ ĐOẢN']
    ]
    for [toencode, encodeto] in encodetexts:
        vntext = vntext.replace(toencode, encodeto)
    return vntext 

def vndecode(vntext):
    decodetexts = [['Ô***ô***n***g','Ô...ô...n...g'], ['nghiệt *** khí','nghiệt chi khí'], ['mục ĐÍCH', 'mục đích'], ['Mục ĐÍCH', 'Mục đích'], ['ĐÍCH thật', 'đích thật'], ['CHI tiêu', 'chi tiêu'], ['CHI tiết', 'chi tiết'], ['CHI nhất mạch', 'chi nhất mạch'], ['CHI thuật', 'chi thuật'], ['uống CHI', 'uống chi'], ['ĐÍCH truyền', 'đích truyền'], ['SỞ trường', 'sở trường'], ['SỞ liệu', 'sở liệu'], ['Đích thực', 'đích thực'], ['suy bại Chi khí', 'suy bại chi khí'], ['xoay SỞ', 'xoay sở'], ['chuyển thế CHI thân', 'chuyển thế chi thân'], ['TRỨNG', 'trứng'], ['ƯƠNG LIỄU', 'ương liễu'], ['tới được ĐÍCH', 'tới được đích'], ['SỞ nguyện', 'sở nguyện'], ['SỞ học', 'sở học'], ['SỞ dĩ', 'sở dĩ'], ['tùy tâm SỞ dục', 'tùy tâm sở dục'], ['cơ SỞ', 'cơ sở'], ['NÓI CHI', 'nói chi'], ['ĐÍCH THÂN', 'đích thân'], ['SỞ HỮU', 'sở hữu'], ['CHI LI', 'chi li'], ['ĐÍCH XÁC', 'đích xác'], ['KHỔ SỞ', 'khổ sở'], ['CÂY LIỄU', 'cây liễu'], ['CHI VIỆN', 'chi viện'], ['SỞ ĐOẢN', 'sở đoản']
   ] 
    for [todecode, decodeto] in decodetexts:
        vntext = vntext.replace(todecode, decodeto)
    return vntext 

def remove_dich_lieu_etc(vntext):
    if vpdebug:
        return vntext
    else:
        return vntext.replace(" đích", "").replace(" liễu", "").replace(" trứ", "").replace(" sở", "").replace(" chi ", " ")
#        return vntext.replace(" đích", "").replace(" liễu", "").replace(" trứ", "").replace(" sở", "")
#        return vntext.replace(" đích", "").replace(" liễu", "").replace(" trứ", "")
#        return vntext.replace(" đích", "").replace(" liễu", "")
    
def latin_punc_refine(vntext):
#remove space (if any) before : ".", ",", "!", "?", ":", "'", "»"
#remove space (if any) at the end of a line
#change " -" to " - "
    latin_punc_refine_list = [(" .", "."), (" ,", ","), (" :", ":"), (" !", "!"), (" ?", "?"), (" '", "'"), (" »", "»"), (" \n","\n"), (" -"," - ")
]
#For han-viet/vietphrase text
    for to_change, change_to in latin_punc_refine_list:
         vntext = vntext.replace(to_change, change_to)
    return vntext

def sentence_case(vntext):
#For han-viet/vietphrase text
#Uppercase for the first charactef of a sentence
#    punc_list = [u"«", "\n", u"?", u"»", u".", "!"]
    punc_list = [u"«", "\n", u"?", u".", "!"]
    ext_punc_list = punc_list + [u" ", u"»", u"`"]
    vntext = vntext.decode('utf-8')
    tmp = ""
    toupper = True
    for i in range(len(vntext)):
        cur_char = vntext[i]
#        print i, cur_char, toupper
        if toupper:
            if cur_char not in ext_punc_list:
                tmp = tmp + vnupper(cur_char)
                toupper = False
#                print tmp, toupper
            else: 
                tmp = tmp + cur_char
#                print "here ", tmp, toupper
        else:
            tmp = tmp + cur_char
            if cur_char in punc_list:
                toupper = True
#            print tmp, toupper
    return tmp.encode('utf-8')

def vnupper(vnchar):
    posinlower = vn_lowercase.find(vnchar)
    if posinlower < 0:
        return vnchar
    else:
        return vn_uppercase[posinlower]    

def remove_irrelevant_infos(cntext):
    ifile = open('irrelevant','r'); lines=ifile.readlines(); ifile.close()
    for line in lines:
        line = line.strip()
        cntext = cntext.replace(line, '')
    return cntext

def strip_lines_and_remove_blank_lines(cntext):
    lines=cntext.splitlines()
#
# remove blank lines and spaces at the ends of each line
#
    cur_line = 0
    while cur_line<len(lines):
       if len(lines[cur_line].strip()) == 0:
           del lines[cur_line]
       else:
           lines[cur_line]=lines[cur_line].strip()
           cur_line += 1
    return  '\n'.join(lines)

def split_to_paragraphs(text):
    plist = text.split("\n")
    i = 0
    while i < len(plist):
        plist[i] = plist[i].strip()
        if len(plist[i]) == 0:
            del plist[i]
        else:
            i += 1
    return plist

def par_split(text):
#
    for mark in chinese_punc_list:
        text = text.replace(mark, "|")
    seclist = text.split("|")
    i = 0;
    while i<len(seclist):
        seclist[i] = seclist[i].strip()
        if seclist[i] == "":
            del seclist[i]
        else:
            i += 1
    return seclist

def write_to_file(filename="output.txt", content=""):
    ofile=open(filename,"w")
    ofile.write(content)
    ofile.close()

def readparnum():
    ifile = open('parnum','r'); parnum = int(ifile.readline()); ifile.close()
    return parnum

def dics_infos():
    return """Number of Chinese-English dictionary entries : %s
Number of Lac Viet dictionary entries : %s
Number of Thieu Chuu dictionary entries : %s
Number of vietphrase entries : %s""" % (import_ce_data(), import_lacviet_data(), import_thieuchuu_data(), import_vietphrase_data()) 

def refine_chinese_text(content):
    chap = ChineseChapter(content=content)
    chap.content = remove_irrelevant_infos(chap.content)
    chap.content = strip_lines_and_remove_blank_lines(chap.content)
    chap.to_paragraphs()
    chap.update_data()
    return chap
    
if __name__ == '__main__':
    import sys, os
    import_data()
    chinesefile = open("chinese.txt","r")
    newchap = refine_chinese_text(chinesefile.read())

    if len(sys.argv) == 1:
        parnum = 1
        print newchap.paragraph(parnum)
    else:
        if sys.argv[1]=="--thv":
            newchap.to_hanvietfile()
        elif sys.argv[1]=="--tvp":
            newchap.to_vpfile()
        elif sys.argv[1]=="--ttv":
            print newchap.to_tangthuvien(sys.argv[2], sys.argv[3])
        elif sys.argv[1]=="--apncc":
            add_proper_name_entry(sys.argv[2], sys.argv[3])
        elif sys.argv[1]=="--ppn":
            add_plus_proper_name_entry(sys.argv[2], sys.argv[3])
        elif sys.argv[1]=="--mpn":
            add_minus_proper_name_entry(sys.argv[2])
        elif sys.argv[1]=="--avpcc":
            try:
                add_vietphrase_entry(sys.argv[2], sys.argv[3])
            except:
                print 'Error: "vietphrase combination" needed'; sys.exit(1)
            newchap.update_act_vpdata(); print newchap.paragraph(readparnum())
        elif sys.argv[1]=="--uvpcc":
            update_vietphrase_entry(sys.argv[2], sys.argv[3])
            newchap.update_act_vpdata(); print newchap.paragraph(readparnum())
        elif (sys.argv[1]=="--uvphv") or (sys.argv[1]=="--uvp"):
            print newchap.find_cc(sys.argv[2])
            if len(pnametoadd) == 1:
                try:
                    vpargv = sys.argv[3]
                except:
                    vpargv = None
                update_vietphrase_entry_having_hanviet(vpargv)
                newchap.update_act_vpdata(); print newchap.paragraph(readparnum())
        elif sys.argv[1]=="--vp":
            print check_vp_data(sys.argv[2])
        elif sys.argv[1]=="--vps":
            print newchap.show_all_vps(sys.argv[2])
        elif sys.argv[1]=="--pns":
            print newchap.show_all_pns(sys.argv[2])
        elif sys.argv[1]=="--ccs":
            try:
                print newchap.show_all_ccombis(sys.argv[2])
            except:
                print "Error!!!"
        elif sys.argv[1]=="--lv":
            print check_lv_data(sys.argv[2])
        elif sys.argv[1]=="--tc":
            print check_tc_data(sys.argv[2])
        elif sys.argv[1]=="--ce":
            print check_ce_data(sys.argv[2])
        elif sys.argv[1]=="--nvpe":
            try:
                minlen = int(sys.argv[2])
            except:
                minlen = 2
            print newchap.new_vietphrase_entries(minlen)
        elif sys.argv[1]=="--dic":
            try: 
                print check_dics(sys.argv[2])
            except:
                print "Error: --dic chinese-expression"; sys.exit(1)
        elif sys.argv[1]=="--dichv":
            try:
                print newchap.find_cc(sys.argv[2])
            except:
                print "Error: 'hanviet' needed'"; sys.exit(1)
            if len(pnametoadd) == 1:
                print check_dics(pnametoadd[0][0])
        elif sys.argv[1]=="--par":
            try:
                parnum = int(sys.argv[2])
            except:
                parnum = readparnum() + 1
            print newchap.paragraph(parnum)
        elif sys.argv[1]=="--parc":
            parnum = readparnum()
            print newchap.paragraph(parnum)
        elif sys.argv[1]=="--parp":
            parnum = readparnum()-1
            print newchap.paragraph(parnum)
        elif sys.argv[1]=="--homonym":
            print check_homonym_data(sys.argv[2])
        elif sys.argv[1]=="--info":
            print dics_infos()
        elif sys.argv[1]=="--cc": #find in the text the chinese combination that has a given hanviet phonetic
            try:
                print newchap.find_cc(sys.argv[2])
            except:
                print 'Error: --cc: hanviet combination'; sys.exit(1)
        elif sys.argv[1]=="--ccvp": #find in the text the chinese combination that has a given vietphrase
            print newchap.find_ccvp(sys.argv[2])
        elif (sys.argv[1]=="--apnhv") or (sys.argv[1]=="--apn"): #add relevant proper name entry corresponding to a given hanviet phonetic
            print newchap.find_cc(sys.argv[2])            
            if len(pnametoadd) == 1:
                try:
                    pnargv = sys.argv[3]
                except:
                    pnargv = None
                add_proper_name_entry_having_hanviet(pnargv)
                newchap.update_act_pndata(); print newchap.paragraph(readparnum())
        elif (sys.argv[1]=="--avphv") or (sys.argv[1]=="--avp"): #add relevant proper name entry corresponding to a given hanviet phonetic
            try:
                print newchap.find_cc(sys.argv[2])
            except:
                print 'Error: "hanviet combination" needed'; sys.exit(1)
            if len(pnametoadd) == 1:
                try:
                    vpargv = sys.argv[3]
                except:
                    vpargv = None
                add_vietphrase_entry_having_hanviet(vpargv)
                newchap.update_act_vpdata(); print newchap.paragraph(readparnum())
        elif sys.argv[1]=="--hv": #return the chinese combination's hanviet phonetic
            print hanviet_combi(sys.argv[2])
        else:
            print "Unrecognized option!!!"
