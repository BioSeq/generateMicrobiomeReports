#!/usr/bin/env Rscript
#
# makepiechart.r
# Author: Hannah Voelker
#Last modified: 5/5/16
#Adapted from printPieChart.r
# Given a set of the 10 most prevalent bacteria in a sample, creates a corresponding pie chart 
#

#import
require(plotrix)

# get the csv file
genuscounts <<- read.csv(file.choose(), header = TRUE, sep = ",")

#loop through the data frame and find the top ten for each 
for(i in 2:ncol(genuscounts)) {
    col <- genuscounts[,i] # extract col
    topten = head(sort(col,decreasing = TRUE), n = 10)
    totalcount = sum(genuscounts[,i])
    slices = topten/totalcount
    
  # add labels
  slices = round(slices*100,2)
  lbls <- topten[1]
  lbls = paste(lbls,as.character(slices))
  lbls = paste(lbls,"%",sep="")

  # output and aesthetics 
  outputDir = "users/hannahvoelker/Documents/BioSeq"
  samplename = genuscounts[i]
  colors = rainbow(length(slices))
  # windowsFonts(A=windowsFont("Arial Black"),B=windowsFont("Myriad Pro"))
  pie(slices, '', radius = 0.6, col=colors, main=samplename, cex.main=5, mai=c(0.2,0,2,0.2),family="serif")
  # can use font.main = '' to adjust the font of main title
  x= 0.8
  y= 0.6
  legend(x,y, lbls, cex=3.6, fill=colors)
  textX = 0
  textY = 0.95
  text(textX,textY,'This sample\'s microbiome, broken down by genus:', cex=4.7, font=4, family="serif")
  textX = -1.6
  textY = 0
  text(textX,textY,' DISCLAIMER:\n Results cannot be\n used to draw any\n conclusions about\n health information.', cex=4, adj=c(0,NA), font=3, family="serif")
  filename = paste(outputDir,samplename,".png",sep="")
  dev.off()
  png(file = filename, height=1200, width=2200)
} 
# this is the end of the for loop
