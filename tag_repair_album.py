#!/usr/bin/python3

import os,re,sys
import taglib
from distutils.util import strtobool

def check_file_name(file_list):
	bad_name_file_list = []
	for i in file_list:
		pure_name = os.path.splitext(os.path.basename(i))[0]
		if len(pure_name.split(' - ')) <= 1 or len(pure_name.split(' - ')) >= 4:
			bad_name_file_list.append(i)
	return bad_name_file_list

def check_tag_album(file_list):

	tag_album_diff = []
	for i in file_list:
		song = taglib.File(i)
		section_list = os.path.splitext(os.path.basename(i))[0].split(' - ')
		
		if len(section_list) == 3:
			new_album = section_list[2].strip()
			
			old_album = 'null'
			if 'ALBUM' in song.tags:
				old_album = song.tags['ALBUM'][0]
			song = {}
			song['file'] = i
			song['old_album'] = old_album
			song['new_album'] = new_album
			tag_album_diff.append(song)
	return tag_album_diff

def process_tag_album(tag_album_diff):
	for i in tag_album_diff:
		song = taglib.File(i['file'])
		song.tags['ALBUM'] = i['new_album']
		song.save()
		

if __name__ == '__main__':
	music_files = [f for f in os.listdir('./') if os.path.splitext(f)[1] in [".flac", ".wav", ".wma", ".mp3"]]
	sub_dir = [f for f in os.listdir('./') if os.path.isdir(f)]
	for i in sub_dir:
		music_files.extend([(i + '/' +  f) for f in os.listdir(i) if os.path.splitext(f)[1] in [".flac", ".wav", ".wma", ".mp3"]])
	
	#for i in music_files:
	#	print(i)
		
	bad_name_file_list = check_file_name(music_files)
	
	if bad_name_file_list:
		print("Error! Check these files name:")
		for i in bad_name_file_list:
			print('\t' + i)
		sys.exit()
	
	tag_album_diff = check_tag_album(music_files)
	
	if tag_album_diff:
		print('Ready to change:')
		for i in tag_album_diff:
			print('\t' + i['file'] + '\tALBUM: \"' + i['old_album'] + '\"  ------->  \"' + i['new_album'] + '\"')
	else:
		print("Nothing needs to be change. Exit.")
		sys.exit()
	
	print('')
	print("Warning!!! please check every item. you may cover the original(right) TAG from file name (wrong TAG)")
	print("Are you sure to continue? Press y/yes to Continue, or press n/no to exit:")
	
	while True:
		try:
			if strtobool(input().lower()):
				process_tag_album(tag_album_diff)
				print("Finished. Exit.")
				sys.exit()
			else:
				print("Nothing changed. Exit.")
				sys.exit()
		except ValueError:
			print("Input error! Exit.")
			sys.exit()
			