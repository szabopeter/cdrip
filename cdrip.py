#!/usr/bin/python

import os
import re
import sys

fnpat = '"%02i cdrip.mp3"'
pretoc = 'pretoc'
intoc  = 'toc'
endtoc = 'endtoc'

#print sys.argv
try:
    dev = sys.argv[1]
except IndexError:
    dev = '/dev/cdrom'

(fin,fout,ferr) = os.popen3('cdda2wav dev=%s -v toc -J -H'%dev)
fin.close()
fout.close()
ls = ferr.readlines()
ferr.close()

sCDINDEX = 'CDINDEX discid: '
sCDDB = 'CDDB discid: '
reCDINDEX = re.compile(sCDINDEX)
reCDDB = re.compile(sCDDB)
for i in ls:
    if re.match(reCDDB,i):
        idCDDB = i.strip()[len(sCDDB):]
    elif re.match(reCDINDEX,i):
        idCDINDEX = i.strip()[len(sCDINDEX):]

print "CDINDEX: %s\nCDDB: %s\n"%(idCDINDEX,idCDDB,)

(fin,fout,ferr) = os.popen3('cdparanoia -d %s -Q'%dev)
fin.close()
fout.close()

tocst = pretoc
reToc1 = re.compile('^Table of')
reTocLine = re.compile('^ *[0-9]+\..* 2\n')
reTocLineNr = re.compile('^ *[0-9]+')
reToc9 = re.compile('^TOTAL')
for i in ferr:
    if tocst == pretoc:
        if re.match(reToc1,i):
            trknrs = []
            tocst = intoc
    elif tocst == intoc:
        if re.match(reToc9,i):
            tocst = endtoc
        elif re.match(reTocLine,i):
            trkno = int(re.findall(reTocLineNr,i)[0])
            trknrs.append(trkno)
    else:
        continue
ferr.close()

class pfopen:
    def __init__(self, filename, mode='w', joinchar=""):
        assert mode=='w', 'Only mode=w is allowed.\n'
        self.filename = filename
        self.data = [ ]
        self.mode = mode
        self.joinchar = joinchar
    def write(self, s):
        if type(s) == type([]):
            for i in s:
                self.write(i)
            return
        if type(s) != type(""): s = str(s)
#        ls = s.split('\n')
#        self.data[-1] += ls[0]
#        if ls[1:]==[]:
#            self.data[-1] += "\n"
#            self.data.append('')
#        else:
#            self.data.extend([x+'\n' for x in ls[1:]])
        #self.straighten()
        #s = "%i %s"%(len(self),s,)
        self.data.append(s)
    def straighten(self):
        #self.data = [ x+'\n' for x in ("".join(self.data)).split('\n') ]
        self.data = ( "".join(self.data) ).splitlines( True )
    def pad(self, n, line="\n"):
        self.straighten()
        self.data.extend( [ line ]*n )
    def __len__(self):
        self.straighten()
        return len(self.data)
    def size(self):
        for i in self.data:
            rv += len(i) + len(self.joinchar)
        return rv
    def content(self):
        return self.joinchar.join(self.data)
    def close(self):
        f = open(self.filename, self.mode)
        f.write(self.content());
        f.close()

#infofile = open('cdripinfo.txt','w')
infofile = pfopen('cdripinfo.txt','w')
#infofile.write("""mp3 = {}
#title = {}
#perf = {}
#genre = {}

infofile.write("""
#Comment to add when no filespecific comment available
#defcomment = { 'RIPPER' : 'cdrip.py', }
#Comments added to all files:
comments = { 'RIPPER' : 'cdrip.py',
#            'EANCODE' : '             ',
#            'ORDER'   : '      -   / ',
#            'COPYRIGHT' : 'TIM The International Music Company AG',
#            'SET'    : 'The Cradle Of Jazz',
#            'ARTIST' : "                         ",
            }

a   = ""        # Artist
T   = ""        # Album title
y   = 0         # Year
g   = ""        # Genre
""")
infofile.write("idCDDB = '%s'\n"%idCDDB)
infofile.write("idCDINDEX = '%s'\n"%idCDINDEX)
infofile.write("ttl = %i\n\n"%len(trknrs))

for i in trknrs:
    infofile.write('perf[%2i]  = a\n'%i)
    infofile.write('title[%2i] = ""\n'%i)
    
infofile.write('\n')
infofile.pad(20 - len(infofile)%20 -1 )
infofile.write('alltitles = """\n"""\n\n')
#infofile.pad(len(trknrs))
infofile.pad(20 - (len(infofile)+len(trknrs))%20 -1 )
infofile.write('allperfs = """\n"""\n\n')

infofile.write('\n\n')
for i in trknrs:
    infofile.write("mp3[%2i]   = %s\n"%(i,fnpat%i,))

infofile.close()
#print trknrs

for i in trknrs:
    ofn = fnpat%i
    print "Track %i => %s"%(i,ofn,)
    #cdin, cdout, cderr = os.popen3('cdparanoia -d %s -R %i-%i:[01] -'%(dev,i,i,))
    cdin, cdout, cderr = os.popen3('cdparanoia -d %s -R %i -'%(dev,i,))
    lmin, lmout, lmerr = os.popen3('lame -r -s 44.1 - -V 5 %s'%ofn)
    lmin.write(cdout.read())
    lmin.close()
    cdout.close()
#    for j in cderr:
#        print j.strip()
    cdin.close()
    cderr.close()
#    for j in lmerr:
#        print j.strip()
    lmout.close()
    lmerr.close()

