#!usr/bin/env python

#convertAggregateCountsToVennDiagrams.py
#Author: Mark Hartman
#Date created: 3/31/2016
#Last modified: 05/04/2016

#Given a spreadsheet of counts for various genus (or other OTU level) for each sample
# Format as shown:
#Genus,MH01-A,MH95HP,MH10-B, ...
#Streptococcus,38,79115,6225, ...
#Propionibacterium,26,3,36045, ...
#Staphylococcus,5,3,6028, ...
#...
#This list should have default filename 'Genus_Level_Aggregate_Counts.csv'
# (Note: This type of file is available from the BaseSpace 16S Metagenomics App.)
#ALSO MUST BE GIVEN a list of pairs of sample names:
# Format as shown:
# SH78_RC	SH78_HP
# SH62_RC	SH62_HP	
# SH95_RC	ALT2_HP	
#This list should have default filename 'microbiomeSamplePairs.txt'
#Return Venn diagrams for each sample in pdf format
# REQUIRES R SCRIPT printVennDiags.r



import subprocess as sp

INPUT_FILENAME = 'Genus_Level_Aggregate_Counts.csv'
PAIRS_LIST_FILENAME = 'microbiomeSamplePairs.txt'

def main():
	readDataOutput = readData(INPUT_FILENAME)
	listOfSamples = readDataOutput[0]
	listOfGenus = readDataOutput[1]
	aggregateCounts = readDataOutput[2]
	dictOfSampleNamesTopGenus = makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus)
	prepDataForVennDiags(dictOfSampleNamesTopGenus, PAIRS_LIST_FILENAME)

def readData(INPUT_FILENAME):
	#read in sample names, genus names, and aggregate counts
	with open(INPUT_FILENAME, 'r') as filer:
		listOfSamples = filer.readline().strip().split(',')[1:]
		listOfGenus = []
		aggregateCounts = []
		for line in filer:
			currentLine = line.strip().split(',')
			listOfGenus.append(currentLine[0])
			aggregateCounts.append(currentLine[1:])
	aggregateCounts = map(list, zip(*aggregateCounts)) #transpose the aggregate counts
	aggregateCounts = [map(int, x) for x in aggregateCounts] #convert aggregate counts to int
	return (listOfSamples, listOfGenus, aggregateCounts)

def makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus):
#convert aggregate counts to presence/absence calls for each genus
#make a list of sets, each set contains the ten most abundent genus in each sample
#requires aggregateCounts, listOfGenus, listOfSamples
	listOfMostAbundantGenus = []
	for samplewiseAggregateCounts in aggregateCounts:
		listOfMaxValueIndexes = []
		mostAbundantGenus = []#initializes the list that will contain the 10 most abundent genus
		totalAggregateCounts = sum(samplewiseAggregateCounts)		
		for x in range(10):
			highestNumOfAggregateCounts = max(samplewiseAggregateCounts)
			currIndex = samplewiseAggregateCounts.index(highestNumOfAggregateCounts)
			mostAbundantGenus.append((listOfGenus[currIndex],float(highestNumOfAggregateCounts)/float(totalAggregateCounts)))
			samplewiseAggregateCounts[currIndex] = 0
		otherAggregateCounts = sum(samplewiseAggregateCounts)
		mostAbundantGenus.append(('Other',float(otherAggregateCounts)/float(totalAggregateCounts)))
		listOfMostAbundantGenus.append(mostAbundantGenus)
		listOfMostAbundantGenus.sort(reverse= True) #ensures we sorted correctly
	#zip these sets into a dictionary {key = sample name: value = set of most abundant genus}
	dictOfSampleNamesTopGenus = dict(zip(listOfSamples,listOfMostAbundantGenus))
	return dictOfSampleNamesTopGenus

def prepDataForVennDiags(dictOfSampleNamesTopGenus, PAIRS_LIST_FILENAME):
	sampleName1 = ""
	sampleName2 = ""
	with open(PAIRS_LIST_FILENAME,'r') as filer:
		for line in filer:
			sampleNames = line.strip().split('\t')
			sampleName1 = sampleNames[0]
			sampleName2 = sampleNames[1]
			sampleData1 = []
			sampleData2 = []
			for value in dictOfSampleNamesTopGenus[sampleName1]:
				sampleData1.append(value[0]+',')
			for value in dictOfSampleNamesTopGenus[sampleName2]:
				sampleData2.append(value[0]+',')
			passDataForVennDiags(sampleName1, sampleName2, sampleData1, sampleData2)

def passDataForVennDiags(sampleName1, sampleName2, sampleData1, sampleData2):
	pathToR = "C:\\Program Files\\R\\R-3.2.2\\bin\\x64\\Rscript.exe" 
	pathToScript = "C:\Users\mhartm02\Dropbox\Lab administration and operation - Tufts\Coding practice\printVennDiags.r"
	sp.call([pathToR, pathToScript,  sampleName1, sampleName2, sampleData1, sampleData2])


if __name__ == '__main__':
        main()
