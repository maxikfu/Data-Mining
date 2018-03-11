
from itertools import product
import difflib
#from difflib_data import *
from Data_PreProcessing import *
import time
import sys
def my_product(l): #generate subseq of the seq
	result = set()
	n=len(l)
	result.add(tuple(l[:-1]))
	for i in range(1,n-1):
		result.add(tuple(l[:i]+l[i+1:]))
	result.add(tuple(l[1:]))
	return result

class AprioriAlgorithm:
	def __init__(self):
		pass

	def apriori_algorithm(self,data,minSup,k):
		fPrev=data.unigram_count
		iterCount=1
		needToDelete=[]
		[needToDelete.append(key) for key, value in fPrev.items() if value<minSup]
		for key in needToDelete: #deleting values what count less then minSupport
			del fPrev[key]
		#now we need to produce next generation (candiadates)
		result = {}
		if (iterCount >= k) and (not not fPrev):
			result.update(fPrev)
		#print('creating new generation')
		totalNumberOFelem = len(data.transactionDB)
		elemChecked = 0
		#print('last f length', len(fPrev))
		while fPrev: #while dictionary is not empty
			newF = self.candidateGen(data,fPrev,minSup)
			iterCount+=1
			#print('New generation created ', round(time.time() - start_time,2))
			start = time.time()
			if (iterCount >= k) and (newF):
				result.update(newF)
			fPrev = newF
			#print('Iteration = ',iterCount,' F length = ',len(fPrev),' Length of result = ', len(result))
			
		return result
	def itemSetCount(self,data,itemSet): #counting number of occurances for itemset
		resultCount=0
		difference = None
		for subKey in itemSet:
			if difference is None:
				difference = data.transactionDB[subKey]
			difference = difference & data.transactionDB[subKey]
		resultCount+=len(difference)
		return resultCount


	def candidateGen(self,data,f,minSupport):
		candidates = {}
		checked = set()
		listF=[]
		[listF.append(key) for key in f]
		sorted(listF)
		for i in range(0,len(listF)-1):
			for j in range(i+1,len(listF)):
				if (listF[i][:-1]==listF[j][:-1]) and (listF[i][-1]!=listF[j][-1]):
					newCandidate = tuple(sorted(listF[i]+tuple([listF[j][-1]])))
					#checking if k-1 was in previouse 
					if (len(newCandidate)>2) and all(subseq in f for subseq in my_product(newCandidate)):
						#newCandidate = tuple(sorted(newCandidate))
						newCandidateCount = self.itemSetCount(data,newCandidate)
						if newCandidateCount >= minSupport: 
							candidates[newCandidate]= newCandidateCount
					elif len(newCandidate) ==2:
						newCandidateCount = self.itemSetCount(data,newCandidate)
						if newCandidateCount >= minSupport: 
							candidates[newCandidate]= newCandidateCount#checking relay on lexicographical order
		return candidates



#function to compare files						
def cmpFiles(experimentResultFile,trueResultFile):
	experimentResult = []
	result = True
	for line in open(experimentResultFile,'r'):
		lineSet=set()
		for ids in line.split():
			lineSet.add(ids)
		experimentResult.append(lineSet)
	for line in open(trueResultFile,'r'):
		lineSet=set()
		for ids in line.split():
			lineSet.add(ids)
		if lineSet not in experimentResult:
			#print('False for ')
			result = False
	if result:
		print('Files are identical')
	else:
		print('ERROR! Files are NOT!!!!!!! identical!') 

def main(minSupport,k_itemset_number,inputFilePath,outputFilePath):
	return minSupport,k_itemset_number,inputFilePath,outputFilePath


if __name__ == "__main__":
	if len(sys.argv) > 3:
		minSupport,k_itemset_number,inputFilePath,outputFilePath = main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])



data = Data_PreProcessing(inputFilePath)
apriori = AprioriAlgorithm()

start_time = time.time()
raw_result = apriori.apriori_algorithm(data,int(minSupport),int(k_itemset_number))
#convert into desired output format
outputList = []
for key,value in raw_result.items():
	output_line=[]
	for k in key:
		[output_line.append(key) for key,value in data.dictionary.items() if value == k]
	output_line=sorted(output_line)
	output_line.append('('+str(value)+')')
	outputList.append(output_line)
#print(raw_result)
orig_stdout = sys.stdout
fout = open(outputFilePath, 'w')
sys.stdout = fout
for l in outputList:
	print(' '.join(l))
runningTime= time.time() - start_time
fout.close()
#sys.stdout = orig_stdout
#print("Running time=",runningTime)
#scmpFiles(outputFilePath,'data/out_s='+minSupport+'_k='+k_itemset_number+'+.txt')