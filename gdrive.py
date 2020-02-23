#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Google Drive
"""

class GDURL:
    def __init__(self,URL=""):
        self.URL = URL

    def getID(self):
#First, try to split by "id="
# for a "normal" Google Drive account
#        return "%s" % self.URL.split('id=')[-1]
        idlist = self.URL.split('id=')
        if len(idlist)!=1:
            return idlist[-1]
        else:
# for Google Drive account type "hus.edu.vn"
#"https://drive.google.com/file/d/0BxqhDSehma75QktLSExhRnZVVVE/view?usp=sharing"
            filedlist = self.URL.split('file/d/')
            return filedlist[-1].split('/')[0]

    def direct_link(self):
        return "https://drive.google.com/uc?export=download&id=%s" % self.getID()

    def wget(self):
        import os
        default_output_file = "wget_download.out"
        try:
            output_file = sys.argv[2]
        except:
            output_file = default_output_file
            print "output file : %s" % default_output_file  
        cmd = 'wget -O %s "%s"' % (output_file, self.direct_link())
        print cmd
        os.system(cmd)

    def __str__(self):
        return "%s" % (self.URL)        
        
if __name__ == '__main__':
    import sys
    usage = 'Usage : %s Google_Drive_URL' % sys.argv[0]
    try: 
        URL = sys.argv[1]
    except:
        print usage; sys.exit(1)
    newlink = GDURL(URL=URL)
    print newlink.getID()
    newlink.wget()

