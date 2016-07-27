translateCustom <- function(file, phase){
  
  library(doSNOW)
  
  actionable <- scan(file, what="", sep=",", quiet=T)
  
  pharm <- read.table("data/pharmAnnotation.txt", header=T, sep="\t")
  
  genes <- pharm[pharm$rs_id %in% actionable, 1]
  
  files <- paste("data/TranslationTables", paste(genes, ".table", sep=""), sep="/")
  haplotables <- lapply(files, read.table, sep="\t", header=F, comment.char="", quote="")

  refAlleles <- read.table("data/refAlleles.txt", sep="\t", comment.char = "", row.names=1)
  #refAlleles <- refAlleles[genes,]
  
  if(phase == 0){
    genotypes <- read.table("data/1KG-phase3.txt", sep="\t", header=T, row.names=1)[,1, drop=F]
    #keep only the genotypes for the given SNPs
    genotypes <- na.omit(genotypes[actionable, , drop=F])
  }else{
    filename <- paste("data/1KG-phase",phase,".txt",sep="")
    genotypes <- read.table(filename, sep="\t", header=T, row.names=1)
    #keep only the genotypes for the given SNPs
    genotypes <- na.omit(genotypes[actionable,])
  }
  
  if(nrow(genotypes) == 0)
    return(NULL)
  
  #parallel programming
  nCores <- 4
  
  #creating the cluster
  cl <- makeCluster(nCores)
  
  #registering the cluster
  registerDoSNOW(cl)
  
  system.time(
    result <- foreach(i= 1:ncol(genotypes), .combine="rbind") %dopar% {
      library(gdata)
      source("R/match.R")
      options(stringsAsFactors=FALSE)
      match(genotypes,i, haplotables, refAlleles)
    })
  
  #stopping the cluster
  stopCluster(cl)
  
  return(result)
}