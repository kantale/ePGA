
import simplejson
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django import forms

import ePGA.models

import re
import itertools
import hashlib
import urllib # For urldecode 

from collections import OrderedDict

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

def process_file(uploaded_file):
	'''
	process a uploaded file
	Return javascript code
	'''

	ret = []

	line_counter = 0
	for line in uploaded_file:
		line_counter += 1

		#Ignore comments 
		if len(line) > 0:
			if line[0] == '#':
				continue

		ls = line.replace('\n', '').split()

		#Allow only 4 fields
		if len(ls) != 4:
			return 'Unformatted input in line %i' % (line_counter)
		ret += [ls]

	return simplejson.dumps(ret)

def index(request, INIT_GENE='', INIT_ALLELES=''):

	version = 2

	if version == 1:
		ret = filter_db([], [], [], [], start=True)

		context = {
		'genes' : ret['genes_names'],
		'gene_number' : len(ret['genes_names'])-0,
		'drugs' : ret['drugs_names'],
		'drug_number' : len(ret['drugs_names'])-0,
		'ms' : ret['ms_names'],
		'ms_number' : len(ret['ms_names'])-0,
		'alleles' : ret['alleles_names'],
		'allele_number' : len(ret['alleles_names'])-0,
		}

		return render(request, 'ePGA/explore.html', context)

	elif version == 2:
		processed_file = "''"
		if request.method == u'POST':
			upload_form = UploadFileForm(request.POST, request.FILES)
			if upload_form.is_valid():
				f = request.FILES['file']
				processed_file = process_file(f)
		else:
			upload_form = UploadFileForm()

		return render(request, 'ePGA/explore.html', {
			'upload_form':upload_form, 
#			'processed_file' : processed_file,
			'upload_data_script' : 'var uds = %s;' % processed_file,
			'init_translation' : 'var init_translation = {"INIT_GENE":"%s", "INIT_ALLELES":"%s"};' % (INIT_GENE, INIT_ALLELES),
			})

def start(request):
	return render(request, 'ePGA/start.html', {})

def about(request):
	return render(request, 'ePGA/about.html', {})

def studies(request):
	return render(request, 'ePGA/studies.html', {})	

def events(request):
	return render(request, 'ePGA/events.html', {})	

def translate(request):
	return render(request, 'ePGA/translate.html', {})	

def explore(request):
	#return render(request, 'ePGA/explore.html', {})
	return index(request)

#Connection with Tzennis's translation 
def explore_translation(request, INIT_GENE, INIT_ALLELES):
	print INIT_GENE
	print INIT_ALLELES
	return index(request, INIT_GENE, INIT_ALLELES)

def query(request):

	ret, filtered = do_query(request)

	#print '-->5->--', len(ret['drugs'])
	#print '---------------------'
	#print ret['check_all']

	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')

def recommendations_GET(request, id_1=None, value_1=None, id_2=None, value_2=None, id_3=None, value_3=None, id_4=None, value_4=None):
	'''
	Adding GET API for recommendations. https://mail.google.com/mail/u/0/#inbox/1528c1602419f98c 
	http://0.0.0.0:8080/explore/recommendations/id1/val1
	http://0.0.0.0:8080/explore/recommendations/id1/val1/id2/val2
	http://0.0.0.0:8080/explore/recommendations/id1/val1/id2/val2/id3/val3
	http://0.0.0.0:8080/explore/recommendations/id1/val1/id2/val2/id3/val3/id4/val4

	http://0.0.0.0:8080/explore/recommendations/id1/val1
	http://0.0.0.0:8080/explore/recommendations/genes/A2M
	http://0.0.0.0:8080/explore/recommendations/genes/A2M,ABCA1
	http://0.0.0.0:8080/explore/recommendations/genes/CYP2D6

	http://0.0.0.0:8080/explore/recommendations/drugs/Enzymes
	http://0.0.0.0:8080/explore/recommendations/drugs/Enzymes/genes/A2M

	http://0.0.0.0:8080/explore/recommendations/ms/Extensive%20Metabolizer

	http://0.0.0.0:8080/explore/recommendations/alleles/rs669

	http://0.0.0.0:8080/explore/recommendations/alleles/*1_*8
	'''
#	print id_1
#	print value_1

#	print id_2
#	print value_2

#	print id_3
#	print value_3

#	print id_4
#	print value_4

	def process_fields(params, name):
		for this_id, value in params:
			if this_id == name:
				if name == 'alleles':
					return [x.replace('_', '/') for x in value.split(',')]
				else:
					return value.split(',')

		return []

	params = zip([id_1, id_2, id_3, id_4], [value_1, value_2, value_3, value_4])

	#Checking for validity
	for this_id, value in params:
		if this_id not in [None, 'genes', 'drugs', 'ms', 'alleles']:
			ret = simplejson.dumps({'error' : 'Unknown field: %s' % (str(this_id))})
			return HttpResponse(ret, content_type='application/json')

	#genes_GET = [u'A2M']
	genes_GET = process_fields(params, 'genes')
	drugs_GET = process_fields(params, 'drugs')
	ms_GET = process_fields(params, 'ms')
	alleles_GET = process_fields(params, 'alleles')

	return recommendations(request,
		genes_GET=genes_GET, drugs_GET=drugs_GET, ms_GET=ms_GET, alleles_GET=alleles_GET)

def rd_connect_GET(request):
	''' 

	### DOES NOT EXIST
	http://www.epga.gr/rd_connect_api/annotations?variant_name=rs12345678
	http://0.0.0.0:8080/rd_connect_api/annotations?variant_name=rs12345678  
	Returns: {}

	
	### EXIST 
	http://www.epga.gr/rd_connect_api/annotations?variant_name=rs12003906
	http://0.0.0.0:8080/rd_connect_api/annotations?variant_name=rs12003906
	Returns: {"URL": "http://www.epga.gr/explore/ABCA1/rs12003906", "SUCCESS": true} 
	'''
	
	#This is a GET request
	if request.method == u'GET':
		GET = request.GET

		if GET.has_key(u'variant_name'): # CHECK API DOCUMENTATION: https://docs.google.com/document/d/1-9sDYEVYfZqTJZdPKjW_kqBd9vjI4dQP0Fn_sYnoy0c/edit# 
			diplotype = GET[u'variant_name']
			
			#Make a request to the API and check if this diplotype exists
			result = recommendations(request, genes_GET=[], drugs_GET=[], ms_GET=[], alleles_GET=[diplotype])
			#This returned a json
			#Check if it returned results
			result_data = simplejson.loads(result.content)
			if result_data['counter'] > 0:

				#We do have information about this diplotype.
				# ATTENTION! We return ONLY the first result (there might be more)
				gene = result_data['gdr'][0]['symbol']
				
				#return_url = 'http://0.0.0.0:8080/explore/%s/%s' % (gene, diplotype)
				#We use the Tzeni's access (gene/diplotype) from the translation service
				return_url = 'http://www.epga.gr/explore/%s/%s' % (gene, diplotype)
				
				#This will be returned to the RD_connect platform
				something_found_d = {
					'url' : return_url,
					'success' : True,
				}
				something_found = simplejson.dumps(something_found_d)
				return HttpResponse(something_found, content_type='application/json')
			else:
				#Return an empty dictionary if nothing is found
				nothing_found = simplejson.dumps({})
				return HttpResponse(nothing_found, content_type='application/json')


def recommendations(request, INIT_GENE=None, INIT_ALLELES=None, genes_GET=None, drugs_GET=None, ms_GET=None, alleles_GET=None):

	# What is the maximum recommendations limit?
	#object_counter_max = 1000
	object_counter_max = -1 # No limit  

	INIT_GENE, INIT_ALLELES = process_INIT_GENE_ALLELES(INIT_GENE, INIT_ALLELES)

	ret, filtered = do_query(request, add_null_tv=True, allowed=True, INIT_GENE=INIT_GENE, INIT_ALLELES=INIT_ALLELES,
		genes_GET=genes_GET, drugs_GET=drugs_GET, ms_GET=ms_GET, alleles_GET=alleles_GET)

	ret = {}
	ret['gdr'] = []

	filtered['geneDrugs'] = list(set(filtered['geneDrugs']))

	object_counter = 0

	for gd in filtered['geneDrugs']:

		#print '--->6->---'
		#print gd
		#print '---6.5---'

		current_gdr = {
			'symbol' : gd.gene.symbol,
			'relatedDrug' : gd.relatedDrug.relatedDrug,
			'source' : gd.source,
			'textHTML' : gd.textHtml,
			'url': gd.url,
			'summaryHTML' : gd.summaryHtml,
			'alleles' : [],
		}

		for a in filtered['alleles']:
			if a.alleles != 'NA' and a.geneDrug == gd:

				#print a.alleles
				#print '--->6.8---'

				object_counter += 1
#				if object_counter >= object_counter_max:
#					break

				#Get clinical annotations
				clinicalAnnotations = []
				for ca in a.clinicalAnnotations.all():
					clinicalAnnotations += [(
						ca.Level_of_Evidence,
						ca.Type,
						ca.Disease,
						ca.OMB_Race,
						ca.Race_Notes,
						ca.Clinical_Annotation,
						ca.diplotype,
						)]

					object_counter += 1
					if object_counter_max > 0 and object_counter > object_counter_max:
						break

				current_gdr['alleles'] += [(
					a.alleles, 
					a.metabolizerStatusProcessed, 
					a.metabolizerStatus,
					a.recomendations,
					a.implications,
					a.phenotype,
					a.activityScore,
					a.url,
					clinicalAnnotations,
					)]

#		for t in gd.term.all():
#			if t in filtered['term']:
#				for tv in t.termValues.all():
#					if tv in filtered['termValues']:
#						for a in tv.alleles.all():
#							if a in filtered['alleles']:
#								current_gdr['terms'] += [(t.term, tv.annotation_textHtml, a.alleles)]

#		current_gdr['terms'] = sorted(current_gdr['terms'], key=lambda x:x[2])

		ret['gdr'] += [current_gdr]

	ret['counter'] = object_counter
	if object_counter_max > 0 and object_counter > object_counter_max:
		ret['success'] = False
	else:
		ret['success'] = True

	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')

def do_query(request, allowed=True, add_null_tv=False, INIT_GENE=None, INIT_ALLELES=None, genes_GET=None, drugs_GET=None, ms_GET=None, alleles_GET=None):

	ret = {'success': 'ok'}

	genes = []
	drugs = []
	ms = []
	alleles = []

	if INIT_GENE:
		genes += [INIT_GENE]

	if INIT_ALLELES:
		alleles += INIT_ALLELES

	print request.method
	if request.method == u'POST':
		POST = request.POST

		#Put in the lists (genes, drugs, ms, alleles) the data from the POST request
		#Also see: http://stackoverflow.com/questions/11190070/django-getlist 
		for l, f in ((genes, u'genes[]'), (drugs, u'drugs[]'), (ms, u'ms[]'), (alleles, u'alleles[]')):
			if POST.has_key(f):
				l += POST.getlist(f)

		print POST
	elif request.method == u'GET':
		# GET is only through the API
		genes = genes_GET
		drugs = drugs_GET
		ms = ms_GET
		alleles = alleles_GET

	filtered = filter_db(genes, drugs, ms, alleles, add_null_tv=add_null_tv, allowed=allowed)

	#print filtered['genes_names']

	ret['genes'] = filtered['genes_names']
	ret['drugs'] = filtered['drugs_names']
	ret['ms'] = filtered['ms_names']
	ret['alleles'] = filtered['alleles_names']
	ret['check_all'] = filtered['check_all']

	if request.method == u'POST':
		if POST.has_key(u'genes[]'):
			ret['genes_combo'] = POST.getlist(u'genes[]')
		else:
			ret['genes_combo'] = u'All'
		if POST.has_key(u'drugs[]'):
			ret['drugs_combo'] = POST.getlist(u'drugs[]')
		else:
			ret['drugs_combo'] = u'All'

		if POST.has_key(u'ms[]'):
			ret['ms_combo'] = POST.getlist(u'ms[]')
		else:
			ret['ms_combo'] = u'All'

		if POST.has_key(u'alleles[]'):
			ret['allele_combo'] = POST.getlist(u'alleles[]')
		else:
			ret['allele_combo'] = u'All'


	elif request.method == u'GET':
		if len(genes) > 0:
			ret['genes_combo'] = genes
		else:
			ret['genes_combo'] = u'All'

		if len(drugs) > 0:
			ret['drugs_combo'] = drugs
		else:
			ret['drugs_combo'] = u'All'

		if len(ms) > 0:
			ret['ms_combo'] = ms
		else:
			ret['ms_combo'] = u'All'

		if len(alleles) > 0:
			ret['allele_combo'] = alleles
		else:
			ret['allele_combo'] = u'All'

	return ret, filtered

def genes_from_list(genes):
	return [g for gs in genes for g in ePGA.models.Gene.objects.filter(symbol=gs)]

def drugs_from_list(drugs):
	return [rd for d in drugs for rd in ePGA.models.RelatedDrugs.objects.filter(relatedDrug=d)]

def geneDrugs_from_genes(genes):
	ret = []
	for g in genes:
		for gd in ePGA.models.GeneDrug.objects.filter(gene=g):
			ret += [gd]

	return ret

def geneDrugs_from_drugs(drugs, allowed=None):
	ret = []
	for d in drugs:
		for gd in ePGA.models.GeneDrug.objects.filter(relatedDrug=d):
			if (allowed and (gd in allowed)) or (not allowed):
				ret += [gd]

	return ret

def drugs_from_geneDrugs(geneDrugs, allowed=None):
	if allowed:
		return [gd.relatedDrug for gd in geneDrugs if gd.relatedDrug in allowed]
	else:
		return [gd.relatedDrug for gd in geneDrugs]

def genes_from_geneDrugs(geneDrugs, allowed=None):
	if allowed:
		return [gd.gene for gd in geneDrugs if gd.gene in allowed]
	else:
		return [gd.gene for gd in geneDrugs]

def term_from_geneDrugs(geneDrugs):
	ret = []
	for gd in geneDrugs:
		for t in gd.term.all():
			#if 'etabolizer' in t.term:
			#	ret += [t]
			ret += [t]

	return ret


def termValues_from_term(terms):
	ret = []
	for t in terms:
		for tv in t.termValues.all():
			ret += [tv]

	return ret

def termValues_from_alleles(alleles, allowed=None):
	ret = []
	for a in alleles:
		if allowed:
			if a.termValues in allowed:
				ret += [a.termValues]
		else:
			ret += [a.termValues]
	return ret

def terms_from_termValues(termValues, allowed=None):
	ret = []
	for tv in termValues:
		if allowed:
			if tv.term in allowed:
				ret += [tv.term]
		else:
			ret += [tv.term]

	return ret

def geneDrug_from_terms(term, allowed = None):
	ret = []

	for t in term:
		if allowed:
			if t.geneDrug in allowed:
				ret += [t.geneDrug]
		else:
			ret += [t.geneDrug]

	return ret

def geneDrugs_from_alleles(alleles, allowed = None, no_genes_objects=None, no_drugs_objects=None):
	ret = []

	for a in alleles:

		if no_genes_objects and a.geneDrug.gene in no_genes_objects:
			continue

		if no_drugs_objects and a.geneDrug.relatedDrug in no_drugs_objects:
			continue

		if allowed:
			if a.geneDrug in allowed: 
				ret += [a.geneDrug]
		else:
			ret += [a.geneDrug]

	return ret

def alleles_from_termValues(termValues, allowed = None):
	ret = []
	for t in termValues:
		for a in t.alleles.all():
			if allowed:
				if a.alleles in allowed:
					ret += [a]
			else:
				ret += [a]

	return ret


def alleles_from_geneDrugs(geneDrugs, allowed=None):
	ret = []
	for gs in geneDrugs:
		for a in gs.alleles.all():
			if allowed:
				if a in allowed:
					ret += [a]
			else:
				ret += [a]

	return ret

def filter_db(genes, drugs, ms, alleles, add_null_tv=False, start=False, allowed=False):
	'''
	ret[] contains objects
	'''

	allowed=True

	ret = {}
	#allowed = False # Restrict on previous values

	#print ' ### 1'

	no_genes = [x[1:] for x in genes if x[0] == '~']
	yes_genes = [x for x in genes if x[0] != '~']

	no_drugs = [x[1:] for x in drugs if x[0] == '~']
	yes_drugs = [x for x in drugs if x[0] != '~']

	no_ms = [x[1:] for x in ms if x[0] == '~']
	yes_ms = [x for x in ms if x[0] != '~']

	no_alleles = [x[1:] for x in alleles if x[0] == '~']
	yes_alleles = [x for x in alleles if x[0] != '~']

	#print ' ### 2'

	no_genes_objects = genes_from_list(no_genes)

	#print ' ### 2.5 '

	no_drugs_objects = drugs_from_list(no_drugs)

	#print ' ### 3'

	#Get Genes
	if yes_genes:
		ret['genes'] = genes_from_list(yes_genes)
	else:
		#Get all Genes
		ret['genes'] = []

	print ret['genes']

	#If not selection has been done, then get everything 
	if (not yes_genes) and (not yes_drugs) and (not yes_ms) and (not yes_alleles):
		ret['genes'] = ePGA.models.Gene.objects.all()
		ret['check_all'] = False # DO NOT CHECK ALL RETURNED ITEMS, WHEN NO SELECTION HAS BEEN DONE
	else:
		ret['check_all'] = True # SELECT EVERYTHING (A selection has been performed)

	#print '-->0->--', genes
	#print '-->0->--', drugs

	#Get drugs, ms and alleles FROM GENES
	#print '-->01'
	ret['geneDrugs'] = geneDrugs_from_genes(ret['genes'])
	#print '-->02'
	ret['drugs'] = drugs_from_geneDrugs(ret['geneDrugs'])
	#print '-->03'

	ret['alleles'] = alleles_from_geneDrugs(ret['geneDrugs'])

	#print '-->1->--', len(ret['drugs'])

	#Filter on drugs
	if drugs:

		#Fix correct drug_names and drugs variables
		
		#drug_names = [d.relatedDrug for d in ret['drugs']]
		#drugs = yes_drugs + [x for x in drug_names if x not in no_drugs]
		#if not drug_names:
		#	drug_names = drugs

		drug_names = drugs
		#print '--->1.3->---', len(drug_names), drug_names
		#print '--->1.4->---', drugs
		#print '--> 1.42 gene drugs ->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))

		if allowed:
			ret['drugs'] = [ePGA.models.RelatedDrugs.objects.get(relatedDrug=x) for x in drugs if x in drug_names]
			#print '--->1.45 drugs->---', len(ret['drugs'])
			ret['geneDrugs'] = geneDrugs_from_drugs(ret['drugs'], allowed=ret['geneDrugs'])
			#print '--> 1.46 gene drugs ->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))
			#for jj in ret['geneDrugs']:
				#print '-----------'
				#print jj
				#print 'drug:', jj.relatedDrug.relatedDrug
				#print 'gene:', jj.gene.symbol
				#print 'source:', jj.source

			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'], allowed=ret['genes'])
			#print '--> 1.47 genes ->--', len(ret['genes']), 'Unique:', len(set(ret['genes']))
		else:
			ret['drugs'] += [ePGA.models.RelatedDrugs.objects.get(relatedDrug=x) for x in drugs if x not in drug_names]
			ret['geneDrugs'] = geneDrugs_from_drugs(ret['drugs'])
			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'])
		#ret['term'] = term_from_geneDrugs(ret['geneDrugs'])
		#ret['termValues'] = termValues_from_term(ret['term'])
		#ret['alleles'] = alleles_from_termValues(ret['termValues'])
		ret['alleles'] = alleles_from_geneDrugs(ret['geneDrugs'])

		#print '--> 1.5 gene drugs ->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))

	#print '-->2->--', len(ret['drugs'])

	#Filter on TermValues
	if ms:

		#Search is done based on alleles
		if not ret['alleles']:
			#Get all alleles
			ret['alleles'] = ePGA.models.Alleles.objects.all()


		new_alleles = []
		for x in ret['alleles']:
			if yes_ms and x.metabolizerStatusProcessed not in yes_ms:
				continue
			if no_ms and x.metabolizerStatusProcessed in no_ms:
				continue

			new_alleles += [x]
		ret['alleles'] = new_alleles

		#print '--->2 Alleles:->--', len(ret['alleles'])
		#print '--> 2.1 gene drugs ->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))

		if allowed:
			ret['geneDrugs'] = geneDrugs_from_alleles(ret['alleles'], ret['geneDrugs'], no_genes_objects=no_genes_objects, no_drugs_objects=no_drugs_objects)
			ret['drugs'] = drugs_from_geneDrugs(ret['geneDrugs'], ret['drugs'])
			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'], ret['genes'])
		else:
			ret['geneDrugs'] = geneDrugs_from_alleles(ret['alleles'])
			ret['drugs'] = drugs_from_geneDrugs(ret['geneDrugs'])
			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'])

		#print '--> 2.2 gene drugs ->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))

	#print '-->2.5 drugs lengths->--', len(ret['drugs'])
	#print '-->2.55 alleles lengths->--', len(ret['alleles'])

	#Filter on Alleles
	if alleles:

		#Search is done based on alleles
		if not ret['alleles']:
			#Get all alleles
			ret['alleles'] = ePGA.models.Alleles.objects.all()

		#print '-->2.57 alleles lengths->--', len(ret['alleles'])
		#print '--> yes alleles:', yes_alleles
		#print '--> no alleles:', no_alleles
		new_alleles = []
		for x in ret['alleles']:
			if yes_alleles and x.alleles not in yes_alleles:
				continue
			if no_alleles and x.alleles in no_alleles:
				continue

			if x not in new_alleles:
				new_alleles += [x]

		ret['alleles'] = new_alleles

		#print '-->2.6 alleles length->--', len(ret['alleles'])

		if allowed:
			ret['geneDrugs'] = geneDrugs_from_alleles(ret['alleles'], ret['geneDrugs'], no_genes_objects=no_genes_objects, no_drugs_objects=no_drugs_objects)
			ret['drugs'] = drugs_from_geneDrugs(ret['geneDrugs'], ret['drugs'])
			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'], ret['genes'])
		else:
			ret['geneDrugs'] = geneDrugs_from_alleles(ret['alleles'])
			ret['drugs'] = drugs_from_geneDrugs(ret['geneDrugs'])
			ret['genes'] = genes_from_geneDrugs(ret['geneDrugs'])

	#print '-->3- len drugs>--', len(ret['drugs'])

		
	#Get unuque values
	ret['genes_names'] = sorted(list(set([x.symbol for x in ret['genes']])))
	ret['drugs_names'] = sorted(list(set([x.relatedDrug for x in ret['drugs']])))
	ret['ms_names'] =  list(set([x.metabolizerStatusProcessed for x in ret['alleles'] if x.metabolizerStatusProcessed != '']))
#	ret['ms_names'] = ['All'] + list(set([x.annotation_processed for x in ret['termValues'] if x.term.term == u'Metabolizer Status']))
	ret['alleles_names']  = sorted(list(set([x.alleles for x in ret['alleles']])))

	#print '-->3.5 >--START-'
	#print [x.alleles for x in ret['alleles']]
	#print '-->3.5 >--END---'
	#print ret['alleles_names']
	#print '-->3.5 >---SET--'

	#print '--> drugs 4->--', len(ret['drugs']), 'Unique:', len(ret['drugs_names'])
	#print '--> gene drugs 5->--', len(ret['geneDrugs']), 'Unique:', len(set(ret['geneDrugs']))

	return ret

# https://docs.djangoproject.com/en/dev/topics/http/file-uploads/
def upload_file(request):
	


	ret = {}
	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')

def process_INIT_GENE_ALLELES(INIT_GENE, INIT_ALLELES):

	# For unicode see : http://stackoverflow.com/questions/16566069/url-decode-utf-8-in-python 
	# Use: urlencode . Join with '&'
	# example 1 : http://0.0.0.0:8080/dosing/explore/ABCB1/%2A1%26%2A1/ 
	# example 2 : http://0.0.0.0:8080/dosing/explore/ABCC2/H1%26H13/ 
	if INIT_GENE:
		ret_INIT_GENE = urllib.unquote(INIT_GENE)
		print INIT_GENE
	else:
		ret_INIT_GENE = None
	if INIT_ALLELES:
		ret_INIT_ALLELES = [x.replace('&', '/') for x in urllib.unquote(INIT_ALLELES).split(',')]
	else:
		ret_INIT_ALLELES = None

	return ret_INIT_GENE, ret_INIT_ALLELES


def fetch_init_json(request, INIT_GENE=None, INIT_ALLELES=None):
	'''
	7 October 2014 
	INIT_GENE and INIT_ALLELES are data specified in url 
	http://www.epga.gr/explore/fetch_init_json

	http://www.epga.gr/explore/recommendations/
	data = 'genes%5B%5D=ABCA1&drugs%5B%5D=atorvastatin%2C+pravastatin%2C+simvastatin&drugs%5B%5D=fenofibrate&drugs%5B%5D=pravastatin&ms%5B%5D=Unknown&alleles%5B%5D=rs12003906&alleles%5B%5D=rs2230806&alleles%5B%5D=rs2230808&csrfmiddlewaretoken=kkqGCbskNs13gjrqZeXhxr7w2x6mCMmg'

curl 'http://www.epga.gr/explore/recommendations/' -H 'Host: www.epga.gr' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:42.0) Gecko/20100101 Firefox/42.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: http://www.epga.gr/explore/' -H 'Cookie: csrftoken=kkqGCbskNs13gjrqZeXhxr7w2x6mCMmg; _ga=GA1.2.340092060.1441876954' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data 'genes%5B%5D=ABCA1&drugs%5B%5D=atorvastatin%2C+pravastatin%2C+simvastatin&drugs%5B%5D=fenofibrate&drugs%5B%5D=pravastatin&ms%5B%5D=Unknown&alleles%5B%5D=rs12003906&alleles%5B%5D=rs2230806&alleles%5B%5D=rs2230808&csrfmiddlewaretoken=kkqGCbskNs13gjrqZeXhxr7w2x6mCMmg'

	data = 'genes%5B%5D=ABCA1&drugs%5B%5D=atorvastatin%2C+pravastatin%2C+simvastatin&drugs%5B%5D=fenofibrate&drugs%5B%5D=pravastatin&ms%5B%5D=Unknown&alleles%5B%5D=rs12003906&alleles%5B%5D=rs2230806&alleles%5B%5D=rs2230808&csrfmiddlewaretoken=kkqGCbskNs13gjrqZeXhxr7w2x6mCMmg'
	headers = {'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.5', 'Pragma': 'no-cache', 'Referer': 'http://www.epga.gr/explore/', 'Cookie': 'csrftoken=kkqGCbskNs13gjrqZeXhxr7w2x6mCMmg; _ga=GA1.2.340092060.1441876954', 'X-Requested-With': 'XMLHttpRequest', 'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:42.0) Gecko/20100101 Firefox/42.0'}
	import requests
	r = requests.post(url, data=data2, headers=headers)
	print(r.text)
	'''

	INIT_GENE, INIT_ALLELES = process_INIT_GENE_ALLELES(INIT_GENE, INIT_ALLELES)

	test_ret = {
		'gene_1' : {
			'drug_1' : { 
				'alleles' : ['al_1', 'al_2', 'al_3'],
				'MSP'     : ['', 'Intermediate', '']
			},
			'drug_2' : { 
				'alleles' : ['al_2', 'al_3', 'al_4'],
				'MSP'     : ['Poor', '', 'Ultra']
			}
		},
		'gene_2' : {
			'drug_2' : { 
				'alleles' : ['al_3', 'al_4', 'al_5'],
				'MSP'     : ['', 'Intermediate', '']
			},
			'drug_3' : { 
				'alleles' : ['al_4', 'al_5', 'al_6'],
				'MSP'     : ['Poor', '', 'Ultra']
			}
		}
	}


	ret = {}

	for gd in ePGA.models.GeneDrug.objects.all():
		g = gd.gene
		rd = gd.relatedDrug
		g_symbol = g.symbol

		#Check connection with Tzenni's translation
		if INIT_GENE:
			if g_symbol not in INIT_GENE:
				continue

		rd_relatedDrug = rd.relatedDrug

		#print g_symbol, rd_relatedDrug

		if g_symbol not in ret:
			ret[g_symbol] = {}

		if rd_relatedDrug not in ret[g_symbol]:
			ret[g_symbol][rd_relatedDrug] = {'alleles' : [], 'MSP' : []}

#		print 'ret1'
#		print ret

		all_al = gd.alleles.all()

		for al in all_al:
			alleles = al.alleles
			msp = al.metabolizerStatusProcessed
			if alleles not in ret[g_symbol][rd_relatedDrug]['alleles']:

				#Check connection with Tzenni's translation 
				if INIT_ALLELES:
					if alleles not in INIT_ALLELES:
						continue

				ret[g_symbol][rd_relatedDrug]['alleles'] += [alleles]
				ret[g_symbol][rd_relatedDrug]['MSP'] += [msp]

#		if not ret[g_symbol][rd_relatedDrug]['alleles']:
#			del ret[g_symbol][rd_relatedDrug]

#	print 'ret2'
#	print ret

	#Ordering..
	#Sorting gene names
	ret_ordered = OrderedDict(sorted(ret.items(), key=lambda t: t[0]))
	for g in ret_ordered:
		#Sorting drug names
		ret_ordered[g] = OrderedDict(sorted(ret_ordered[g].items(), key=lambda t: t[0]))
		for f in ret_ordered[g]:
			#Sorting alleles 
			zipped = zip(ret_ordered[g][f]['alleles'], ret_ordered[g][f]['MSP'])
			zipped_sorted = sorted(zipped, key=lambda x : x[0])
			ret_ordered[g][f]['alleles'] = [x[0] for x in zipped_sorted]
			ret_ordered[g][f]['MSP'] = [x[1] for x in zipped_sorted]

	#Save
	#d = '\n'.join(['\t'.join(x2) for x2 in sorted(list(set([xxxxx for xxxx in [[(x, xxx) for xxx in xx['alleles'] for xx in y.values()] for x,y in ret_ordered.iteritems()] for xxxxx in xxxx])), key=lambda x:str(x[0]) + '__' + str(x[1]))])

	#json = simplejson.dumps(ret)
	json = simplejson.dumps(ret_ordered)
	#json = simplejson.dumps(test_ret)
	#print json
	#with open('tzenh_7_aug_2015.txt', 'w') as f:
	#	f.write(json + '\n')


	return HttpResponse(json, content_type='application/json')

def fetch_init_json_filtering(old_data, gene_filter, drug_filter, ms_filter, alleles_filter):
	'''
	emulate the function get_fields(component) from emodia.js
	'''

	new_data = {}

	if gene_filter:
		for gene_checked in gene_filter:
			if gene_checked in old_data:
				new_data[gene_checked] = old_data[gene_checked]

	elif drug_filter:
		for g in old_data:
			for d in old_data[g]:
				if d in drug_filter:
					if g not in new_data:
						new_data[g] = {}
					if d not in new_data[g]:
						new_data[g][d] = old_data[g][d]

	elif ms_filter:
		for g in old_data:
			for d in old_data[g]:
				for a_index, a in enumerate(old_data[g][d]['alleles']):
					ms = old_data[g][d]['MSP'][a_index]
					if ms in ms_filter:
						if g not in new_data:
							new_data[g] = {}
						if d not in new_data[g]:
							new_data[g][d] = {'alleles' : [], 'MSP' : []}

						new_data[g][d]['alleles'] += [a]
						new_data[g][d]['MSP'] += [ms]


	elif alleles_filter:
		for g in old_data:
			for d in old_data[g]:
				for a_index, a in enumerate(old_data[g][d]['alleles']):
					ms = old_data[g][d]['MSP'][a_index]
					if a in alleles_filter:
						if g not in new_data:
							new_data[g] = {}
						if d not in new_data[g]:
							new_data[g][d] = {'alleles' : [], 'MSP' : []}

						new_data[g][d]['alleles'] += [a]
						new_data[g][d]['MSP'] += [ms]


	return new_data

def get_genes_old(request):

	ret = {'results' : []}

	if request.method == u'GET':
		GET = request.GET

		if GET.has_key(u'drugs'):
			all_drugs = [x.strip() for x in GET[u'drugs'].split(',')]

			all_genes_found = []
			for drug in all_drugs:
				try:

					drug_found = RelatedDrugs.objects.get(relatedDrug=drug)

					all_dosing = Dosing.objects.filter(relatedDrug=drug_found)
					all_genes_found += list(set([x.gene.symbol for x in all_dosing]))

				except ObjectDoesNotExist:
					pass
			ret = {'results' : list(set(all_genes_found))}


	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')

def get_genes(request):

	return get_all_objects(request, u'drugs', RelatedDrugs, "relatedDrug", "relatedDrug", 'gene.symbol')

def get_drugs(request):
	return get_all_objects(request, u'genes', Gene, 'symbol', 'gene', 'relatedDrug.relatedDrug')

def get_all_objects(request, field_name, Search_Class, Class_field, Dosing_field, selector):
	ret = {'results' : []}

	if request.method == u'GET':
		GET = request.GET

		if GET.has_key(field_name):
			all_items = [x.strip() for x in GET[field_name].split(',')]

			all_items_found = []
			for item in all_items:
				try:
					item_found = Search_Class.objects.get(**{Class_field:item})
					all_dosing = Dosing.objects.filter(**{Dosing_field:item_found})

					if selector == 'gene.symbol':
						all_items_found += list(set([x.gene.symbol for x in all_dosing]))
					elif selector == 'relatedDrug.relatedDrug':
						all_items_found += list(set([x.relatedDrug.relatedDrug for x in all_dosing]))

				except ObjectDoesNotExist:
					pass
			ret = {'results' : list(set(all_items_found))}
			#print ret


	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')

def get_drug(drug):

	found = None
	try:
		found = RelatedDrugs.objects.get(relatedDrug = drug)
	except ObjectDoesNotExist:
		pass

	return found


def get_gene(gene):

	found = None
	try:
		found = Gene.objects.get(symbol = gene)
	except ObjectDoesNotExist:
		pass

	return found


def get_phenotypes(request):
	ret = {'results' : []}

	print 1

	if request.method == u'GET':
		GET = request.GET

		print 2

		all_drugs = []
		if GET.has_key(u'drugs'):
			all_items = [x.strip() for x in GET[u'drugs'].split(',')]

			all_drugs = [y for y in [get_drug(x) for x in all_items] if y]

			print 3

		all_genes = []
		if GET.has_key(u'genes'):
			all_items = [x.strip() for x in GET[u'genes'].split(',')]

			all_genes = [y for y in [get_gene(x) for x in all_items] if y]

			print 4

		for d, g in itertools.product(all_drugs, all_genes):

			ret['results'] += list(set([x.term for x in Dosing.objects.filter(relatedDrug=d, gene=g)]))

			print 5

	json = simplejson.dumps(ret)
	return HttpResponse(json, content_type='application/json')	

def test_jquery(request):

	results = {'success':2}

	if request.method == u'GET':
		GET = request.GET
		if GET.has_key(u'pk'):
			results = {'success' : int(GET[u'pk']) + 1}

	json = simplejson.dumps(results)
	return HttpResponse(json, content_type='application/json')
