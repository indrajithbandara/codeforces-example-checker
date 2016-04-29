import os, sys, urllib, re, subprocess
from bs4 import BeautifulSoup

to_replace = {
	"&gt;" : '>',
	"&lt;" : '<'
}

def get_link(file):
	with open(file, 'r') as infile:
		return infile.readline()[2:]

def convert_repl(string):
	for k, v in to_replace.items():
		string.replace(k, v)
	return string

def compile(name):
	name = name[:name.find('.')]
	if lang == "c++":
		subprocess.call(["g++", source, "-o", name])

def run(name, input):
	if lang == "c++":
		p = subprocess.Popen(["./" + name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = p.communicate(input.encode("utf-8"))
	return stdout.decode("utf-8")

def comp_test(texample, tuser, nr):
	if (texample == tuser):
		print ("Test" + str(nr) + ": [OK]")
	else: 
		print("Test" + str(nr) + ": [X]\n" + "Input:\n" + i_lines +
			  "Your answer:\n" + tuser + "\nExpected answer:\n" + texample)

def main(soup):
	compile(source)
	if lang == "c++": exe = source[:source.find('.')]
	inputs = soup.find_all('div', attrs = {"class" : "input"})
	outputs = soup.find_all('div', attrs = {"class" : "output"})
	test_nr = 0

	for pre_input, pre_output in zip(inputs, outputs):
		test_nr += 1
		raw_in = pre_input.find_all('pre')
		raw_out = pre_output.find_all('pre')

		pat = r"\>(.+?)\<"

		raw_in = re.findall(pat, str(raw_in))
		raw_out = re.findall(pat, str(raw_out))

		input_str = ""
		output_str = ""
		for line in raw_in: 
			input_str += convert_repl(line) + '\n'

		stdout = run(exe, input_str)

		if len(raw_out) > 1: 
			for line in raw_out: output_str += line + '\n'
		else: output_str = raw_out[0]

		print(80 * '-')
		comp_test(stdout, output_str, test_nr)

source = sys.argv[1]
link = get_link(source)
lang = "c++"

web_page = urllib.request.urlopen(link)
soup_page = BeautifulSoup(web_page, "html.parser")

main(soup_page)
