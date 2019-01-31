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

def check_tag_title(file_list):

	tag_title_diff = []
	for i in file_list:
		song = taglib.File(i)
		section_list = os.path.splitext(os.path.basename(i))[0].split(' - ')
		
		old_title = 'null'
		if 'TITLE' in song.tags:
			old_title = song.tags['TITLE'][0]
		
		new_title = section_list[1].strip()
			
		if old_title != new_title:
			song = {}
			song['file'] = i
			song['old_title'] = old_title
			song['new_title'] = new_title
			tag_title_diff.append(song)
	return tag_title_diff

def process_tag_title(tag_title_diff):
	for i in tag_title_diff:
		song = taglib.File(i['file'])
		song.tags['TITLE'] = i['new_title']
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
	
	tag_title_diff = check_tag_title(music_files)
	
	if tag_title_diff:
		print('Ready to change:')
		for i in tag_title_diff:
			print('\t' + i['file'] + '\tTITLE: \"' + i['old_title'] + '\"  ------->  \"' + i['new_title'] + '\"')
	else:
		print("Nothing needs to be change. Exit.")
		sys.exit()
	
	print('')
	print("Warning!!! please check every item. you may cover the original(right) TAG from file name (wrong TAG)")
	print("Are you sure to continue? Press y/yes to Continue, or press n/no to exit:")
	
	while True:
		try:
			if strtobool(input().lower()):
				process_tag_title(tag_title_diff)
				print("Finished. Exit.")
				sys.exit()
			else:
				print("Nothing changed. Exit.")
				sys.exit()
		except ValueError:
			print("Input error! Exit.")
			sys.exit()
			