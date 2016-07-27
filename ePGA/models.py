from django.db import models

# Create your models here.

'id	relatedDrugs	symbol	summaryHtml	textHtml	term	annotation_textHtml	alleles'

#class Dosing(models.Model):
#	id2 = models.CharField(max_length=50)
#	summaryHtml = models.TextField()
#	textHtml = models.TextField()
#	gene = models.ForeignKey('Gene')
#	relatedDrug = models.ForeignKey('RelatedDrugs')
#	term = models.CharField(max_length=50)
#	annotation_textHtml = models.TextField()
#	alleles = models.CharField(max_length=50)

class Gene(models.Model):
	symbol = models.CharField(max_length=50, db_index=True)
	relatedDrugs = models.ManyToManyField('RelatedDrugs')

class RelatedDrugs(models.Model):
	relatedDrug = models.CharField(max_length=50, db_index=True)
	genes = models.ManyToManyField('Gene')

class GeneDrug(models.Model):
	gene = models.ForeignKey('Gene', db_index=True)
	relatedDrug = models.ForeignKey('RelatedDrugs', db_index=True)
	source = models.CharField(max_length=50, db_index=True)
	textHtml = models.TextField()
	summaryHtml = models.TextField()
	url = models.TextField()
	alleles = models.ManyToManyField('Alleles')

class Alleles(models.Model):
	alleles = models.CharField(max_length=50, db_index=True)
	geneDrug = models.ForeignKey('GeneDrug', related_name='reverse_Alleles', db_index=True)
	metabolizerStatus = models.TextField()
	metabolizerStatusProcessed = models.CharField(max_length=50)
	recomendations = models.TextField()
	implications = models.TextField()
	phenotype = models.TextField()
	activityScore = models.TextField()
	url = models.TextField()

	clinicalAnnotations = models.ManyToManyField('ClinicalAnnotation', related_name='reverse_alleles')

class ClinicalAnnotation(models.Model):
	#Clinical Annotation fields
	url = models.CharField(max_length=50)
	Level_of_Evidence = models.CharField(max_length=50)
	Type = models.CharField(max_length=50)
	Disease = models.CharField(max_length=50)
	OMB_Race = models.CharField(max_length=50)
	Race_Notes = models.CharField(max_length=50)
	Clinical_Annotation = models.TextField()
	diplotype = models.CharField(max_length=50)

	alleles = models.ForeignKey('Alleles', db_index=True)


#	term = models.ManyToManyField('Term')
#
#class Term(models.Model):
#	term = models.CharField(max_length=50)
#	geneDrug = models.ForeignKey('GeneDrug', related_name='reverse_term')
#	termValues = models.ManyToManyField('TermValues', related_name='reverse_term')
#
#class TermValues(models.Model):
#	annotation_textHtml = models.TextField()
#	annotation_processed = models.CharField(max_length=50)
#	alleles = models.ManyToManyField('Alleles', related_name='reverse_termValues')
#	term = models.ForeignKey('Term')
#
#class Alleles(models.Model):
#	alleles = models.CharField(max_length=50)
#	termValues = models.ForeignKey('TermValues', related_name='reverse_alleles')
