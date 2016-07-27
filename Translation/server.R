library(shiny)
library(shinyBS)
library(rmarkdown)
library(VariantAnnotation)
options(shiny.maxRequestSize=30*1024^2) 
options(stringsAsFactors=FALSE)

#run only if tables or genotypes have changed
#source("R/translate.R")

#code that runs per user
source("R/translateCustom.R")
source("R/analysis.R")

shinyServer(function(input, output, session){
  
  #Change the selected tab depending on input 
  observe({
    if(input$goButton>0)
    {
      if(is.null(input$file))
        updateTabsetPanel(session, "tabs", selected = "tabF")
      else 
        updateTabsetPanel(session, "tabs", selected = "tabC")
    }
  })
  #generate report for full translation
  output$downloadReport1 <- downloadHandler(
    
    filename= "eMoDiA-report.pdf",
    
    content = function(file) {
      library(rmarkdown)
      inputEnv <- new.env() 
      inputEnv$df <- loadFULL()
      #delete recommendations
      inputEnv$df[,5] <- NULL
      out <-rmarkdown::render("report.Rmd", "pdf_document", envir = inputEnv)
      file.rename(out, file)
    },
    
    contentType = 'application/pdf'
  )
  #generate report for custom translation
  output$downloadReport2 <- downloadHandler(
    
    filename= "eMoDiA-report.pdf",
    
    content = function(file) {
      inputEnv <- new.env() 
      inputEnv$df <- loadCustom()
      out = rmarkdown::render("report.Rmd", "pdf_document", envir = inputEnv)
      file.rename(out, file)
    },
    
    contentType = 'application/pdf'
  )
  
  loadFULL <- reactive ({ 
    phase <- input$gen
    
    outFile <- paste("output/", "emodia", phase, ".match", sep="")
    
    withProgress(message = 'Loading...', value = 0, {
      
      df <- read.table(outFile, header=T, sep="\t", comment.char="", quote="")
      #filter out NO_MATCH & NO_INFO
      df <- df[!(df$phenotype=="NM"),]
      df <- df[!(df$phenotype=="NI"),]
      row.names(df) <- NULL
      
      print("dataset loaded..")
      
      incProgress(0.3, detail="Dataset loaded")
      Sys.sleep(0.1)
      
      checkRec <- read.table("data/genes_alleles.txt", sep="\t", header=T, comment.char="", quote="")
      checkRec <- checkRec[!duplicated(checkRec),]
      checkRec <- split(checkRec, checkRec$Gene)
      
      #create URL links  to explore recommendations
      #only for diplotypes that exist in explore
      links <- apply(df,1,function(r)
      {
        gene <- strsplit(r[2], split="_2")[[1]]
        checkRecGene <- checkRec[[gene]]
        diplotype_rev <- paste(rev(strsplit(r[3],"/")[[1]]), collapse="/")
        if( r[3] %in% checkRecGene$Alleles ){
          diplo <- URLencode(gsub("/","&",r[3]),reserved = T)
          link <- paste("http://139.91.210.31/explore",gene,diplo,sep="/")
        }else if( diplotype_rev %in% checkRecGene$Alleles){ #due to string matching, diplotypes may be reversed ex. *9A/*1
          diplo <- URLencode(gsub("/","&",diplotype_rev),reserved = T)
          link <- paste("http://139.91.210.31/explore",gene,diplo,sep="/")
        }else if( gene %in% c("ZNF804A","TMCC1","LECT2","OR52J3,OR52J2P","OR52E2","SCN8A","ASIC2")){
          link <- "https://www.pharmgkb.org/pmid/21961650"
        }else
          link <- ""
      })
      print("Links created..")
      
      incProgress(0.3, detail="Links created")
      Sys.sleep(0.1)
      
      idx <- links == ""
      Recommendations <- paste0("<a href='",  links, "' target='_blank'>Check</a>")
      Recommendations[idx] <- "Not Available"
      
      incProgress(0.4, detail="Done")
      Sys.sleep(0.1)
      
      print("END OF FULL")
      
      df <- cbind(df,Recommendations)
      
    })
  })
  
  #FULL Translation  
  output$full <- renderDataTable({
    
    if (input$goButton == 0){
      validate("Please click on the 'Go' button to start the translation process")
      return()
    }
    
    print("FULL")
    
    df <- isolate(loadFULL())
    
  },
  options = list(pageLength = 10, 
                 rowCallback = I(
                   'function(nRow, aData) {
                   if (aData[3] == "WT/WT"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "green");
                   }
                   if (aData[3] == "WT/Var"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "yellow"); 
                   }
                   if (aData[3] == "Var/Var"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "red");          
                   }
                }'),
                 autoWidth = T,
                 columnDefs = list(list(targets = 3 , searchable = F , orderable = F), list(targets=4, searchable=F)),
                 dom= "lrtip", info=TRUE
  ),
  escape=c(4) )
  
  loadCustom <- reactive({
    
    file <- input$file$datapath
    phase <- input$gen
    df <- translateCustom(file,phase)
    
    validate(need(df,"No diplotypes matched based on this actionable SNPs' file!"))
    
    print("custom translation done")
    #filter out NO_MATCH & NO_INFO
    df <- df[!(df$phenotype=="NM"),]
    df <- df[!(df$phenotype=="NI"),]
    
  })
  
  #Custom Translation
  output$actionable <- renderDataTable({
    
    if (input$goButton == 0){
      validate("Please upload an actionable file and then click on the 'Go' button") 
      return()
    }
    
    print("CUSTOM")
    
    isolate({
      file <- input$file$datapath
      validate(need(file, "Please upload an actionable file and then click on the 'Go' button")) 
    })  
    
    withProgress(message = 'Loading...', detail = "This may take a while...", value = 0, {
      
      df <- isolate(loadCustom())
      
      incProgress(0.5, detail="Translation done")
      Sys.sleep(0.1)
      
      checkRec <- read.table("data/genes_alleles.txt", sep="\t", header=T, comment.char="", quote="")
      checkRec <- checkRec[!duplicated(checkRec),]
      checkRec <- split(checkRec, checkRec$Gene)
      
      #create URL links  to explore recommendations
      #only for diplotypes that exist in explore
      links <- apply(df,1,function(r)
      {
        gene <- strsplit(r[2], split="_2")[[1]]
        checkRecGene <- checkRec[[gene]]
        diplotype_rev <- paste(rev(strsplit(r[3],"/")[[1]]), collapse="/")
        if( r[3] %in% checkRecGene$Alleles ){
          diplo <- URLencode(gsub("/","&",r[3]),reserved = T)
          link <- paste("http://139.91.210.31/explore",gene,diplo,sep="/")
        }else if( diplotype_rev %in% checkRecGene$Alleles){ #due to string matching, diplotypes may be reversed ex. *9A/*1
          diplo <- URLencode(gsub("/","&",diplotype_rev),reserved = T)
          link <- paste("http://139.91.210.31/explore",gene,diplo,sep="/")
        }else if( gene %in% c("ZNF804A","TMCC1","LECT2","OR52J3,OR52J2P","OR52E2","SCN8A","ASIC2")){
          link <- "https://www.pharmgkb.org/pmid/21961650"
        }else
          link <- ""
      })
      
      print("links created..")
      
      incProgress(0.3, detail="Links created")
      Sys.sleep(0.1)
      
      idx <- links == ""
      Recommendations <- paste0("<a href='",  links, "' target='_blank'>Check</a>")
      Recommendations[idx] <- "Not Available"
      
      incProgress(0.2, detail="Done")
      Sys.sleep(0.1)
      
      print("END OF CUSTOM")
      
      df <- cbind(df,Recommendations)
      
    })
    
  },
  #number of rows to display
  options = list(pageLength = 10, 
                 rowCallback = I(
                   'function(nRow, aData) {
                   if (aData[3] == "WT/WT"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "green");
                   }
                   if (aData[3] == "WT/Var"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "yellow"); 
                   }
                   if (aData[3] == "Var/Var"){
                   $("td:eq(3)", nRow).html("");
                   $("td:eq(3)", nRow).css("background-color", "red");          
                   }
              }'),
                 autoWidth=T,
                 columnDefs = list(list(targets = 3 , searchable = F , orderable = F), list(targets=4, searchable=F)),
                 dom= "lrtip"
  ),
  escape=c(4))
  
  output$genes <- renderDataTable({
    
    if (input$goButton == 0)
      return()
    
    phase <- isolate(input$gen)
    
    outFile <- paste("output/", "emodia", phase, ".match", sep="")
    
    df <- analysis(outFile, 0)
  },
  options = list(pageLength = 10,
                 rowCallback = I(
                   'function(nRow, aData){
                    $("td:eq(3)", nRow).css("background-color", "green");
                    $("td:eq(4)", nRow).css("background-color", "yellow");
                    $("td:eq(5)", nRow).css("background-color", "red");
                  }'),
                 dom= "lrtip"
  ))
  
  output$samples <- renderDataTable({
    if (input$goButton == 0)
      return()
    
    phase <- isolate(input$gen)
    
    outFile <- paste("output/", "emodia", phase, ".match", sep="")
    
    df <- analysis(outFile, 1)
  },
  options = list(pageLength = 10,
                 rowCallback = I(
                   'function(nRow, aData){
                   $("td:eq(1)", nRow).css("background-color", "green");
                   $("td:eq(2)", nRow).css("background-color", "yellow");
                   $("td:eq(3)", nRow).css("background-color", "red");
                }'),
                 dom= "lrtip"
  ))
  
  # output$summary <- renderUI({ 
  #   
  #   if (input$goButton == 0)
  #     return()
  #   list(
  #     h4("Summary"),
  #     pre(includeText("Data/summary.txt"))
  #   )
  # })
})
