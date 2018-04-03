import sys
import ast


def create_posting_list(vocab_map_file_path, doc_file_path):
	vocab_map = {}
	total_doc = set()
	doc_vocab = {}
	posting_list = {}
	doc_id=1
	for line in open(vocab_map_file_path,'r',encoding = 'UTF-8'):
		vocab_map[int(line.split()[0])] = line.split()[2]
	for line in open(doc_file_path,'r',encoding = 'UTF-8'):
		list_line=ast.literal_eval(line)
		doc_vocab[doc_id] = list_line
		total_doc.add(doc_id)
		for token_id in list_line:
			if vocab_map[token_id] in posting_list:
				posting_list[vocab_map[token_id]].add(doc_id)
			else:
				l = set()
				l.add(doc_id)
				posting_list[vocab_map[token_id]] = l 
		doc_id+=1
	return posting_list, vocab_map,doc_vocab,total_doc

def intersection(posting_list_1,posting_list_2):
	list_1 = sorted(posting_list_1)
	list_2 = sorted(posting_list_2)
	i=0
	j=0
	result = set()
	while (i<len(list_1)) and (j<len(list_2)):
		if list_1[i] == list_2[j]:
			result.add(list_1[i])
			i+=1
			j+=1
		elif (list_1[i]<list_2[j]):
			i+=1
		else:
			j+=1
	return result
def evaluateANDQuery(a,b):
	return intersection(a,b)

def union(posting_list_1, posting_list_2):
	list_1 = sorted(posting_list_1)
	list_2 = sorted(posting_list_2)
	i=0
	j=0
	result = set()
	while (i<len(list_1)) and (j<len(list_2)):
		if list_1[i] == list_2[j]:
			result.add(list_1[i])
			i+=1
			j+=1
		elif (list_1[i]<list_2[j]):
			result.add(list_1[i])
			i+=1
		else:
			result.add(list_2[j])
			j+=1
	if i < len(list_1):
		while i<len(list_1):
			result.add(list_1[i])
			i+=1
	if j<len(list_2):
		while j<len(list_2):
			result.add(list_2[j])
			j+=1
	return result

def evaluateORQuery(a,b):
	return union(a,b)

def not_(p):
	result = set()
	for x in total_doc_id:
		if x not in p:
			result.add(x)
	return result

def evaluateAND_NOTQuery(a,b):
	return intersection(a,not_(b))

			
def main(query_type,query_string,output_file_path):
	return query_type,query_string,output_file_path

if __name__ == "__main__":#reading data from cmd line
	if len(sys.argv) > 2:
		query_type,query_list,output_file_path = main(sys.argv[1],sys.argv[2:-1],sys.argv[-1])

query_string = ' '.join(query_list)
orig_stdout = sys.stdout #output in the file
fout = open(output_file_path, 'w')
sys.stdout = fout
lower_case_query = ''
word_a = None
for i in query_list:
	if i not in ['(',')','AND','OR','NOT']:
		if word_a != None:
			word_b = i.lower()
			lower_case_query=lower_case_query+' '+word_b
		else:
			word_a = i.lower()
			lower_case_query=lower_case_query+' '+word_a
	else:
		lower_case_query=lower_case_query+' '+i
vocab_map_file_path = 'proj_2/vocab_map.txt'
doc_file_path = 'proj_2/docs.txt'

posting_list, vocab_map,doc_vocab,total_doc_id = create_posting_list(vocab_map_file_path,doc_file_path)

if query_type == 'PLIST':
	print(lower_case_query.strip(),'->',sorted(posting_list[lower_case_query]))
elif (query_type == 'AND'):
	print(lower_case_query.strip(),'->',sorted(evaluateANDQuery(posting_list[word_a],posting_list[word_b])))
elif (query_type == 'OR'):
	print(lower_case_query.strip(),'->',sorted(evaluateORQuery(posting_list[word_a],posting_list[word_b])))
else:
	print(lower_case_query.strip(),'->',sorted(evaluateAND_NOTQuery(posting_list[word_a],posting_list[word_b])))


