library(shiny)
library(shinyBS)

shinyUI(fluidPage(title="ePGA Translation",
                  includeCSS('www/style.css'),
                  sidebarLayout(
                    sidebarPanel(h3("Input", align="center"),
                                 hr(),
                                 selectInput("gen", label = h4("Genotype File"), 
                                             choices = list(
                                               "1000 Genomes Phase-1 (1092 Samples)" = 1,
                                               "1000 Genomes Phase-3 (2504 Samples)" = 3,
                                               "1000 Genomes Phase-3 (1 Sample)" = 0),
                                             selected = 1),
                                 helpText('Available in ',
                                          a(href="http://www.1000genomes.org/wiki/analysis/variant%20call%20format/vcf-variant-call-format-version-41",target="blank", "VCF"),
                                          'format;you may download an',
                                          a(href="1KG-samples.vcf", download="1KG-samples.vcf", "example VCF file")),
                                 #downloadLink("vcf", "example VCF file")),
                                 div(id="ic1",icon("info-circle"),
                                     a(href= "PGx_Translation.pdf", download="PGx_Translation.pdf", "Get help"),
                                     style="text-align: right;"),
                                 fileInput("file",label=h4("File for Customized Translation (optional)"), multiple=F,
                                           accept = c(
                                             'text/csv',
                                             'text/comma-separated-values',
                                             'text/plain',
                                             '.csv'
                                           )),
                                 helpText('List of variant RS ids; Translation is performed just on these variants.
                                          You may download and save an ',a(href="actionable.txt", download="actionable.txt", "example file,"),
                                          'which then you may store and upload'),
                                 hr(),               
                                 div(actionButton("goButton", "Go!", icon = icon("user-md", "fa-2x")), 
                                     "Please refer to the",
                                     a(target="popup", onclick= "window.open('ePGA_Purpose_and_Use.pdf','popup','width=1000,height=700'); return false;",
                                       tags$u("Purpose and Use of ePGA Translation Service")),
                                     style="text-align: center; color:red"),
                                 #htmlOutput("summary"),
                                 hr()), 
                    mainPanel(
                      navbarPage(title="", collapsible=T, id = "tabs",
                                 tabPanel("Welcome",
                                          h2("Pharmacogenomics (PGx) Translation Service",  style = "font-family: 'gill sans MT'"),
                                          hr(),
                                          fluidRow(
                                            column(7
                                            ),
                                            column(3,
                                                   includeHTML("www/html/quote.html")
                                            ),
                                            column(2,
                                                   img(src = "pictures/hippocrates.png",height="100", width="80")
                                            )
                                          ),
                                          br(),
                                          includeHTML("www/html/body.html"),
                                          icon =  icon("star")                      
                                 ),
                                 tabPanel(value="tabF",
                                          title="ePGA Translation", 
                                          h4("About"),
                                          p("ePGA Translation considers the entire list of SNPs."),
                                          hr(),
                                          conditionalPanel("output.full",
                                                           div(id="pheno", img(src = "pictures/pheno.png", height="40", width="500"),
                                                               style="text-align: center;")
                                          ),
                                          br(),
                                          dataTableOutput("full"),
                                          conditionalPanel("output.full",
                                                           div(id="download", downloadButton('downloadReport1',"Download Report"),
                                                               style="text-align: right;"))
                                 ),
                                 tabPanel(value="tabC",
                                          title="Custom Translation", 
                                          h4("About"),
                                          p("Custom Translation considers only the list of SNPs uploaded."),
                                          hr(),
                                          conditionalPanel("output.actionable",
                                                           div(id="pheno", img(src = "pictures/pheno.png", height="40", width="500"),
                                                               style="text-align: center;")
                                          ),
                                          br(),
                                          dataTableOutput("actionable"),
                                          conditionalPanel("output.actionable",
                                                           div(id="download", downloadButton('downloadReport2',"Download Report"),
                                                               style="text-align: right;"))
                                 ),
                                 tabPanel("Gene Summary", 
                                          h4("About"),
                                          p("Gene Summary is based on ePGA(FULL) Translation."),
                                          hr(),   
                                          conditionalPanel("output.full",
                                                           div(id="pheno", img(src = "pictures/pheno2.png", height="40", width="700"),
                                                               style="text-align: center;")
                                          ),
                                          br(),
                                          dataTableOutput("genes")),
                                 tabPanel("Sample Summary", 
                                          h4("About"),
                                          p("Sample Summary is based on ePGA(FULL) Translation."),
                                          hr(),
                                          conditionalPanel("output.full",
                                                           div(id="pheno", img(src = "pictures/pheno.png", height="40", width="500"),
                                                               style="text-align: center;")
                                          ),
                                          br(),
                                          dataTableOutput("samples"))
                      )
                    )
                  )
))