
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

pdf(file = "samplegraphs.pdf", width = 8.5, height = 11, onefile = TRUE)

#loop through the data frame and find the top ten for each 
for(i in 2:ncol(genuscounts)) {
    thisColumn <- genuscounts[,c(1,i)]
    topten <- head(thisColumn[order(thisColumn[,2], decreasing = TRUE), ], 10)
    totalcount = sum(genuscounts[,i])
    slices = topten[,2]/totalcount
    
  # add labels
  slices = round(slices*100,2)
  lbls <- topten[,1]
  lbls = paste(lbls,as.character(slices))
  lbls = paste(lbls,"%",sep="")

  samplename = names(genuscounts[i])

  colors = rainbow(length(slices))
  pie(slices, '', radius = 0.6, col=colors, main=samplename, cex.main=6.0, mai=c(0.2,0.2,0.2),family="serif")
  # can use font.main = '' to adjust the font of main title
  x= -0.5
  y= -0.65
  legend(x,y, lbls, cex=1.0, fill=colors)
  textX = 0
  textY = 0.95
  text(textX,textY,'This sample\'s microbiome, broken down by genus:', cex=2, font=4.0, family="serif")
  textX = 0.5
  textY = -1.0
  text(textX,textY,' DISCLAIMER:\n Results cannot be\n used to draw any\n conclusions about\n health information.', cex=1, adj=c(0,NA), font=0.5, family="serif")
} 
dev.off()
# this is the end of the for loop
