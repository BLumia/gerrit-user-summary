from pyquery import PyQuery as H
import urllib.request as request
import urllib.parse as parse
import collections
import getopt, sys
import datetime
import argparse
import json

baseUrl = "https://cr.deepin.io/"
accountId = "BLumia"
summaryCount = 20

try:
	opts, args = getopt.getopt(sys.argv[1:], "u:a:c:ho:v", ["url", "account", "count", "help", "output="])
except getopt.GetoptError as err:
	# print help information and exit:
	print(str(err))  # will print something like "option -a not recognized"
	print("Argument not correct")
	sys.exit(2)

for o, a in opts:
	if o == "-v":
		verbose = True
	elif o in ("-u", "--url"):
		baseUrl = a
	elif o in ("-a", "--account"):
		accountId = a
	elif o in ("-c", "--count"):
		summaryCount = a
	elif o in ("-h", "--help"):
		usage()
		sys.exit()
	elif o in ("-o", "--output"):
		output = a
	else:
		assert False, "unhandled option"

urlArguments = parse.urlencode({'q': "owner:" + accountId, 'n': summaryCount})
requestUrl = baseUrl + "changes/?" + urlArguments

# print("Loading summary from `" + requestUrl + "`\n")
# exit("asd")
print("Loading summary from `" + baseUrl + "`")
print("Account: `" + accountId + "`")
print("Request summary count: " + summaryCount + "\n")

summaryDict = collections.OrderedDict()

with request.urlopen(requestUrl) as url:
	rawData = url.read().decode()
	if rawData[:3] != ')]}':
		exit("wtf")
	data = json.loads(rawData[4:])
	for commit in data:
		commitUpdateTimeStr = None
		if 'submitted' in commit.keys():
			commitUpdateTimeStr = commit['submitted']
		else:
			commitUpdateTimeStr = commit['created']
		commitUpdateTime = datetime.datetime.strptime(commitUpdateTimeStr[:-3], "%Y-%m-%d %H:%M:%S.%f")
		summaryDict.setdefault(commitUpdateTime.strftime("%Y-%m-%d"), []).append(commit['subject'])

for when, oneDay in summaryDict.items():
	print(when + ":")
	for commit in oneDay:
		print(" * " + commit)
	print("")