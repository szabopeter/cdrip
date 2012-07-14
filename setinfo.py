#!/usr/bin/python

import os
import sys
import eyeD3

sglob = {}
sloc = { 'mp3'   : {},
         'title' : {},
         'perf'  : {},
         'genre' : {},
         'cmt'   : {},
         'year'  : {},
         'cddb'  : {},
         'cdindex' : {},
         'comments' : {},
         'defcomments' : {},
         'alltitles' : '',
         'allperfs'  : '',
         'album'    : {},
         }
try:
    ss = sys.argv[1]
except IndexError:
    ss = 'cdripinfo.txt'

try:
    execfile(ss,sglob,sloc)
except SyntaxError,e:
    ofs = e.offset
    lin = e.lineno
    msg = e.msg
    fn  = e.filename
    print "Syntax error: %s in %s line %s char %s."%(
                         msg,  fn,     lin,    ofs, )
    print e[:]
#    print dir(SyntaxError)
    sys.exit()

locals().update(sloc)
nrs = mp3.keys()

#print sloc

#print ttl, "tracks", idCDDB, idCDINDEX
alltitles = alltitles.strip()
allperfs = allperfs.strip()
if alltitles:
    alltitles = alltitles.split("\n")
    if len(alltitles)<len(nrs):
        sys.stderr.write('Warning: alltitles does not have all titles!\n')
    while len(alltitles)<len(nrs):
        alltitles.append(None)
if allperfs:
    allperfs = allperfs.split('\n')
    while len(allperfs)<len(nrs):
        sys.stderr.write('Warning: allperfs does not have entries for all files!\n')
    while len(allperfs)<len(nrs):
        allperfs.append(None)
for i in nrs:
    #print mp3[i],perf[i],title[i],genre.get(i,None)
    fn = mp3[i]
    at = perf.get(i,None)
    if not at:
        at = allperfs[nrs.index(i)]
    tt = title.get(i,None)
    if not tt:
        tt = alltitles[nrs.index(i)]
    al = album.get(i,T)
    gr = genre.get(i,g)
    ct = cmt.get(i,defcomments)
    yr = year.get(i,y)
    ct.update(comments)
    
    if idCDDB and not 'CDDB' in ct.keys():
        ct['CDDB'] = idCDDB
    if idCDINDEX and not 'CDINDEX' in ct.keys():
        ct['CDINDEX'] = idCDINDEX

    
    try:
        tagfile = eyeD3.Mp3AudioFile(fn)
    except IOError:
        sys.stderr.write('No file by the name %s here!\n'%fn)
    tag = tagfile.getTag()
    if tag == None:
        tag = eyeD3.Tag(fn)
        tag.setVersion(eyeD3.ID3_DEFAULT_VERSION)
    
    eargs = ['eyeD3']
    argv = []
    ln = fn+' :'
    if tt:
        ln += ' %s'%tt
        tag.setTitle(tt)
        eargs.append("-t '%s'"%tt)
        argv.extend(['-t',tt])
    if at:
        ln += ' by %s'%at
        tag.setArtist(at)
        eargs.append("-a '%s'"%at)
        argv.extend(['-a',at])
    if al:
        ln += ' from the album %s'%al
        tag.setAlbum(al)
        eargs.append("-A '%s'"%al)
        argv.extend(['-A',al])
    if gr:
        ln += ' (genre: %s)'%gr
        tag.setGenre(gr)
        eargs.append("-G '%s'"%gr)
        argv.extend(['-G',gr])
    if yr:
        ln += ' (year: %s)'%yr
        tag.setDate(yr)
        eargs.append('-Y "%s"'%yr)
        argv.extend(['-Y',str(yr)])
    if ct:
        ln += '\nComments'+str(ct)
        #print ct
        for k, v in ct.items():
            tag.addComment(v,k)
            eargs.append("--comment=':%s:%s'"%(k,v,))
            argv.append("--comment=':%s:%s'"%(k,v,))
    tag.setTrackNum([i,ttl])
    eargs.append("-n %i"%i)
    eargs.append("-N %i"%ttl)

    eargs.append("'%s'"%fn)
    argv.extend( ["-n", str(i), "-N", str(ttl), fn] )
    
    tag.update()
    del tag
    #print " ".join(eargs)
    #print argv
    #print os.spawnv(os.P_WAIT,'/usr/bin/eyeD3',argv)
#    fin,fout,ferr = os.popen3('/usr/bin/eyeD3 '+" ".join(argv))
#    print fout.read()
#    print ferr.read()
#    fin.close()
#    fout.close()
#    ferr.close()
##    argv = ['eyeD3'] + argv
##    for i in argv:
##        if type(i) != type(""):
##            print "------------------: ",i
##    if os.fork() == 0:
##        print os.execl('/usr/bin/', argv)
