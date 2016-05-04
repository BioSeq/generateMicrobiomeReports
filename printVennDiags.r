#!/usr/bin/env Rscript
#
# printPieChart.r
# Author: Mark Hartman
# Copyright (c) 2016 BioSeq
#
# Given a set of the 10 most prevalent bacteria in a sample, creates a corresponding Venn diagram 
#
#import
require(plotrix)

# Command Line args
args <- commandArgs(TRUE)

# CONSTANTS
sampleName1 = args[1]
sampleName2 = args[2]
vennList1 = args[3]
vennList2 = args[4]

makeVennList <- function(vennListInput){
vennList = unlist(strsplit(vennListInput,","))
indexOfOther = match("Other",vennList)
vennList = vennList[-indexOfOther]
return(vennList)
}

vennList1 = makeVennList(args[3])
vennList2 = makeVennList(args[4])
# vennList2 = unlist(strsplit(vennList2,","))


outputDir = "C:\\Users\\mhartm02\\Dropbox\\Lab administration and operation - Tufts\\Coding practice\\vennDiagOutput\\"
filename = paste(outputDir,sampleName1,".pdf",sep="")
pdf(file=filename, height=11, width=8.5)
par(mfrow=c(3,1),mar=c(0,0,0,0))

#parameters for layout of the Venn diagram and text
#vennX1 = 0.375 centers the Venn diagram on the page
radius = 0.2
vennX1=0.625; vennY1=0.5
vennX2=vennX1+radius; vennY2=vennY1
#placement of lists of microbes within each circle
textX1=vennX1-0.05; textY1=vennY1+0.3
textX2=vennX1+0.18; textY2=textY1
textSize = 1.2
#placement of the title near the top of each circle (e.g. SH07_RC)
titleX1=textX1+0.02; titleY1=textY1+0.05
titleX2=titleX1+0.26; titleY2=titleY1
titleSize = 2
#first Venn diagram has message 1, second and third Venn diagrams have message 2
message1 = "SAME person, DIFFERENT body sites"
message2 = "DIFFERENT people, SAME body site"
windowsFonts(A=windowsFont("Arial Black"),B=windowsFont("Myriad Pro"))


drawVennDiagram <- function(message, leftSampleName, rightSampleName, leftVennList, rightVennList){
draw.circle(vennX1,vennY1,radius,nv=100,border=NULL,col=NA,lty=1,lwd=1)
draw.circle(vennX2,vennY1,radius,nv=100,border=NULL,col=NA,lty=1,lwd=1)
legend(textX1,textY1, leftVennList, cex=textSize, bty="n",adj=c(1,NA))
legend(textX2,textY2, rightVennList, cex=textSize, bty="n")
text(titleX1,titleY1,leftSampleName, cex=titleSize, font=2)
text(titleX2,titleY2,rightSampleName, cex=titleSize, font=2)
text(titleX1+0.02,titleY1+0.08,"Sample 1", cex=0.8, font=3)
text(titleX2-0.02,titleY2+0.08,"Sample 2", cex=0.8, font=3)
text(0,0.9, message, cex=2, font=2, adj=c(0,NA))
text(0,0.5, "How many microbes are found in BOTH Sample 1 and Sample 2?
Answer 1:\n\n\n\n
How many different microbes are found in either sample?
(Don't count any more than once.)
Answer 2:\n\n\n\n
Calculate the Jaccard Similarity:
Divide Answer 1 by Answer 2 and multiply by 100%",
	cex=1, font=2, adj=c(0,NA))
}

#Draw all three Venn diagrams
plot.new()
drawVennDiagram(message1, sampleName1, sampleName2, vennList1, vennList2)
plot.new()
drawVennDiagram(message2, sampleName1, "", vennList1, "")
plot.new()
drawVennDiagram(message2, sampleName2, "", vennList2, "")
