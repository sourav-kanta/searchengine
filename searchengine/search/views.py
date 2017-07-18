from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import requests
from time import sleep

from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
from pymongo import MongoClient


# Create your views here.
def search():
    client = MongoClient()
    db = client.test
    from datetime import datetime
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    import json
    i = 1
    r = requests.get('http://localhost:9200')


    print("$$$$$$$$$$**********$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    #print(es.get(index='sw', doc_type='people', id=5))
    print(es.search(index="sw", body={"query": {"match": {'data': 'Foundation'}}}))

    # result = db.star&ships.insert_one()

@csrf_exempt
def search_page(request):
	search()
	return HttpResponse("Exhausted links.")


def start(request):
     return render(
        request,
        'Search/startindex.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
        }
    )