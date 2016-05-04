#!usr/bin/env python

#convertAggregateCountsToPieCharts.py
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
# (Note: This type of file is available from the BaseSpace 16S Metagenomics App.)
#
#Return pie chart images for each sample as png format
# REQUIRES R SCRIPT printPieChart.r

import subprocess as sp

INPUT_FILENAME = 'Genus_Level_Aggregate_Counts.csv'

def main():
	readDataOutput = readData(INPUT_FILENAME)
	listOfSamples = readDataOutput[0]
	listOfGenus = readDataOutput[1]
	aggregateCounts = readDataOutput[2]
	dictOfSampleNamesTopGenus = makeDictOfTopGenus(aggregateCounts, listOfSamples, listOfGenus)
	prepDataForPieCharts(dictOfSampleNamesTopGenus)

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
		mostAbundantGenus = set() #initializes the set that will contain the 10 most abundent genus
		totalAggregateCounts = sum(samplewiseAggregateCounts)		
		for x in range(10):
			highestNumOfAggregateCounts = max(samplewiseAggregateCounts)
			currIndex = samplewiseAggregateCounts.index(highestNumOfAggregateCounts)
			mostAbundantGenus.add((listOfGenus[currIndex],float(highestNumOfAggregateCounts)/float(totalAggregateCounts)))
			samplewiseAggregateCounts[currIndex] = 0
		otherAggregateCounts = sum(samplewiseAggregateCounts)
		mostAbundantGenus.add(('Other',float(otherAggregateCounts)/float(totalAggregateCounts)))
		listOfMostAbundantGenus.append(mostAbundantGenus)
	#zip these sets into a dictionary {key = sample name: value = set of most abundant genus}
	dictOfSampleNamesTopGenus = dict(zip(listOfSamples,listOfMostAbundantGenus))
	return dictOfSampleNamesTopGenus

#convert the list of Jaccard values from floats to strings
	#dictOfSampleNamesTopGenus = map(str, dictOfSampleNamesTopGenus)
def prepDataForPieCharts(dictOfSampleNamesTopGenus):
	for key in dictOfSampleNamesTopGenus:
		dataForR = []
		title = key
		for value in dictOfSampleNamesTopGenus[key]:
			for item in value:
				dataForR.append(str(item)+',')
			passDataForPieCharts(title, dataForR)

def passDataForPieCharts(title, dataForR):
	pathToR = "C:\\Program Files\\R\\R-3.2.2\\bin\\x64\\Rscript.exe" 
	pathToScript = "C:\Users\mhartm02\Dropbox\Lab administration and operation - Tufts\Coding practice\printPieChart.r"
	sp.call([pathToR, pathToScript, title, dataForR])

if __name__ == '__main__':
        main()
