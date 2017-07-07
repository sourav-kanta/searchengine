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
    while r.status_code == 200:
        r = requests.get('http://swapi.co/api/people/' + str(i))

        es.index(index='sw', doc_type='people', id=i, body=json.loads(r.content))

        result = db.stars.insert_one(json.loads(r.content))
        i = i + 1
    # except requests.exceptions.ConnectionError:
    # sleep(10)
    # e = sys.last_value
    # print(e.args[0].reason)



    print(i)

    print(es.get(index='sw', doc_type='people', id=5))
    print(es.search(index="sw", body={"query": {"match": {'name': 'Darth Vader'}}}))

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