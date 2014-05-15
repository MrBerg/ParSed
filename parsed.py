#!/usr/bin/env python
import sys
import argparse
import esm
import getch
import os.path

parser = argparse.ArgumentParser(description='ParSed - a parallel stream editor')
parser.add_argument('-i', '--input', nargs="+",  help='Name of input file(s) to apply filters to')
parser.add_argument('-o', '--output', nargs="*", help='Name of file(s) to save modified text to')
parser.add_argument('-f', '--filter', nargs="+", help='Name of file(s) containing filters' )
parser.add_argument('-r', '--recursions', nargs="?", metavar='N', type=int, default=0, help='Allows for N recursions, default 0')
args = parser.parse_args()

#max_recursion_depth like a TTL flag on a packet.
max_recursion_depth = args.recursions
def read_filter_file(file_name, trie, replacement_list):
	filter_file = open(file_name, "r")
	for line in filter_file:
		line = line.rstrip('\n')
		#might need a better split sign if we want to change some pseudocode
		split_list = line.split(":=")
		if len(split_list) == 2:
			original = split_list[0].strip()
			changed = split_list[1].strip()
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
		first_match = matches[0][1]
		first_replacement = replacement_list[first_match]
		active_string = active_string.replace(first_match,first_replacement,1)
		substitution_has_occured = True
	else:
		substitution_has_occured = False
	return active_string, modified_text, substitution_has_occured

def pass_through_text(text, trie, replacement_list, recursive):
	active_string = ''
	modified_text = ''
	index = 0
	length = len(text)
	change_detected = False
	if recursive:
		recursions = 0
		while index<length:
			if index<len(text):
				char = text[index]
			else:
				break
			if not char:
				break
			active_string = active_string + char
			prev_active_string = active_string
			prev_modified_text = modified_text
			active_string, modified_text, change_detected = substitute(active_string, modified_text, trie, replacement_list,recursive)
			#TODO fix it
			while recursions < max_recursion_depth and change_detected:
				recursions = recursions + 1
				prev_active_string = active_string
				active_string, modified_text, change_detected = substitute(active_string, modified_text,trie,replacement_list, recursive)
				if change_detected:
					length = length + (len(active_string) - len(prev_active_string))
			if recursions > 0:
				modified_text = modified_text + active_string[0]
				active_string = active_string[1:]
			index = index + 1
			recursions = 0
	else:
		while index<length:
			char = text[index]
			if not char:
				break
			active_string = active_string + char
			active_string, modified_text, change_detected = substitute(active_string, modified_text,trie,replacement_list, recursive)
			index = index + 1
	modified_text = modified_text + active_string	
	return modified_text.rstrip('\n')
def pass_through_text_file(file_name, trie, replacement_list, recursive):	
	text_file = open(file_name, "r")
	active_string = ''
	modified_text = ''
	for line in text_file:
		modified_line = pass_through_text(line.rstrip('\n'), trie, replacement_list, recursive)
		modified_text = modified_text + '\n' + modified_line
	return modified_text.rstrip('\n').lstrip('\n')
def main():
	trie = esm.Index()
	replacement_list = {}
	recursive = args.recursions > 0
	if args.filter and len(args.filter) >= 1:
		for filter_file in args.filter:
			read_filter_file(filter_file,trie,replacement_list)
	else:
		raise Exception("There's no point to this program if you don't want to change anything. It would just be a clumsier echo.")
	trie.fix()
	modified_text = ''
	if args.input and len(args.input) >= 1:
 		for input_file in args.input:
			modified_text = pass_through_text_file(input_file, trie, replacement_list, recursive)
			if args.output and len(args.output):
				if len(args.output) >= len(args.input):
					output_file_name = args.output[args.input.index(input_file)]
					output_file = open(output_file_name, "w")
					print >>output_file, modified_text
					output_file.close()
				else:
					output_file_name = args.output[0]
					output_file = open(output_file_name, "a")
					print >>output_file, modified_text
					output_file.close()
			else:
				print modified_text
main()
