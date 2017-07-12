# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.contrib.auth.models import User
from pymongo import MongoClient
import requests
import urllib2
import time,json
import re
import threading
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from crawler.models import RegistrationForm
from elasticsearch import Elasticsearch
from parser1 import parse
url_pool = [("https://en.wikipedia.org/wiki/Main_Page",5),("http://www.michigan.gov",3),("https://www.nrcan.gc.ca/",3),("http://dnr.maryland.gov/",3),("https://resourcegovernance.org/",3),("https://naturalresources.virginia.gov/",3),("https://naturalresources.wales/?lang=en",3)]
client = MongoClient()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
db = client.test
collection = db.docs
class AllThreads(threading.Thread):
	
	print('crawl')
	def __init__(self,url,period):
		period = period
		#print('crawl')
		threading.Thread.__init__(self)
		self.url = url
	def crawl(self,url_pool,period):
		#print('crawl')
		#print(self.url)
		if(urllib2.urlopen(self.url)):
			page = urllib2.urlopen(self.url)
			soup = BeautifulSoup(page)
			all_links = soup.find_all("a") 
			for link in all_links:
				#print(link)
				new_link = link.get("href")
				if new_link not in url_pool:
					if(re.findall('^/',str(new_link))):
						try:
							url_pool.append((self.url + str(new_link),1))
							id = datetime.now()
							try:
								data = parse(self.url + str(new_link))
							except:
								#print "error"
								data = parse(self.url + str(new_link))
								data = "Nothing Found"
							db.docs.insert_one({"id": id,"data":data,"link":self.url + str(new_link)})
							dict1 = {"link":self.url + str(new_link),"data":data}
							data = json.dumps(dict1, ensure_ascii=False)
							es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
							#with open("doc.json", "w") as f:
    								#json.dump(list(collection.find()), f)
						except urllib2.HTTPError as e:

							'''
							url_pool.append((self.url + str(new_link),1))
							print(self.url + str(new_link))
							id = datetime.now()
							try:
								data = parse(self.url + str(new_link))
							except:
								#print "error"
								data = parse(self.url + str(new_link))
								data = "Nothing Found"
						
							print("error while encoding1")	
							db.docs.insert_one({"id": id,"data":data,"link":self.url + str(new_link)})
							dict1 = {"link":self.url + str(new_link),"data":data}
							data = json.dumps(dict1, ensure_ascii=False)
							es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
							#with open("doc.json", "w") as f:
    								#json.dump(list(collection.find()), f)
    						'''
    					
    							error_message = e.read()
    							print "error part1",error_message

					else:
						try:
							url_pool.append((new_link,1))
							id = datetime.now()
							try:
								#data = urllib2.urlopen(new_link)
								data = parse(str(new_link))
							except:
								#print "error"
								data = "Nothing Found"
							db.docs.insert_one({"id": id,"data":data,"link":str(new_link)})
							dict1 = {"link":str(new_link),"data":data}
							data = json.dumps(dict1, ensure_ascii=False)
							es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
							#with open("doc.json", "w") as f:
    								#json.dump(list(db.docs.find()), f)
						except urllib2.HTTPError as e:
							error_message = e.read()
    							print "error part2",error_message
			#with open("doc.json", "w") as f:
    				#json.dump(list(docs.find()), f)
			print(url_pool)	 
		 	#print(db.docs)
		 	time.sleep(period)
		 	self.crawl(url_pool,period)


def get_the_links(url_pool):
	k = 0
	for i in url_pool:
		if i[0] is not None:
			background = AllThreads(i[0],i[1])
			background.start()
			#print(i)
			background.crawl(url_pool,i[1])
			background.join()
			#print(url_pool)
			#print(len(url_pool))
			#print(i)
			#print k
			k = k + 1
		else:
			break
	return url_pool
def crawldata():
	global url_pool
	print "Crawling"
	url_pool = get_the_links(url_pool)
	print url_pool

def crawldata2():
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
	def crawl3(links,pid):
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
	#crawldata()
	global url_pool
	for index in es.indices.get('*'):
  		print index
	#print(es.search(index='sw'))
	url_pool = get_the_links(url_pool)
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

def signup(request):
	if request.method == 'POST':
	    form = RegistrationForm(request.POST)
	    if form.is_valid():
	        user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
	        return HttpResponseRedirect('/login')
	form = RegistrationForm()
	variables = RequestContext(request, {'form': form,
	        'title':'Demo Content',
	        'year': datetime.now().year,
	    })
	return render_to_response('crawler/signup.html',variables)

def login(request):
	return render(
        request,
        'crawler/login.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
        }
    )

def home(request):
	template = loader.get_template('crawler/home.html')
	variables = Context({ 'user': request.user ,
            'title':'Demo Content',
            'year': datetime.now().year,
        })
	output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')