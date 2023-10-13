#!/usr/bin/python3
# author: suffs811
# Copyright (c) 2023 suffs811
# https://github.com/suffs811/fuzzler.git
# read the README.md file for more details; software distributed under MIT license; for personal, legal use only.
#
# usage: python3 fuzzler.py -t <target_ip> (optional -p to specify port other than 80)
#
# note <> you may have to specify the specific version of python3 you are running:
# (python3.6 fuzzler.py ... || python3.9 fuzzler.py ... etc.)


import os
import argparse
from datetime import datetime
import sys
import time

print('''
### ###  ##  ###  ### ##   ### ##   ####     ### ###  ### ##
 ##  ##  ##   ##  ##  ##   ##  ##    ##       ##  ##   ##  ##
 ##      ##   ##     ##       ##     ##       ##       ##  ##
 ## ##   ##   ##    ##       ##      ##       ## ##    ## ##
 ##      ##   ##   ##       ##       ##       ##       ## ##
 ##      ##   ##  ##  ##   ##  ##    ##  ##   ##  ##   ##  ##
####      ## ##   # ####   # ####   ### ###  ### ###  #### ##
\n
\\ created by: suffs811
\\ https://github.com/suffs811/fuzzler.git
''')

time.sleep(2)

# install nltk library
print("\n### downloading nltk library ###\n")
os.system("python3 -m pip install --upgrade pip")
if "nltk" in sys.modules:
	print("nltk library already installed")
else:
	os.system("python3 -m pip install nltk || echo '*** error installing nltk; please install manually before proceeding ***'")
import nltk
nltk.download("wordnet")
nltk.download("omw-1.4")
from nltk.corpus import wordnet as wn


# set up arguments for script
parser = argparse.ArgumentParser(description="script for creating tailored password lists using Machine Learning")
parser.add_argument("-t", "--targetip", help="specify target ip to crawl")
parser.add_argument("-p", "--port", help="specify target port (default=80)")
args = parser.parse_args()
ip = args.targetip
port = args.port


# ensure necessary tools are downloaded and check if fuzzed pswd file already exists
def preCheck():

	# download cewl and hashcat
	print("\n### downloading necessary tools and libraries ###\n")


	deps = ["cewl", "hashcat"]
	for dep in deps:
		exists = os.system("which {}".format(dep))

		if exists != 0:
			os.system("sudo apt install {}".format(dep))

	# check for fuzzes.txt; if exists, return new unique file name using datetime
	if os.path.exists("fuzzes.txt"):
		answer = input("\n *** fuzzes.txt already exists, do you want to replace it? (y/n) ***\n")
		if answer.lower() == "y":
			os.system("rm -f fuzzes.txt")
			nFile = "fuzzes.txt"
		elif answer.lower() == "n":
			# get current time to make unique file name
			now = datetime.now()
			time = now.strftime("%H%M%S")
			nFile = "fuzzes_{}.txt".format(time)
		else:
			print("\n*** please specify either 'y' or 'n' ***")
			preCheck()
		return nFile
	else:
		nFile = "fuzzes.txt"
		return nFile


# crawl the webpage and gather words for password list
def crawl(ip, port):
	
	# check if port was specified, use default if not
	if port:
		tport = port
	else:
		tport = "80"
	print("\n### crawling {}:{} ###".format(ip, tport))
	os.system("cewl -d 2 -m 3 -e -w cewlPass.txt http://{}:{}".format(ip, tport))

	# find emails and grab username and domain, add to list
	with open("cewlPass.txt") as fp:
		f = fp.readlines()
		for line in f:
			if "@" in line:
				nline = line.split("@")
				for i in nline:
					if "." in i:
						nnline = nline.split(".")[0]
						fp.write(nnline)
					else:
						continue
			else:
				continue


# use natural language processing to add similar words to the list
def extend(ip):
	print("\n### generating new words with nlp ###")
	os.system("touch prePass_{}.txt".format(ip))
	with open("cewlPass.txt", "r") as fp, open("prePass_{}.txt".format(ip), "a") as fw:
		fr = fp.readlines()
		sets = []
		addWords = []
		for line in fr:
			sets.append(line.lower().strip())
		for s in sets:
			synset = wn.synsets(s)
			if synset:
				for syn in synset:
					newWords = [str(lemma.name()) for lemma in syn.lemmas()]
					for w in newWords:
						addWords.append(w.strip())
			else:
				continue
		addWords = list(set(addWords))
		for i in addWords:
			fw.write(i.strip())
			fw.write("\n")


# fuzz the list of words (lowercase, uppercase, capitalize, capitalize all but first letter, reverse word, prepend/append digits 0-9999, and translate to 1337 speak
def fuzz(ip, path):
	print("\n### fuzzing word list with hashcat ###")
	rules = [':', 'l', 'u', 'c', 'C', 't', 'r', 'd', 'sa@', 'sa4', 'se3', 'sl1', 'sa@ se3 sl1', 'sa4 se3 sl1']
	rulesFile = ""

	# check if the hascat rules file exists; if exists, create unique file name
	if os.path.exists("fuzz.rule"):
		now = datetime.now()
		time = now.strftime("%H%M%S")
		os.system("touch fuzz_{}.rule".format(time))
		rulesFile = "fuzz_{}.rule".format(time)
	else:
		os.system("touch fuzz.rule")
		rulesFile = "fuzz.rule"
	with open(rulesFile, "a") as r:
		for rule in rules:
			r.write(rule+"\n")

	passFile = "prePass_{}.txt".format(ip)
	outputFile = "preUnique.txt"
	print(rulesFile)
	os.system("hashcat --stdout {} -r {} > {}".format(passFile, rulesFile, outputFile))
		
	#os.system("rm -f {}".format(rulesFile))

	
	with open(outputFile, "r") as allWords, open(path, "a") as wu:
		unique = []
		a = allWords.readlines()
		for line in a:
			if line not in unique:
				unique.append(line)
			else:
				continue
		for u in unique:
			wu.write(u.strip()+"\n")


# count number of passwords generated
def countPass(path):
	
	try:
		with open(path) as fr:
			counter = 0
			f = fr.readlines()
			for line in f:
				counter += 1
			return counter
	except:
		print("\n*** Error occurred: Password list not generated ***")
		print("\n*** You might need to increase your VM's RAM (at least 4GB suggested) ***")


# call functions
path = preCheck()
crawl(ip, port)
extend(ip)
fuzz(ip, path)
count = countPass(path)

#os.system("rm -f cewlPass.txt prePass_{}.txt preUnique.txt".format(ip))

if count > 0:
	print("\n-+- {} tailored passwords generated -+-".format(count))
	print("\n#################################")
	print("### password list saved to {} ###".format(path))
	print("#################################")
