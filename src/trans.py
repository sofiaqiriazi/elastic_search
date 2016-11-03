import re

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
	for i in allwords:
		if ( not(i.isdigit()) and not(i.isalpha()) and len(code)<len(i)):
			code = i
	return code

counter = 0
with open('collection.txt') as fp:
	f = open('1docum.json','w')
	for line in fp:
		counter+=1
		elements = re.split(r'\t+', line)
		str2 = elements[1].rstrip('\n')
		allwords = (str2).split(' ')
		
		code = find_code(allwords)
		str1 = ' '.join(allwords)
		dimensions = find_dimensions(str1)

		f.write('{"index":{"_index":"sofia", "_type":"products", "_id": "'+ str(counter) +'"}}\n') # python will convert \n to os.linesep
		f.write('{ "pid":"'+ elements[0]+'", "pcode":"'+ code+'", "pdim":"'+ dimensions +'","pdesc":"'+ str1 +'"}\n') # python will convert \n to os.linesep
f.close() # you can omit in most cases as the destructor will call it
