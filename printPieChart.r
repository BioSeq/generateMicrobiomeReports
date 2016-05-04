#!/usr/bin/env Rscript
#
# printPieChart.r
# Author: Mark Hartman
#Date created: 3/31/2016
#Last modified: 05/04/2016
#
# Given a set of the 10 most prevalent bacteria in a sample, creates a corresponding pie chart 
#

#import
require(plotrix)

# Command Line args
args <- commandArgs(TRUE)

# CONSTANTS
title = args[1]
input = args[2]

input  = strsplit(input, ",")
output = matrix(unlist(input), ncol = 2, byrow = TRUE)
slices = as.numeric(output[,2])
slices = round(slices*100,2)
lbls = output[,1]
lbls = paste(lbls,as.character(slices))
lbls = paste(lbls,"%",sep="")

outputDir = "C:\\Users\\mhartm02\\Dropbox\\Lab administration and operation - Tufts\\Coding practice\\pieChartOutput\\"
filename = paste(outputDir,title,".png",sep="")
png(file=filename, height=1200, width=2200)
colors = rainbow(length(slices))
windowsFonts(A=windowsFont("Arial Black"),B=windowsFont("Myriad Pro"))
pie(slices, '', radius = 0.6, col=colors, main=title, cex.main=5, mai=c(0.2,0,2,0.2),family="A")
# can use font.main = '' to adjust the font of main title
x= 0.8
y= 0.6
legend(x,y, lbls, cex=3.6, fill=colors)
textX = 0
textY = 0.95
text(textX,textY,'This sample\'s microbiome, broken down by genus:', cex=4.7, font=4, family="B")
textX = -1.6
textY = 0
text(textX,textY,' DISCLAIMER:\n Results cannot be\n used to draw any\n conclusions about\n health information.', cex=4, adj=c(0,NA), font=3, family="B")

dev.off()