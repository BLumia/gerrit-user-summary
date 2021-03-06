# from pyquery import PyQuery as H
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
summaryStart = 0
summaryDict = collections.OrderedDict()


def usage():
	print('''
Gerrit User Summary - Get a summary list group by day via gerrit API

Example:
    {0} -u https://cr.deepin.io/ -a BLumia -c 10

Usage:
    -h          --help            : Display this help
    -u <url>    --url <url>       : Gerrit API Url
    -a <id>     --account <id>    : Gerrit account id
    -c <count>  --count	<count>   : Commit count fetched from gerrit
    -s <count>  --start	<count>   : Commit start at number <count>
    -o <path>   --output= <path>  : Not implemented...
'''.format(sys.argv[0]))


def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "u:a:c:s:ho:e", ["url", "account", "count", "start", "help", "empty", "output="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err))  # will print something like "option -a not recognized"
		print("Argument not correct")
		print("Try `{0} -h` to see usage.".format(sys.argv[0]))
		sys.exit(2)

	global baseUrl
	global accountId
	global summaryCount
	global summaryStart

	for o, a in opts:
		if o in ("-u", "--url"):
			baseUrl = a
		elif o in ("-a", "--account"):
			accountId = a
		elif o in ("-s", "--start"):
			if a.isdigit():
				summaryStart = int(a)
			else:
				assert False, "argument not valid"
		elif o in ("-c", "--count"):
			if a.isdigit():
				summaryCount = int(a)
			else:
				assert False, "argument not valid"
		elif o in ("-h", "--help"):
			usage()
			exit()
		elif o in ("-o", "--output"):
			output = a
		elif o in ("-e", "--empty"):
			print("Empty empty empty empty...")
			print("Lazy guy!")
		else:
			assert False, "unhandled option"
			
	if len(opts) == 0:
		usage()
		exit()

	if baseUrl[-1] != '/':
		baseUrl = baseUrl + '/'
	argumentDirectory = {'q': "owner:" + accountId, 'n': summaryCount}
	if summaryStart > 0:
		argumentDirectory['S'] = summaryStart
	urlArguments = parse.urlencode(argumentDirectory)
	requestUrl = baseUrl + "changes/?" + urlArguments

	# print("Loading summary from `" + requestUrl + "`\n")
	# exit("asd")
	print("Loading summary from `" + baseUrl + "`")
	print("Account: `" + accountId + "`")
	if summaryCount > 0:
		print("Request summary start from: " + str(summaryStart))
	print("Request summary count: " + str(summaryCount) + "\n")

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


if __name__ == "__main__":
	main()
