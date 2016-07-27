# ePGA

Working installation: [http://www.epga.gr/](http://www.epga.gr/)

Use ePGA’s explore service to:
* Receive personalized recommendations based on gene-drug-phenotype associations.
* Browse the state of the art pharmacogenomics knowledge on gene-drug-phenotype associations.

Use ePGA’s translate service to:
* Upload individual genotypes and receive a report on their phenotypes for all known pharmacogenes.
* Browse pharmacogenomics summary data on a set of genotypes.

LICENSE: [GNU GENERAL PUBLIC LICENSE, Version 3](LICENSE.md)

## INSTALLATION
The ePGA explore is a django app. This repo includes an example project called 'main'. To test the installatio run:
```bash
python manage.py runserver 0.0.0.0:8000
```

## Translation
Make sure that the following packages are installed in R: ```shiny```, ```shinyBS```, ```rmarkdown```.

Also the followig biocLite packages are necessary: [VariantAnnotation](https://bioconductor.org/packages/release/bioc/html/VariantAnnotation.html)

Edit: [Translation/translation.r](Translation/translation.r) file and set the desiref IP and port values:

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


