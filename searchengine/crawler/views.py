# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render

from pymongo import MongoClient
import requests
import urllib2
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def crawldata():
	url = "http://stackoverflow.com"
	page = urllib2.urlopen(url)
	#r = requests.get('http://swapi.co/api/people/1')
	soup = BeautifulSoup(page)
	i = 1
	client = MongoClient()
	db = client.test
	print(soup)
	id1 = datetime.now()
	r = requests.get('http://swapi.co/api/people/1')
	all_links = soup.find_all("a")
	links = []
	pids = []
	for link in all_links:
		print(link.get("href"))
		id = datetime.now()
		try:
			db.testdb.insert_one({"id": id,"pid": id1 ,"link":str(link)})
		except :
			print("error while encoding")
		pids.append(id)
		links.append(link)


	#this function scarps all the links in a web page and then does the same thing for all the links it gives an id to each link and a pid to the parent link from which it was scraped.
	def crawl(links,pid):
		for link,pid in zip(links,pids):
			links2 = []
			pid2 = []
			page = urllib2.urlopen(url)
			soup = BeautifulSoup(page)
			all_links = soup.find_all("a")
			for link in all_links:
				id = datetime.now()
				pid2.append(id)
				try:
					db.testdb.insert_one({"id": id,"pid": pid ,"link":str(link)})
				except:
					print("error while encoding")
				print(link.get("href"))
				links2.append(link)
			crawl(links2,pid2)
	crawl(links,pids)




@csrf_exempt
def crawl_page(request):
	crawldata()
	return HttpResponse("Exhausted links.")

def start(request):
	return render(
        request,
        'crawler/startindex.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
        }
    )