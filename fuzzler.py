#!/usr/bin/python3
# author: suffs811
# Copyright (c) 2023 suffs811
# https://github.com/suffs811/fuzzler.git
# read the README.md file for more details; software distributed under MIT license; for personal, legal use only.
#
# usage: python3 fuzzler.py -t <target_ip>
#
# note <> you may have to specify the specific version of python3 you are running (i.e. python3.6 || python3.9 etc.)


import os
# install nltk library
os.system("python3 -m pip install nltk || echo '*** error installing nltk; please install manually before proceeding ***'")
import argparse
from datetime import datetime
from nltk.corpus import wordnet as wn


# set up arguments for script
parser = argparse.ArgumentParser(description="script for creating tailored password lists using Machine Learning")
parser.add_argument("-t", "--targetip", help="specify target ip to crawl")
parser.add_argument("-p", "--port", help="specify target port (default=80)")
args = parser.parse_args()
ip = args.targetip
port = args.port
nFile = ""


# ensure necessary tools are downloaded and check if fuzzed pswd file already exists
def preCheck():

	# download cewl and hashcat
	print("\n### downloading necessary tools and libraries ###\n")
	os.system("sudo apt install cewl")
	os.system("sudo apt install hashcat")

	# check for fuzzes.txt; if exists, return new unique file name using datetime
	if os.path.exists("fuzzes.txt"):
		answer = input("\n *** fuzzes.txt already exists, do you want to replace it? (y/n) ***")
		if answer.lower() == "y":
			os.system("rm -f fuzzes.txt")
		elif answer.lower() == "n":
			# get current time to make unique file name
			now = datetime.now()
			time = now.strftime("%H%M%S")
			nFile = "fuzzes_{}.txt".format(time)
		else:
			print("\n*** please specify either 'y' or 'n' ***")
			preCheck()
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
						fp.append(nnline)
					else:
						continue
			else:
				continue


# use NLP to add similar words to the list
def extend():
	with open("cewlPass.txt") as fp:
		f = fp.readlines()
		for word in f:
			synset = wn.synsets(word)[0]
			syns = wn.synset(synset).lemma_names()
			for syn in syns:
				fp.append(syn)


# fuzz the list of passwords
def fuzz(path):
	rules = [':', 'l', 'u', 'c', 'C', 't', 'r', 'd', '$?d', '$?d$?d', '$?d$?d$?d', '$?d$?d$?d$?d', '^?d', '^?d^?d', '^?d^?d^?d', '^?d^?d^?d^?d', 'sa@', 'sa4', 'se3', 'sl1', 'sa@ se3 sl1', 'sa4 se3 sl1']
	rulesFile = ""

	# check if the hascat rules file exists; if exists, create unique file name
	if os.path.exists("fuzzRules.txt"):
		now = datetime.now()
		time = now.strftime("%H%M%S")
		rulesFile = "fuzzRules_{}.txt".format(time)
	else:
		rulesFile = "fuzzRules.txt"
	with open(rulesFile) as r:
		for rule in rules:
			r.append(rule)

		passFile = "cewlPass.txt"
		os.system("hashcat --force {} -r {} > {}".format(passFile, rulesFile, path))


# count number of passwords generated
def countPass(path):

	with open("{}".path) as fr:
		f = fr.readlines()
		counter = 0
		for line in f:
			counter += 1

		return counter


# call functions
path = preCheck()
crawl(ip, port)
extend()
fuzz(path)
count = countPass(path)

print("\n-+- {} tailored passwords generated -+-".format(count))
print("\n### password list saved to {} ###".format(path))
