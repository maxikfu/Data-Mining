#here we will manage data pre-processing
import sys
class Data_PreProcessing:
	def __init__(self,file):
		self.dictionary = {}#maping ids to its integer value
		self.transactionDB = {}#dictionary of lines from txt file where ids replaced by it's integer value
		self.unigram_count = {}
		idGen = 0
		setOfTransactions=set()
		transactionID =0
		for line in open(file,'r'):
			newLine=set()
			for ids in line.split():
				if ids in newLine:
					print('They repeat in one transaction')
				else:
					newLine.add(ids)
				if ids not in self.dictionary:
					self.dictionary[ids]=idGen
					setOfTransactions.add(transactionID)
					self.transactionDB[idGen] =setOfTransactions
					setOfTransactions=set() 
					self.unigram_count[tuple([idGen])]=1
					idGen+=1
				else:
					self.transactionDB[self.dictionary[ids]].add(transactionID)
					self.unigram_count[tuple([self.dictionary[ids]])]+=1
			transactionID+=1
