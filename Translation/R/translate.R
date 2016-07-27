rm(list = ls())
options(stringsAsFactors=FALSE)

library(doSNOW)
source("R/match.R")

files <- list.files("data/TranslationTables", pattern = "*.table", full.names = T)
haplotables <- lapply(files, read.table, sep="\t", header=F, comment.char="", quote="")

refAlleles <- read.table("data/refAlleles.txt", sep="\t", comment.char = "", row.names=1)

nCores <- 4

#creating the cluster
cl <- makeCluster(nCores)

#registering the cluster
registerDoSNOW(cl)

genotypes <- read.table("data/1KG-phase1.txt", sep="\t", header=T, row.names=1)
print("starting...")
system.time(
match1 <- foreach(i= 1:ncol(genotypes), .combine="rbind" ) %dopar% {
  library(gdata)
  options(stringsAsFactors=FALSE)
  match(genotypes,i, haplotables, refAlleles)
})

print("done 1092 samples")

genotypes <- read.table("data/1KG-phase3.txt", sep="\t", header=T, row.names=1)

system.time(
match2 <- foreach(i= 1:ncol(genotypes), .combine="rbind" ) %dopar% {
  library(gdata)
  options(stringsAsFactors=FALSE)
  match(genotypes,i, haplotables, refAlleles)
})

print("done 2054 samples")

#stopping the cluster
stopCluster(cl)

fileM <- paste("output/","emodia",0,".match",sep="")
write.table(match2[match2$sample == "HG00096",], fileM, sep="\t", col.names = T, quote=F, row.names=F)
fileM <- paste("output/","emodia",1,".match",sep="")
write.table(match1, fileM, sep="\t", col.names = T, quote=F, row.names=F)
fileM <- paste("output/","emodia",3,".match",sep="")
write.table(match2, fileM, sep="\t", col.names = T, quote=F, row.names=F)
  
