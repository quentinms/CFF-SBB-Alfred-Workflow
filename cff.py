#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
import urllib2
import urllib
import time
import sys



def main():

	train_icons = {'IR' : 'IR.png', 'TGV' : 'TGV.png', 'M' : 'metro.jpg'}

	args = sys.argv


	if len(args) == 1:
		f = open('config.txt', 'r')
		tmp = f.readline()[:-1]
		args = [x.strip() for x in tmp.split('_')]
		print args
	else:
		args = args[1:]

	args[0] = urllib.quote(unicode(args[0], errors='ignore'), '')
	args[1] = urllib.quote(unicode(args[1], errors='ignore'), '')

	url = 'http://transport.opendata.ch/v1/connections?from=%s&to=%s' % (args[0], args[1])
	res = urllib2.urlopen(url)
	timetables = json.load(res)

	results = '<?xml version="1.0"?><items>'

	for journey in timetables['connections']:
		departure = time.strptime(journey['from']['departure'], '%Y-%m-%dT%H:%M:%S+0200')
		duration = time.strptime(journey['duration'], '00d%H:%M:%S')
		
		train_type = journey['products'][0]
		platform = journey['from']['platform']

		nb_transfer = journey['transfers']


		title ="<title>"+('0'+str(departure.tm_hour))[-2:]+":"+('0'+str(departure.tm_min))[-2:]+"</title>"
		subtitle="<subtitle>%s, Platform %s, %s:%s, %s transfers</subtitle>" % (train_type, platform, ('0'+str(duration.tm_hour))[-2:], ('0'+str(duration.tm_min))[-2:], nb_transfer)

		if train_type in train_icons:
			icon = "<icon>"+train_icons[train_type]+"</icon>"
		else:
			icon = "<icon>icon.png</icon>"
		
		item = "<item>"+title+subtitle+icon+"</item>"
		results += item

	change_default_item = "<item arg='%s _ %s'><title>Set as default travel</title><icon></icon></item>" % (args[0], args[1])

	results+=change_default_item+"</items>"

	print results

main()