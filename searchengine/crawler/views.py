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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
url_pool = [("http://www.michigan.gov",3),("https://www.nrcan.gc.ca/",3),("http://dnr.maryland.gov/",3),("https://resourcegovernance.org/",3),("https://naturalresources.virginia.gov/",3),("https://naturalresources.wales/?lang=en",3)]
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
								data,header = parse(self.url + str(new_link))
								dict1 = {"link":self.url + str(new_link),"data":data,"header":header}
								data = json.dumps(dict1, ensure_ascii=False)
								if not header=="none":
									es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
							except:
								#print "error"
								data = parse(self.url + str(new_link))
								data = "Nothing Found"
						
						except urllib2.HTTPError as e:

							
    							error_message = e.read()
    							print "error part1",error_message

					else:
						try:
							url_pool.append((new_link,1))
							id = datetime.now()
							try:
								#data = urllib2.urlopen(new_link)
								data,header = parse(str(new_link))
								dict1 = {"link":str(new_link),"data":data,"header":header}
								data = json.dumps(dict1, ensure_ascii=False)
								if not header=="none":
									es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
							except:
								#print "error"
								data = "Nothing Found"
							
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



@csrf_exempt
def crawl_page(request):
	global url_pool
	#for index in es.indices.get('*'):
  	#	print index
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
	    else:
	    	variables = RequestContext(request, {
				'form': form,
				'title':'Demo Content',
				'year': datetime.now().year,
	    	})
	    	return render_to_response('crawler/signup.html',variables)
	form = RegistrationForm()
	variables = RequestContext(request, {
		    'form': form,
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
	if not request.GET.get('query'):
		template = loader.get_template('crawler/home.html')
		variables = Context({ 'user': request.user ,
	            'title':'Demo Content',
	            'year': datetime.now().year,
	        })
		output = template.render(variables)
	else :
		result = es.search(index="sw", body={"query": {"match": {'data': request.GET.get('query')}}})
		#print result['hits']['hits'][0]["_source"]
		res=[]
		for rows in result['hits']['hits']:
			f_res={}
			f_res["link"]=rows["_source"]["link"]
			if len(rows["_source"]["data"]) >= 500:
				f_res["data"]=rows["_source"]["data"][:500]+"..."
			else:
				f_res["data"]=rows["_source"]["data"]
			f_res["header"]=rows["_source"]["header"]
			res.append(f_res)
		if len(res)==0:
			f_res={}
			f_res["link"]=""
			f_res["data"]="No results were found for "+request.GET.get('query')+""
			f_res["header"]=""
			res.append(f_res)
		template = loader.get_template('crawler/search.html')
		variables = Context({ 'user': request.user ,
	            'title':'Demo Content',
	            'year': datetime.now().year,
	            'results' : res
	        })
		output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')