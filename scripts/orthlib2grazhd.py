#!/usr/bin/python
import os, re
import csltranscode as CT
from tqdm import tqdm

def list_files(path, pattern):
	file_list = []
	for sd in os.listdir(path):
		subpath = path + '/' + sd
		if os.path.isdir(subpath):
			file_list += list_files(subpath, pattern)
		else:
			if re.match(pattern, sd):
				file_list += [subpath]
	return(file_list)


def sub_by_dictionary_simple(string, dictionary):
    for item in dictionary.keys():
        string = re.sub(item, dictionary[item], string)
    return string

uncolor_one_letter = {
    r'%<([a-zA-Zа-яА-Я\'`"^=_<>\\~-]+)%>([a-zA-Zа-яА-Я\'`"^=_<>\\~-])' : r'\1\2',
    r'(\s[^%\s]*)%>([a-zA-Zа-яА-Я\'`"^=_<>\\~-])' : r'%>\1\2',
    r'%<([_<]*(А|И|О|W|О_у|О_У)[=\'"^`]*>*)%>' : r'\1'
}

split_kinovar = {
	'%<' : '*',
	r'%>\s*$' : '*',
	r'%>\s*' : '*\n'

}


def convert_paragraph(paragraph, out_enc):
	# убрать выделения одной буквы
	paragraph = sub_by_dictionary_simple(paragraph, uncolor_one_letter)
	paragraph =  CT.csl_transcode(paragraph, 'hip', out_enc)
	paragraph = sub_by_dictionary_simple(paragraph, split_kinovar)
	return(paragraph)


def convert_file(input_file, output_file, out_enc):
	try:
		# print (input_file)
		os.makedirs(os.path.dirname(output_file), exist_ok=True)
		with open(output_file, 'w') as f_out:
			with open(input_file, 'rt') as f:
				paragraph = ''
				while True:
					line = f.readline()
					if not line:
						if not whiteline.match(paragraph):
							print(convert_paragraph(paragraph, out_enc), file = f_out)
						break
					if whiteline.match(line): # blank line
						if not whiteline.match(paragraph):
							print(convert_paragraph(paragraph, out_enc) + '\n', file = f_out)
						paragraph = ''
					if paragraph == '':
	 					paragraph = line.strip()
					else:
						paragraph += ' ' + line.strip()
	except:
		print ("Oops, something went wrong with file ", input_file)


whiteline = re.compile('^\s*$')

in_path = '/Users/pantlmn/Desktop/slavcorpora/hip/orthlib'
out_path = '/Users/pantlmn/Desktop/slavcorpora/grazhd/orthlib-from-hip'
file_list = list_files(in_path, '.*hip')

for input_file in tqdm(file_list):
		output_file = out_path + input_file[len(in_path):]
		convert_file(input_file, output_file, 'grazhd')

