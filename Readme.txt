I ran it on ubuntu 22.04
pip install pydub ffmpeg ffmpeg-python
sudo apt install ffmpeg



#1-st argument: Directory, where original mp3 file resides  (/home/user/Downloads/audios/A)
#2-nd argument: basename of file, without extension(mp3)    (07092021_liza_guben_60e856e5_0_0_102_77)
#3-rd argument: xml file                                    (07092021_liza_guben_20210709.xml)
python3 cut_audio_into_pieces.py /home/user/Downloads/audios/A 07092021_liza_guben_60e856e5_0_0_102_77 07092021_liza_guben_20210709.xml

Output is folder /home/user/Downloads/audios/A/mp3s, where folders will be created for each speaker.
├── Alf
│   ├── 1625839585_1625839600.mp3
│   ├── 1625840493_1625840501.mp3
│   └── combined.mp3
├── almon
│   ├── 1625839545_1625839551.mp3
│   └── combined.mp3
├── ap
│   ├── 1625842761_1625842765.mp3
│   └── combined.mp3
In Each speacker folder there will be created mp3-s for this speaker and also combined audio for this speacker.
