from pydub import AudioSegment
from pydub.utils import make_chunks
import io, os, sys

CUE = str(sys.argv[1])
WAV = str(sys.argv[2])

# 对cue文件进行处理，得到字典 process the cue file to dict
fp = io.open(CUE,'r',encoding='utf-8')
cue = []
song = {}
for line in fp.readlines():
    text = line.strip()

    if text[:5]=='TRACK':
        song = {}
        continue

    if text[:5]=='TITLE':
        song['TITLE']= text[7:-1]
        continue
    
    if text[:9]=='PERFORMER':
        song['PERFORMER'] = text[11:-1]
        continue
    
    if text[:8]=='INDEX 01':
        song['INDEX01'] = text[9:]
    
    if len(song.keys())>=3:
        cue.append(song)  

fp.close

# 获取需要cut的节点（line）和音乐的标题 get the point that we need to cut(which is the list: line) and the music title
line=[]
title=[]
for i in range(len(cue)):
    minute = int(cue[i]['INDEX01'][:2]) 
    second = int(cue[i]['INDEX01'][3:5])
    ms = int(cue[i]['INDEX01'][6:8])
    line.append((minute*60+second)*1000+ms)
    title.append(cue[i]['TITLE']+'.wav')

# 打开音频文件 open the music file
wav = AudioSegment.from_file(WAV)
finish=wav.duration_seconds*1000 # 增加结束点 add the finish point
line.append(finish)
for i in range(len(line)-1):
    begin = line[i]
    finish = line[i+1]
    song = wav[begin:finish]
    song.export(title[i],format='wav')