import urllib2,urllib,os,eyed3,time
eyed3.log.setLevel("ERROR")
def similar(w1, w2):
    w1 = w1 + ' ' * (len(w2) - len(w1))
    w2 = w2 + ' ' * (len(w1) - len(w2))
    return sum(1 if i == j else 0 for i, j in zip(w1.lower(), w2.lower())) / float(len(w1))

path = "C:/Users/Dylan/Music"
songs = os.listdir(path)
match = list()
iffy = list()
nono = list()
for song in songs:
    if 'mp3' not in song: continue
    audiofile = eyed3.load(path+'/'+song)
    #print audiofile.tag.title
    name = song[:song.index("(")] if "(" in song else audiofile.tag.title
    url = "http://search.azlyrics.com/search.php?"+urllib.urlencode({"q":name+' '+str(audiofile.tag.artist)})
    response = urllib2.urlopen(url)
    html = response.read()
    with open('f.txt','w') as f:
        f.write(html)
    lister = html.index('1.')
    #print lister-len(name)
    html = html[lister-len(name):]
    bold = html.index("<b>",lister)
    #print html[bold:html.index("</b>",bold)]
    try:
        l1 = html.index('<a href="http://www.azlyrics.com/lyrics/')
    except ValueError:
        print 'Song Not Found: '+name
        continue
    l2 = html.index("by",l1)
    title,artist = html[html.index("<b>",l1)+3:html.index("</b>",l1)], html[l2+6:html.index("</b>",l2)].lower().replace("the","")
    while artist.startswith(" "): artist = artist[1:]
    print title, artist, similar(title,name), similar(artist,str(audiofile.tag.artist))
    #raise SystemExit
    #time.sleep(3)
##if 'no results' data:
##    print name, 'no results found'
