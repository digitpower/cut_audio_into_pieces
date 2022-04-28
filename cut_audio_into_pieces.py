from datetime import datetime
from pydub import AudioSegment
from itertools import cycle
import os
import sys
from pathlib import Path


g_base_dir = sys.argv[1]
original_audio_file = sys.argv[2]
xml_file = sys.argv[3]

g_mp3dir = g_base_dir + "/mp3s"
Path(g_mp3dir).mkdir(parents=True, exist_ok=True)

sound = AudioSegment.from_file(os.path.join(g_base_dir, f"{original_audio_file}.wav"))
sound.export(os.path.join(g_base_dir, f"{original_audio_file}.mp3"), format="mp3")



def take_portion_from_audio(start, end, portion_name) :
    FMT = '%M:%S.%f'
    dt_start = datetime.strptime(start, FMT)
    dt_end = datetime.strptime(end, FMT)
    tdelta = datetime.strptime(end, FMT) - datetime.strptime(start, FMT)
    
    first_cut_point = (dt_start.minute*60 + dt_start.second) * 1000 + dt_start.microsecond/1000
    last_cut_point = (dt_end.minute*60 + dt_end.second) * 1000 + dt_end.microsecond/1000
    
    sound_clip = sound[first_cut_point:last_cut_point]
    global g_mp3dir
    sound_clip.export(os.path.join(g_mp3dir, f"{start}_{end}_{last_cut_point}_{first_cut_point}_{last_cut_point-first_cut_point}.mp3"), format="mp3")
    print(last_cut_point, first_cut_point)

def take_portion_from_audio_bytimestamp(first_cut_point, last_cut_point, portion_name, timestamp) :
    sound_clip = sound[first_cut_point:last_cut_point]
    global g_mp3dir
    sound_clip.export(os.path.join(g_mp3dir, f"{timestamp}_{first_cut_point}_{last_cut_point}_{portion_name}.mp3"), format="mp3")

    
def get_start_end(line):
    fields = line.split(" ")
    start = fields[-3].replace('"', '')
    end = fields[-1].replace('"\n', '').replace('"', '')
    return [start, end]


import xml.etree.ElementTree as ET
root = ET.parse(f'{g_base_dir}/{xml_file}').getroot()



records = []

for type_tag in root.findall('annotations/annotation'):
    ts = type_tag.get('ts')
    speaker = type_tag.get('labeldata')
    records.append({"ts" : ts , "speaker" :speaker})
#print(records)


g_start_timestamp = 0



for i in range(len(records)):
    if i < len(records) - 1:
        if i == 0 : # We are on the first line
            start_tmstmp = int(records[i]["ts"].replace('.000000', ''))
            g_start_timestamp = start_tmstmp
        start_tmstmp = int(records[i]["ts"].replace('.000000', '')) - g_start_timestamp
        end_tmstmp = int(records[i+1]["ts"].replace('.000000', '')) - g_start_timestamp
        duration = end_tmstmp - start_tmstmp
        #print (f'start_tmstmp {start_tmstmp} end_tmstmp duration {end_tmstmp} duration {duration} portionname {records[i]["speaker"]}')
        take_portion_from_audio_bytimestamp(start_tmstmp*1000, end_tmstmp*1000, records[i]["speaker"], start_tmstmp)
    else :
        print('this', records[i])


# with open('filtered.txt') as f:
#     lines = f.readlines()
    
#     for line in lines:
#         start_end = get_start_end(line)
#         start = start_end[0]
#         end = start_end[1]
#         portion_name = ''
#         take_portion_from_audio(start, end, portion_name)