analysis <- function(file, flag){

  m <- read.table(file, header=TRUE, sep="\t", fill=TRUE, comment.char="")
  
  #Analysis for Genes
  Gen <- table(m[,c(2,4)])
  Gen <- round(prop.table(Gen,1)*100,2)
  Gen <- as.data.frame.matrix(Gen) 
  Gen <- cbind(Genes=row.names(Gen),Gen)
  row.names(Gen)<-NULL
  colnames(Gen)[4:6] <- c("WT/WT", "WT/Var", "Var/Var")
  colnames(Gen)[-1] <- paste("%",colnames(Gen)[-1])
  
  if(flag == 0 )
    return(Gen)
 
  m <- m[!m$phenotype == "NM" ,]
  m <- m[!m$phenotype == "NI" ,]

  #Analysis for Samples
  Indv <- table(m[,c(1,4)])
  Indv <- round(prop.table(Indv,1)*100,2)
  Indv <- as.data.frame.matrix(Indv) 
  Indv <- cbind(Samples=row.names(Indv),Indv)
  row.names(Indv)<-NULL
  colnames(Indv)[-1] <- c("WT/WT", "WT/Var", "Var/Var")
  colnames(Indv)[-1] <- paste("%",colnames(Indv)[-1])
  
  if (flag == 1)
    return(Indv)
  
  
  
  
  
  
  
}