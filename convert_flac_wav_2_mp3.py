#!/usr/bin/python3

from pydub import AudioSegment
import os

files = [f for f in os.listdir('./') if os.path.splitext(f)[1] in [".flac", ".wav"]]
file_wma = [f for f in os.listdir('./') if os.path.splitext(f)[1] == ".wma"]

sub_dir = [f for f in os.listdir('./') if os.path.isdir(f)]

for i in sub_dir:
	files.extend([(i + '/' +  f) for f in os.listdir(i) if os.path.splitext(f)[1] in [".flac", ".wav"]])
	file_wma.extend([(i + '/' +  f) for f in os.listdir(i) if os.path.splitext(f)[1] == ".wma"])
	
def convert(old_file, new_file):
	if os.path.splitext(old_file)[1] == ".flac":
		song = AudioSegment.from_file(old_file, "flac")	
	elif os.path.splitext(old_file)[1] == ".wav":
		song = AudioSegment.from_file(old_file, "wav")
	print('Converting ' + old_file + '\t' + new_file)
	song.export(new_file, format="mp3", bitrate="320k")
	
for i in files:
	new_dir = 'converted_' + os.path.dirname(i)
	new_name = os.path.splitext(os.path.basename(i))[0] + '.mp3'
	new_file = new_dir + '/' + new_name
	if os.path.isfile(new_file):
		print('Skip convert ' + i + '. File exists in ' + new_dir + '/')
	elif not os.path.exists(new_dir):
		os.mkdir(new_dir)
		convert(i, new_file)
	else:
		convert(i, new_file)
	
if file_wma:
	print('')
	print('Convert failed for:' )  ##ffmpeg not support .wma format
	for i in file_wma:
		print(i)
		



