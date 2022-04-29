from pydub import AudioSegment
from itertools import cycle
import os
import sys
from pathlib import Path


g_base_dir = sys.argv[1]
original_audio_file = sys.argv[2]
xml_file = sys.argv[3]

dest_mp3s = f'{g_base_dir}/mp3s'
sound = AudioSegment.from_file(os.path.join(g_base_dir, f"{original_audio_file}.mp3"))

g_start_timestamp = 0

def take_portion_from_audio(timestamp_start, timestamp_end, portion_name) :

    #We need cut points in milliseconds, so we multiple to 1000
    first_cut_point = (timestamp_start - g_start_timestamp)*1000
    last_cut_point = (timestamp_end - g_start_timestamp)*1000
    
    sound_clip = sound[first_cut_point:last_cut_point]
    portion_name = portion_name.replace(' ', '_')
    dest_path = f'{dest_mp3s}/{portion_name}'
    Path(dest_path).mkdir(parents=True, exist_ok=True)
    sound_clip.export(os.path.join(dest_path, f"{timestamp_start}_{timestamp_end}.mp3"), format="mp3")

records = []
import xml.etree.ElementTree as ET
root = ET.parse(f'{g_base_dir}/{xml_file}').getroot()

for type_tag in root.findall('annotations/annotation'):
    ts = type_tag.get('ts')
    speaker = type_tag.get('labeldata')
    records.append({"ts" : ts , "speaker" :speaker})

for i in range(len(records)):
    if i < len(records) - 1:
        #get timestamp_end from current line and timestamp_end from next line
        timestamp_start = int(records[i]["ts"].replace('.000000', ''))
        timestamp_end = int(records[i+1]["ts"].replace('.000000', ''))
        
        # We are on the first line of xml
        if i == 0 : 
            g_start_timestamp = timestamp_start
 
        # We need start and end timestamps in milliseconds
        take_portion_from_audio(timestamp_start, timestamp_end, records[i]["speaker"])
    else :
        #This is final line
        print('Final line of xmlfile', records[i])

# Get sorted speakers dirs
speakers_dirs = []
for dir in os.scandir(dest_mp3s):
    if dir.is_dir():
        speakers_dirs.append(dir.name)
speakers_dirs.sort()

#Iterate each speaker dir
for dir in speakers_dirs :
    person_dir = f"{dest_mp3s}/{dir}"
    print(person_dir)
    for _, _, f_list in os.walk(person_dir):
        combined_file = AudioSegment.empty()
        #Iterate each mp3 file for this speaker
        # and combine all of them into one final file.
        # Final filename will be conbined.mp3
        for file in f_list:
            print(f'    {file}')
            try:
                audio_segment = AudioSegment.from_file(f"{person_dir}/{file}", format="mp3")
                combined_file += audio_segment
            except:
                print(f'        {file} failed to combine')
        combined_file.export(f"{person_dir}/combined.mp3", format="mp3")
