from __future__ import print_function, division
import os
import requests
import json
import re
import sys

def get_count(new_dict,a):
    ttl = 0
    for i in new_dict[a]:
        if new_dict[a][i] == '1':
            ttl+=1

    return ttl

def get_sum_precision(a):
    indx = 0
    ttl = 0
    precision = 0
    for i in a:
        indx+=1
        if i == 1:
            ttl+=1
            precision += ttl/indx

    return precision


def get_map(new_dict):
    maps = dict()
    for i in new_dict:
        total = 0
        for j in new_dict[i]:
            if new_dict[i][j] == '1':
                total +=1;
        map_value = total/len(new_dict[i])
        maps[i] = map_value

    return maps
def calc_p(a):
    p_1 = results[0]/1
    p_5 = sum(results[0:5])/5
    p_30 = sum(results[0:30])/30
    p_1000 = sum(results[0:1000])/1000
    return {"p_1":p_1, "p_5":p_5,"p_30":p_30,"p_1000":p_1000}

def calc_s(a):
    s_1 = 0
    if a[0] == 1:
        s_1 = 1

    s_5 = 0
    for i in a[0:5]:
        if i==1:
            s_5 = 1

    s_30 = 0
    for i in a[0:30]:
        if i==1:
            s_30 = 1

    s_1000 = 0
    for i in a[0:100]:
        if i==1:
            s_1000 = 1

    return {"s_1":s_1, "s_5":s_5,"s_30":s_30,"s_1000":s_1000}

def calc_ranks(a):
    try:
        return 1/(a.index(1)+1)
    except ValueError:
        return 0

def calc_binary(a,b):

    binary = list()
    for key, value in sorted(a.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        if key in b:
            binary.append(int(b[key]))
        else:
            binary.append(0)
    return binary

if __name__ == '__main__':


    with open("testrun.txt", "r") as ins:
        run_dict = {}
        for line in ins:
            terms = re.split(r'\t+', line.rstrip('\n'))
            if terms[0] in run_dict:
                run_dict[terms[0]][terms[2]] = float(terms[4])
            else:
                run_dict[terms[0]] = {}
                run_dict[terms[0]][terms[2]] = float(terms[4])

    with open("testqrels.txt", "r") as ins:
        new_dict = {}
    	for line in ins:
            terms = re.split(r'\t+', line.rstrip('\n'))
            indexes = terms[0].split()
            if indexes[0] in new_dict:
                new_dict[indexes[0]][indexes[2]] = indexes[3]
            else:
                new_dict[indexes[0]] = {}
                new_dict[indexes[0]][indexes[2]] = indexes[3]


    log = open("scriptresults.txt", "w")
    avg_map = 0
    avg_p1 = 0
    avg_p5 = 0
    avg_p30 = 0
    avg_p1000 = 0
    avg_s1 = 0
    avg_s5 = 0
    avg_s30 = 0
    avg_s1000 = 0
    avg_recip_rank = 0

    for key in sorted(run_dict.iterkeys()):
        results = calc_binary(run_dict[key],new_dict[key])
        ps = calc_p(results)
        ss = calc_s(results)
        recip_ranks = calc_ranks(results)
        relev_documents = get_count(new_dict,key)
        precision = get_sum_precision(results)
        m_a_p = round(precision/relev_documents,4)
        avg_map += m_a_p
        avg_p1 += ps["p_1"]
        avg_p5 += ps["p_5"]
        avg_p30 += ps["p_30"]
        avg_p1000 += ps["p_1000"]
        avg_s1 += ss["s_1"]
        avg_s5 += ss["s_5"]
        avg_s30 += ss["s_30"]
        avg_s1000 += ss["s_1000"]
        avg_recip_rank += recip_ranks
        print("map\t%s\t%.4f" % (key,m_a_p), file=log)
        print("P1\t%s\t%s" % (key,str(ps["p_1"])), file=log)
        print("P5\t%s\t%f" % (key,ps["p_5"]), file=log)
        print("P30\t%s\t%f" % (key,ps["p_30"]), file=log)
        print("P1000\t%s\t%f" % (key,ps["p_1000"]), file=log)
        print("recip_rank\t%s\t%f" % (key,recip_ranks), file=log)
        print("S1\t%s\t%f" % (key,ss["s_1"]), file=log)
        print("S5\t%s\t%f" % (key,ss["s_5"]), file=log)
        print("S30\t%s\t%f" % (key,ss["s_30"]), file=log)
        print("S1000\t%s\t%f" % (key,ss["s_1000"]), file=log)
    length = len(run_dict)
    print("map\tall\t%.4f" % (avg_map/length), file=log)
    print("P1\tall\t%f" % (avg_p1/length), file=log)
    print("P5\tall\t%f" % (avg_p5/length), file=log)
    print("P30\tall\t%f" % (avg_p30), file=log)
    print("P1000\tall\t%f" % (avg_p30), file=log)
    print("recip_rank\tall\t%f" % (avg_recip_rank/length), file=log)
    print("S1\tall\t%f" % (avg_s1/length), file=log)
    print("S5\tall\t%f" % (avg_s5/length), file=log)
    print("S30\tall\t%f" % (avg_s30/length), file=log)
    print("S1000\tall\t%f" % (avg_s1000/length), file=log)
    