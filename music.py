import os
from mutagen.mp3 import MP3
from collections import *
def count():
    path = "C:/Users/Dylan/Music"
    total = 0
    for folder in next(os.walk(path))[1]:
        npath = path+'/'+folder
        for name in os.listdir(npath):
            if name.endswith(".mp3"):
                audio = MP3(npath+'/'+name)
                total += int(audio.info.length)
    print total
string = """ Cry Baby 00:04
 Mess Around 04:11
 Sweetie Little Jean 07:04
 Too Late to Say Goodbye 10:49
 Cold Cold Cold 15:02
 Trouble 18:35
 How Are You True 22:23
 That's Right 27:04
 Punchin' Bag 30:57
 Portuguese Knife Fight 34:44"""
album = "Tell Me I'm Pretty"
def convert():
    times = OrderedDict()
    for line in string.split('\n'):
        times[line[line.index(' ')+1:line.index(":")-3]] = line[line.index(":")-2:line.index(":")+3]
    from pydub import AudioSegment
    path = "C:/Users/Dylan/Music/"+album+"/"
    name = "full.mp3"
    song = AudioSegment.from_mp3(path+name)
    times = list(times.items())
    bSeconds = 0
    for index,time in enumerate(times):
        if index + 1 != len(times):
            eSeconds = (int(times[index+1][1][:2])*60)+int(times[index+1][1][3:])
        else:
            eSeconds = song.duration_seconds*1000
        eSeconds *= 1000
        curr = song[bSeconds:eSeconds]
        out_f = open(path+time[0]+".mp3", 'wb')
        curr.export(out_f,format='mp3',tags={'artist': 'Cage The Elephant', 'album': album,'title':time[0]})
        out_f.close()
        bSeconds = eSeconds
        print time[0]
