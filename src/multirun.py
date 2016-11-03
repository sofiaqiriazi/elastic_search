from __future__ import print_function
import os
import requests
import json
import re
import sys


def find_dimensions(a):
    #regular expressions
    strs = []
    strs.append('x'.join(re.findall(r'\w+\s*mm\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*mt\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*MM\b',a)))
    strs.append('x'.join(re.findall(r'\b\d+x*\d+\b',a)))
    strs.append('x'.join(re.findall(r'\b\d+X*\d+\b',a)))
    strs.append('x'.join(re.findall(r'\b\d+\s*mm\b',a)))
    strs.append('x'.join(re.findall(r'\b\d+\s*MM\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*kg\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*KG\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*ml\b',a)))
    strs.append('x'.join(re.findall(r'\w+\s*ML\b',a)))  
    strs.append('x'.join(re.findall(r'\w+\s*gr\b',a)))  
    strs.append('x'.join(re.findall(r'\w+\s*GR\b',a)))  
    return ' '.join(strs)
     
def find_code(a):
    code = " "
    for i in a:
        if ( not(i.isdigit()) and not(i.isalpha()) and len(code)<len(i)):
            code = i
    return code

def search(uri,code,dim,terms):
    """Simple Elasticsearch Query"""
    query = json.dumps({
        "sort":["_score"],
        "size": 100,
        "query": {
            "bool": {
                "should": [
                {
                    "match": {
                    "pdesc": {
                        "query": terms,
                        "boost": 3
                    }
                }
            },
            {
                "match": {
                "pcode": {
                    "query": code,
                    "boost": 1
                }
            }
            },
            {
                "match": {
                "pdim": {
                    "query": dim,
                    "boost": 1
                }
            }
            }
        ]
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
        if i<100:
    	   i+=1
    	   print("%s\tQ0\t%s\t%s\t%s\t%s" % (terms[0], doc['_source']['pid'],i ,doc['_score'],nameofrun),file=log)

if __name__ == '__main__':
    
    #python run.py nameofrun

    uri_search = 'http://localhost:9200/sofia/_search'
    log = open("multi3to20.run", "w")
    print("Qid\tIter\tDocid\tRank\tSim\tRunid",file=log)

    with open("500queries.txt", "r") as ins:
    	for line in ins:
            terms = re.split(r'\t+', line.rstrip('\n'))
            print (terms)
            code = find_code(terms[1].split(' '))
            print (code)
            dim = find_dimensions(terms[1])
            print (dim)
            results = search(uri_search, code, dim, terms[1])
            format_results(terms,results,log,sys.argv[1])