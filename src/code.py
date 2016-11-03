import re

counter = 0
with open('collection.txt') as fp:
	f = open('docum.json','w')
	for line in fp:
		counter+=1
		elements = re.split(r'\t+', line)
		f.write('{"index":{"_index":"semere", "_type":"products", "_id": "'+ str(counter) +'"}}\n') # python will convert \n to os.linesep
		allwords = elements[1].rstrip('\n')
		f.write('{ "pid":"'+ elements[0]+'", "pdesc":"'+ allwords+'"}\n') # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call it
