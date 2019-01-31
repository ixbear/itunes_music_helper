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

def check_tag_artist(file_list):

	tag_artist_diff = []
	for i in file_list:
		song = taglib.File(i)
		section_list = os.path.splitext(os.path.basename(i))[0].split(' - ')
		
		old_artist = []
		if 'ARTIST' in song.tags:
			for artists in song.tags['ARTIST']:
				artist = re.split(',|\;|\/|\&',artists)
				old_artist.extend(artist)
		else:
			old_artist = ['null']

		artists_from_file_name = re.split(',|\;|\&',section_list[0])
		
		new_artist = []
		for a in artists_from_file_name:
			new_artist.append(a.strip())
			
		if old_artist != new_artist:
			song = {}
			song['file'] = i
			song['old_artist'] = old_artist
			song['new_artist'] = new_artist
			tag_artist_diff.append(song)
	return tag_artist_diff

def process_tag_artist(tag_artist_diff):
	for i in tag_artist_diff:
		song = taglib.File(i['file'])
		song.tags['ARTIST'] = i['new_artist']
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
	
	tag_artist_diff = check_tag_artist(music_files)
	
	if tag_artist_diff:
		print('Ready to change:')
		for i in tag_artist_diff:
			print('\t' + i['file'] + '\tARTIST: \"' + ','.join(i['old_artist']) + '\"  ------->  \"' + ','.join(i['new_artist']) + '\"')
	else:
		print("Nothing needs to be change. Exit.")
		sys.exit()
	
	print('')
	print("Warning!!! please check every item. you may cover the original(right) TAG from file name (wrong TAG)")
	print("Are you sure to continue? Press y/yes to Continue, or press n/no to exit:")
	
	while True:
		try:
			if strtobool(input().lower()):
				process_tag_artist(tag_artist_diff)
				print("Finished. Exit.")
				sys.exit()
			else:
				print("Nothing changed. Exit.")
				sys.exit()
		except ValueError:
			print("Input error! Exit.")
			sys.exit()
			