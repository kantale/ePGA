
install.packages('shiny', repos='http://cran.us.r-project.org')
install.packages('shinyBS', repos='http://cran.us.r-project.org')
install.packages('rmarkdown', repos='http://cran.us.r-project.org')
install.packages('doSNOW', repos='http://cran.us.r-project.org')
install.packages('gdata', repos='http://cran.us.r-project.org')
install.packages('knitr', repos='http://cran.us.r-project.org')
install.packages('XML', repos='http://cran.us.r-project.org')
install.packages('RMySQL', repos='http://cran.us.r-project.org')
install.packages('rtracklayer', repos='http://cran.us.r-project.org')

source("https://bioconductor.org/biocLite.R")

BiocInstaller::biocLite(c("VariantAnnotation"))

