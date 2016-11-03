from __future__ import print_function
import os
import requests
import json
import re
import sys



def search(uri,term):
    """Simple Elasticsearch Query"""
    query = json.dumps({
    	"sort":["_score"],
    	"size": 100,
        "query": {
            "match": {
                "pdesc": {
                    "query":term
                }
            }
        }
    })
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return results

def format_results(terms,results,log,nameofrun):
    """Print results nicely:
    doc_id) content
    """
    data = [doc for doc in results['hits']['hits']]
    i=0
    for doc in data:
    	i+=1
    	print("%s\tQ0\t%s\t%s\t%s\t%s" % (terms[0], doc['_source']['pid'],i ,doc['_score'],nameofrun),file=log)

if __name__ == '__main__':
    
    #python run.py nameofrun

    uri_search = 'http://localhost:9200/test/_search'
    log = open("../runs/2to3grams3.run", "w")
    print("Qid\tIter\tDocid\tRank\tSim\tRunid",file=log)

    with open("500queries.txt", "r") as ins:
    	for line in ins:
        	terms = re.split(r'\t+', line.rstrip('\n'))
        	results = search(uri_search, terms[1])
        	format_results(terms,results,log,sys.argv[1])