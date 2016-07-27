match <- function(genotypes, id, haplotables, refAlleles){
  
  sample <- colnames(genotypes)[id]
  snpsG <- row.names(genotypes)
  
  df <- data.frame()
  
  for (haplotable in haplotables)
  {
    gene <- haplotable[1,1]
    colnames(haplotable) <- haplotable[1,]
    haplotable <- haplotable[-1,]
    row.names(haplotable) <- NULL
    
    ref <- refAlleles[gene,]
    
    #snps per gene-table
    snpsT <- haplotable[,1]
    
    common <- snpsT[snpsT %in% snpsG]
    
    if(length(common) !=0){
      #SNPs in table that the genotypes don't have
      #remove alleles with variations in these SNPs
      notCom <- which(!snpsT %in% snpsG)
      for(i in notCom){
        ind <- which(haplotable[i,-c(1:7)] != haplotable[i,4])
        if(length(ind) != 0){
          ind <- ind+7
          haplotable <- haplotable[,-ind]
        }
      }
      if(length(notCom) != 0 )
        haplotable <- haplotable[-notCom,]
      
      haplotypes <- haplotable[,-c(1:7)]
      
      genotype <- strsplit(genotypes[common, id], "/")
      g1 <- sapply(genotype, "[", 1)
      g2 <- sapply(genotype, "[", 2)
      
      if(class(haplotypes) == "data.frame"){
        haplo1 <- names(which(apply(haplotypes == g1, 2, all)))
        haplo2 <- names(which(apply(haplotypes == g2, 2, all)))
        
        #if no match, give value NM to haplotype
        #if multiple matches, keep first one
        if(length(haplo1) == 0 )
          haplo1 <- "NM"
        else haplo1 <- haplo1[1]
        if(length(haplo2) == 0 )
          haplo2 <- "NM"
        else haplo2 <- haplo2[1]
      }else{ #if there is only one haplotype in table
        if(all(haplotypes == g1)){
          haplo1 <- colnames(haplotable)[8]
        }else 
          haplo1 <- "NM"
        if(all(haplotypes == g2)){
          haplo2 <- colnames(haplotable)[8]
        }else haplo2 <- "NM"
      }
     
      diplotype <- paste(haplo1, haplo2, sep="/")
      
      #phenotype inference
      if(haplo1 == "NM" | haplo2 == "NM"){
        diplotype <- "NM"
        pheno <- "NM"
      }else if( haplo1 == ref & haplo2 == ref){
        pheno <- "WT/WT"
      }else if( haplo1 == ref | haplo2 == ref){
        pheno <- "WT/Var"
      }else 
        pheno <- "Var/Var"
      row = c(sample,gene,diplotype,pheno)
    }else
      row = c(sample,gene,"NO_INFO","NI")
    df <- rbind(df,row)
  }
  colnames(df) <- c("sample","gene", "diplotype", "phenotype")
  
  return(df)
}

