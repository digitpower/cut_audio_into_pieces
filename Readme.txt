I ran it on ubuntu 22.04
pip install pydub ffmpeg ffmpeg-python
sudo apt install ffmpeg



#1-st argument: Directory, where original mp3 file resides  (/home/user/Downloads/audios/A)
#2-nd argument: basename of file, without extension(mp3)    (07092021_liza_guben_60e856e5_0_0_102_77)
#3-rd argument: xml file                                    (07092021_liza_guben_20210709.xml)
python3 cut_audio_into_pieces.py /home/user/Downloads/audios/A 07092021_liza_guben_60e856e5_0_0_102_77 07092021_liza_guben_20210709.xml

output is folder /home/user/Downloads/audios/A/mp3s


I will change python code to create specific folder for each speaker
