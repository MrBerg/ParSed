#!/usr/bin/env python
import sys
import argparse
import esm
#import esmre
import getch
import os.path

parser = argparse.ArgumentParser(description='ParSed - a parallel stream editor')
parser.add_argument('text_to_transform', nargs="?",  help='Text to be transformed (stdin)')
parser.add_argument('-i', '--input', nargs="*",  help='Name of input file(s) to apply filters to')
parser.add_argument('-o', '--output', nargs="*", help='Name of file(s) to save modified text to')
parser.add_argument('-f', '--filter', nargs="*", help='Name of file containing filters' )
parser.add_argument('-r', '--recursive', action="store_true", help='Allows for recursion')
#args = parser.parse_args(['--input', 'hello.py'])
args = parser.parse_args()

#this value is here for your safety. It's like a TTL flag on a packet.
max_recursion_depth = 100
def read_filter_file(file_name, trie, replacement_list):
	filter_file = open(file_name, "r")
	for line in filter_file:
		line = line.rstrip('\n')
		#might need a better split sign if we want to change 
		split_list = line.split(":=")
		if len(split_list) == 2:
			original = split_list[0].strip()
			changed = split_list[1].strip()
			#print(original, changed)
			#check whether same original is entered multiple times
			trie.enter(original)
			replacement_list[original] = changed
		else: 
			raise Exception("Your filter file is badly formatted.")
	filter_file.close()

def substitute(active_string, modified_text, trie, replacement_list, recursive):
	matches = trie.query(active_string)
	if not len(matches) == 0:
		#substitute the first match listed
		first_match_start = matches[0][0][0]
		#if the first match doesn't start at the first character in the active string, move all characters before the first match into the final modified string
		if not first_match_start == 0:
			modified_text = modified_text + active_string[0:first_match_start]
			active_string = active_string[first_match_start:]
		#checks first match in list right now
		first_match = matches[0][1]
		first_replacement = replacement_list[first_match]
		active_string = active_string.replace(active_string,first_replacement,1)
	return active_string, modified_text

def pass_through_text(text, trie, replacement_list, recursive):
	active_string = ''
	modified_text = ''
	index = 0
	if recursive:
		recursions = 0
		while index<len(text):
			char = text[index]
			if not char:
				break
			active_string = active_string + char
			previous_active_string = active_string
			active_string, modified_text = substitute(active_string, modified_text, trie, replacement_list,recursive)
			#TODO fix it
			if len(active_string) == len(previous_active_string):
				#this means a substitution has occurred. Add 1 recursion depth
				recursions = recursions + 1
			if recursions = max_recursion_depth:
				index = index + 1
				recursions = 0
	else:
		while index<len(text):
			char = text[index]
			if not char:
				#print "fooo!"
				break
			active_string = active_string + char
	#		matches = trie.query(active_string)
	#		if not len(matches) == 0:
	#			#substitute
	#			first_match_start = matches[0][0][0]
	#			if not first_match_start == 0:
	#				modified_text = modified_text + active_string[0:first_match_start]
	#				active_string = active_string[first_match_start:]
	#			#checks first match in list right now
	#			first_match = matches[0][1]
	#			first_replacement = replacement_list[first_match]
	#			active_string = active_string.replace(active_string,first_replacement,1)
			active_string, modified_text = substitute(active_string, modified_text,trie,replacement_list, recursive)
			index = index + 1
	modified_text = modified_text + active_string	
	return modified_text.rstrip('\n')
def pass_through_text_file(file_name, trie, replacement_list, recursive):	
	text_file = open(file_name, "r")
	active_string = ''
	modified_text = ''
	while True:
		#check whether UTF/ISO latin works
		char = text_file.read(1)
		#char = Getch.getch()
		#print char
		if not char:
			break
		active_string = active_string + char
#		matches = trie.query(active_string)
#		if not len(matches) == 0:
#			first_match_start = matches[0][0][0]
#			if not first_match_start == 0:
#				modified_text = modified_text + active_string[0:first_match_start]
#				active_string = active_string[first_match_start:]
#			#checks first match in list right now
#			first_match = matches[0][1]
#			first_replacement = replacement_list[first_match]
#			active_string = active_string.replace(active_string,first_replacement,1)
		active_string, modified_text = substitute(active_string, modified_text,trie,replacement_list, recursive)
	modified_text = modified_text + active_string
	return modified_text.rstrip('\n')
def main():
	trie = esm.Index()
	replacement_list = {}
	recursive = args.recursive
	#TODO add inline filter
	if len(args.filter) >= 1:
		for filter_file in args.filter:
			read_filter_file(filter_file,trie,replacement_list)
	else: #TODO
		pass
	trie.fix()
	modified_text = ''
	if args.input and args.output:
	#TODO fixa att antalet in och output matchar
		if len(args.input) == len(args.output) and len(args.input) >= 1:
	 		for input_file in args.input:
				modified_text = pass_through_text_file(input_file, trie, replacement_list, recursive)
				output_file_name = args.output[args.input.index(input_file)]
				output_file = open(output_file_name, "w")
				print >>output_file, modified_text
				output_file.close()
	else:
		#TODO add stream reading and reading from stdio
		#modified_text = pass_through_stream(trie,replacement_list)
		if args.text_to_transform:
			#if os.path.isfile(args.text_to_transform) and not args.text_to_transform.istty():
			#	text_to_transform = args.text_to_transform.read()
			#else: 
			#	text_to_transform = args.text_to_transform

			modified_text = pass_through_text(args.text_to_transform, trie, replacement_list, recursive)
		if args.input:
			#if os.path.isfile(args.input[0])
			modified_text = pass_through_text_file(args.input[0], trie, replacement_list, recursive)
		if args.output:
			output_file = open(args.output, "w")
			print >>output_file, modified_text
			output_file.close()
		else:
			print modified_text
main()
