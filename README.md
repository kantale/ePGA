# ePGA

Working installation: [http://www.epga.gr/](http://www.epga.gr/)

ePGA is comprised by two different services: Explore and Translate.

Explore:
* Receive personalized recommendations based on gene-drug-phenotype associations.
* Browse the state of the art pharmacogenomics knowledge on gene-drug-phenotype associations.

Translate:
* Upload individual genotypes and receive a report on their phenotypes for all known pharmacogenes.
* Browse pharmacogenomics summary data on a set of genotypes.

These are two independent web services, although in order to get full functionality both should be running. 

LICENSE: [GNU GENERAL PUBLIC LICENSE, Version 3](LICENSE.md)

## Explore Installation
The ePGA explore service is a django app that is located on the [ePGA](ePGA/) folder. This repo includes an example project called 'main'. To test the installatio run:
```bash
python manage.py runserver 0.0.0.0:8000
```

## Translation Installation
The Translation service of ePGA is a shiny web application. To install, make sure that the following packages are installed in R: ```shiny```, ```shinyBS```, ```rmarkdown```.

Also the followig biocLite packages are necessary: [VariantAnnotation](https://bioconductor.org/packages/release/bioc/html/VariantAnnotation.html)

Edit: [Translation/translation.r](Translation/translation.r) file and set the desired IP and port values:

```
runApp(host="0.0.0.0",port = 8080)
```

Edit the file [ePGA/templates/ePGA/translate.html](ePGA/templates/ePGA/translate.html) and insert the same values in the line:
```html
<iframe id="example1" src="http://0.0.0.0:8080/" style="border: none; width: 1350px; height: 850px" frameborder="0"  scrolling="yes" align="center"></iframe>
```

Start with:
```bash
/usr/bin/R CMD BATCH ./translation.r
```

## Contact
Development
* [Alexandros Kanterakis](mailto:kantale@ics.forth.gr)
* [Evgenia Kartsaki](mailto:ekartsak@ics.forth.gr)

Supervision
* [Patrinos George](mailto:gpatrinos@upatras.gr)
* [Potamias George](mailto:potamias@ics.forth.gr)


