	var data = {}; 

	var colors = {};

	//Remove colors https://github.com/kantale/emodia/issues/55 
	colors["Intermediate Metabolizer"] = "WhiteSmoke"; // "orange";
	colors["Poor Metabolizer"] = "WhiteSmoke";// "OrangeRed";
	colors["Extensive Metabolizer"] = "WhiteSmoke";// "OliveDrab";
	colors["Ultrarapid Metabolizer"] = "WhiteSmoke";// "PaleGoldenRod";
	colors["Unknown"] = "WhiteSmoke";

	//Takes json data and places them in the combo boxes 
	function convert_json_to_select(some_data, first) {

		var gene_select = "";
		var drug_select = "";
		var MSP_select = "";
		var al_select = "";
		var alleles_in = [];
		var MSP_in = [];

		var different_genes = [];
		var different_drugs = [];
		var different_ms = [];
		var different_alleles = [];

		for (var g in some_data) {
			gene_select += "<option value=\"" + g + "\">" + g + "</option>\n";

			drug_select += "<optgroup label=\"" + g + "\">\n";
			al_select += "<optgroup label=\"" + g + "\">\n";

			var different_genes_index = different_genes.indexOf(g);
			if (different_genes_index == -1) {
				different_genes.push(g);
			}

			for (var d in some_data[g]) {
				//drug_select += "<option value=\"" + g + '__' + d + "\">" + d + "</option>\n";
				drug_select += "<option value=\"" + Math.random().toString(36).substring(7) + "\">" + d + "</option>\n";

				var different_drugs_index = different_drugs.indexOf(d);
				if (different_drugs_index == -1) {
					different_drugs.push(d);
				}

				for (var a in some_data[g][d]['alleles']) {
					var al_name = some_data[g][d]['alleles'][a];

					var different_alleles_index = different_alleles.indexOf(al_name);
					if (different_alleles_index == -1) {
						different_alleles.push(al_name);
					}

					var gene_allele = g + '__' + al_name;
					var alleles_in_index = alleles_in.indexOf(gene_allele);
					if (alleles_in_index == -1) {
						//al_select += "<option value=\"" + g + '__' + al_name + "\">" + al_name + "</option>\n";
						al_select += "<option value=\"" + Math.random().toString(36).substring(7) + "\">" + al_name + "</option>\n";
						alleles_in.push(gene_allele);
					}

					var MSP_name = some_data[g][d]['MSP'][a];
					if (MSP_name) {

						var different_ms_index = different_ms.indexOf(MSP_name);
						if (different_ms_index == -1) {
							different_ms.push(MSP_name);
						}

						var MSP_in_index = MSP_in.indexOf(MSP_name);
						if (MSP_in_index == -1) {
							MSP_select += "<option value=\"" + MSP_name + "\">" + MSP_name + "</option>\n";
							MSP_in.push(MSP_name);
						}
					}
				}
			}
			drug_select += "</optgroup>\n";
			al_select += "</optgroup>\n";

		}

		$("#input_genes_id")[0].innerHTML = gene_select;
        $("#input_genes_id").multiselect("refresh");

        $("#input_drugs_id")[0].innerHTML = drug_select;
        $("#input_drugs_id").multiselect("refresh");

        $("#combo_ms_id")[0].innerHTML = MSP_select;
        $("#combo_ms_id").multiselect("refresh");

        $("#combo_alleles_id")[0].innerHTML = al_select;
        $("#combo_alleles_id").multiselect("refresh");
		

		if (first) {
			$("#input_genes_id").multiselect("uncheckAll");
			$("#input_drugs_id").multiselect("uncheckAll");
			$("#combo_ms_id").multiselect("uncheckAll");
			$("#combo_alleles_id").multiselect("uncheckAll");
		}
		else {
			$("#input_genes_id").multiselect("checkAll");
			$("#input_drugs_id").multiselect("checkAll");
			$("#combo_ms_id").multiselect("checkAll");
			$("#combo_alleles_id").multiselect("checkAll");
		}

		$("#gene_number_id")[0].innerHTML = different_genes.length;
		$("#drug_number_id")[0].innerHTML = different_drugs.length;
		$("#ms_number_id")[0].innerHTML = different_ms.length;
		$("#allele_number_id")[0].innerHTML = different_alleles.length;

		//http://stackoverflow.com/questions/5773073/using-jquery-ui-setting-width-on-a-particular-multiselect-box 
		$('.ui-multiselect').css('width', '400px');

        //console.log(al_select);
        //console.log(alleles_in);
	}

	//Called when a combo box is closed
	//It does not perform any AJAX call! Everything is done via javasript  
	//Creates new data json 
	function get_fields(component, new_data_argument) {
		//alert('close');

		if (typeof new_data_argument === 'number') {
			var new_data = {};
		}
		else {
			//Clone new_data_argument  http://stackoverflow.com/questions/122102/what-is-the-most-efficient-way-to-clone-an-object/5344074#5344074 
			//var new_data = jQuery.extend(true, {}, new_data_argument);
			var new_data = {};
		}

		//Filter on genes
		if (component == "input_genes_id") {
			var genes_checked = $("#input_genes_id").multiselect("getChecked");

			for (var genes_checked_ind in genes_checked) {
				var value_checked = genes_checked[genes_checked_ind].value;
				//var value_checked = genes_checked[genes_checked_ind].innerText;
				if (data[value_checked]) {
					new_data[value_checked] = data[value_checked];
				}
			}

			//Update UI?
			if (typeof new_data_argument === 'number') {
				if (Object.keys(new_data).length > 0) {
					convert_json_to_select(new_data, false);
				}
				else {
					location.reload();
				}
			}
		}

		else if (component == 'input_drugs_id') {

			//Take the values of all selected drugs
			var drugs_checked = $("#input_drugs_id").multiselect("getChecked");
			var drugs_checked_values = [];

			for (var drugs_checked_ind in drugs_checked) {
				//var drug_checked_value = drugs_checked[drugs_checked_ind].value;
				var drug_checked_value = drugs_checked[drugs_checked_ind].title;
				//console.log(drug_checked_value);
				if (!drug_checked_value) {
					continue;
				}
				//drug_checked_value = drug_checked_value.split('__')[1];
				//var drug_checked_value = drugs_checked[drugs_checked_ind].textContent;

				//Check if it is already in the drugs_checked_value array
				var drugs_checked_values_ind = drugs_checked_values.indexOf(drug_checked_value);

				if (drugs_checked_values_ind == -1) {
					if (drug_checked_value) { //Remove undefined
						drugs_checked_values.push(drug_checked_value);
					}
				}
			}

			//console.log(drugs_checked_values);

			for (var gene in data) {
				for (var drug in data[gene]) {
					//var gene_drug = gene + '__' + drug;
					//var drugs_checked_values_ind = drugs_checked_values.indexOf(gene_drug);
					var drugs_checked_values_ind = drugs_checked_values.indexOf(drug);
					if (drugs_checked_values_ind > -1) {
						if (!(gene in new_data)) {
							new_data[gene] = {};
						}
						new_data[gene][drug] = data[gene][drug];
					} 
				}
			}

			//Update UI?
			if (typeof new_data_argument === 'number') {
				if (Object.keys(new_data).length > 0) {
					convert_json_to_select(new_data, false);
				}
				else {
					location.reload();
				}
			}
		}

		else if (component == "combo_ms_id") {


			//Take the values of all checked 
			var MSP_checked = $("#combo_ms_id").multiselect("getChecked");
			var MSP_checked_values = []; //Take all different checked values

			for (var MSP_checked_ind in MSP_checked) {
				var MSP_checked_value = MSP_checked[MSP_checked_ind].value;
				if (!MSP_checked_value) {
					continue;
				}

				//Check if it is already in the ms_checked_value array
				var MSP_checked_values_ind = MSP_checked_values.indexOf(MSP_checked_value);

				if (MSP_checked_values_ind == -1) {
					if (MSP_checked_value) { //Remove undefined
						MSP_checked_values.push(MSP_checked_value);
					}
				}
			}

			//console.log(MSP_checked_values);

			for (var gene in data) {
				for (var drug in data[gene]) {

					//console.log(data[gene][drug]["alleles"]);

					for (var allele_ind in data[gene][drug]["alleles"]) {
						var allele = data[gene][drug]["alleles"][allele_ind];
						var MSP = data[gene][drug]["MSP"][allele_ind];

						//console.log('111')
						//console.log(MSP);
						//console.log(allele);

						if (!MSP) {
							//onsole.log('AAA');
							continue;
						}

						var MSP_checked_ind = MSP_checked_values.indexOf(MSP);
						if (MSP_checked_ind > -1) {
							if (!(gene in new_data)) {
								new_data[gene] = {};
							}
							if (!(drug in new_data[gene])) {
								new_data[gene][drug] = {"alleles" : [], "MSP" : []};
							}

							//Check if the pair (allele, MSP) exists in new_data[gene][drug]
							exists = false;
							for (var new_allele_ind in new_data[gene][drug]["alleles"]) {
								if (new_data[gene][drug]["alleles"][new_allele_ind]==allele && new_data[gene][drug]["MSP"][new_allele_ind]==MSP) {
									exists = true;
									break;
								}
							}
							if (!exists) {
								//It does not exist. Insert it.
								new_data[gene][drug]["alleles"].push(allele);
								new_data[gene][drug]["MSP"].push(MSP);
							}


							//var new_data_index = new_data[gene][drug]["MSP"].indexOf(MSP);
							//if (new_data_index == -1) {
							//	new_data[gene][drug]["alleles"].push(allele);
							//	new_data[gene][drug]["MSP"].push(MSP);
							//} 
						}
					}
				}
			}

			//Update UI ? 
			if (typeof new_data_argument === 'number') {
				if (Object.keys(new_data).length > 0) {
					convert_json_to_select(new_data, false);
				}
				else {
					location.reload();
				}
			}
		}

		else if (component == "combo_alleles_id") {
			//Take the values of all selected drugs
			var alleles_checked = $("#combo_alleles_id").multiselect("getChecked");
			var alleles_checked_values = [];

			for (var alleles_checked_ind in alleles_checked) {
				//var alleles_checked_value = alleles_checked[alleles_checked_ind].value;
				var alleles_checked_value = alleles_checked[alleles_checked_ind].title;
				if (!alleles_checked_value) {
					continue;
				}
				//alleles_checked_value = alleles_checked_value.split('__')[1];

				//Check if it is already in the alleles_checked_value array
				var alleles_checked_values_ind = alleles_checked_values.indexOf(alleles_checked_value);

				if (alleles_checked_values_ind == -1) {
					if (alleles_checked_value) { //Remove undefined
						alleles_checked_values.push(alleles_checked_value);
					}
				}
			}

			//console.log(drugs_checked_values);

			for (var gene in data) {
				for (var drug in data[gene]) {

					for (var allele_ind in data[gene][drug]["alleles"]) {
						var allele = data[gene][drug]["alleles"][allele_ind];
						var MSP = data[gene][drug]["MSP"][allele_ind];

						var alleles_checked_ind = alleles_checked_values.indexOf(allele);
						if (alleles_checked_ind > -1) {
							if (!(gene in new_data)) {
								new_data[gene] = {};
							}
							if (!(drug in new_data[gene])) {
								new_data[gene][drug] = {"alleles" : [], "MSP" : []};
							}

							var new_data_index = new_data[gene][drug]["alleles"].indexOf(allele);
							if (new_data_index == -1) {
								new_data[gene][drug]["alleles"].push(allele);
								new_data[gene][drug]["MSP"].push(MSP);
							} 
						}
					}
				}
			}

			//Update UI?
			if (typeof new_data_argument === 'number') {
				//console.log(Object.keys(new_data).length);
				if (Object.keys(new_data).length > 0) {
					convert_json_to_select(new_data, false);
				}
				else {
					location.reload();
				}
			}
		}

		//console.log(new_data);

		//Update data?
		if (typeof new_data_argument === 'number') {
			data = new_data;
		}
		else {
			return new_data;
		}

	}

	function after_load() {

		//Some basic setups 
		$("#button_clear_id")[0].onclick = function() {
  			location.reload(); //Reload page
  		};


  		// RECOMMENDATIONS BUTTON START. Show recommendations button 
  		$("#button_recommendations_id")[0].onclick = function() {

			//$("#button_recommendations_id")[0].prop("disabled", true);

			$("#recommendations_id")[0].innerHTML = '<h3>Please Wait..</h3>'

			$("#button_recommendations_id")[0].disabled = true;

			function jtree_modal(current_node, longtext, name, lttitle) {

			//Check if the textHTML is too big to show in the tree
				if (longtext.length > 100) {
					current_node['children'].push({
						'state' : { 'opened' : false, 'selected' : false },
						'text' : '<b>' + name + ': </b>' + longtext.replace("<p>", "").substring(0,50) + '..<font color="red">(Click to show full text)</font>',
						'longtext' : longtext,
						'lttitle' : lttitle
					});
				}
				else {
					current_node['children'].push('<b>' + name + ': </b>' + longtext.replace("</p>", "").replace("<p>", ""));	
				}
			}

			json_d = {
			//genes : $("#input_genes_id").data('info'),
			genes : $("#input_genes_id").multiselect("getChecked").map(function(){return this.value;}).get(),

			//drugs : $("#input_drugs_id").data('info'),
			drugs : $("#input_drugs_id").multiselect("getChecked").map(function(){return this.title;}).get(),

			//ms : $("#combo_ms_id").data('info'),
			ms : $("#combo_ms_id").multiselect("getChecked").map(function(){return this.title;}).get(),

			//alleles : $("#combo_alleles_id").data('info'),
			alleles : $("#combo_alleles_id").multiselect("getChecked").map(function(){return this.title;}).get(),

			csrfmiddlewaretoken : init_translation['csrfmiddlewaretoken']
			};
		
			//$.getJSON(
			$.post(
				"recommendations/",
				json_d,
				function(json, textStatus) {
				
					if (json['success'] == false) {
						$("#recommendations_id")[0].innerHTML = '<strong>Too many results. Please refine your query. Results:' + json['counter'] + '</strong>';
					}

					else { 
						// new_HTML = '<strong>Results:' + json['counter'] + '</strong></p>\n';

						//console.log(json);

						json_tree = [];
						colored_nodes = [];

						for (var x in json['gdr']) {
							current_node = {};
							current_node_name = json['gdr'][x]['symbol'] + ' - ' + json['gdr'][x]['relatedDrug'] + '  (' + json['gdr'][x]['source'] + ')';
							current_node['id'] = current_node_name;
							current_node['text'] = current_node_name;
							current_node['state'] = { 'opened' : false, 'selected' : false };
							current_node['children'] = [];
						

							//new_HTML += '<strong>' + json['gdr'][x]['symbol'] + ' --> ' + json['gdr'][x]['relatedDrug'] + '</strong></p>\n';
							//new_HTML += '<b>Source: </b>' + json['gdr'][x]['source'] + '</p>\n';
							//new_HTML += '<b>Summary: </b>' + json['gdr'][x]['summaryHTML'] + '</p>\n';
							//new_HTML += '<b>Text: </b>' + json['gdr'][x]['textHTML'] + '</p>\n';

							current_node['children'].push('<b>Source: </b>' + json['gdr'][x]['source']);
							
							if (json['gdr'][x]['source'] != 'Clinical Annotation') {
								//current_node['children'].push('Summary: ' + json['gdr'][x]['summaryHTML'].replace('</p>', '').replace('<p>', ''));
								jtree_modal(current_node, json['gdr'][x]['summaryHTML'].replace('</p>', '').replace('<p>', ''), 'Summary', current_node_name);

								//Check if the textHTML is too big to show in the tree
								//jtree_modal(current_node, json['gdr'][x]['textHTML'].replace('</p>', '').replace('<p>', '').replace('</div>', '').replace('<div style="color: red;">', ''), 'Details', current_node_name);
								current_node['children'].push('<a href="' + json['gdr'][x]['url'] + '"><b>Guideline</b></a>' );
								//console.log(json['gdr'][x]['textHTML']);
								//console.log('------------');
								//console.log(json['gdr'][x]['textHTML'].replace('</p>', '').replace('<p>', ''));
							}

							current_node_alleles = {};
							current_node_alleles['id'] = current_node_name + '_alleles';
							current_node_alleles['text'] = 'Variations';

							//https://github.com/kantale/emodia/issues/55 
							if (json['gdr'][x]['source'] != 'Clinical Annotation') {
								current_node_alleles['text'] += ' (click link and select diplotype)';
							}
							current_node_alleles['state'] = { 'opened' : false, 'selected' : false };
							current_node_alleles['children'] = [];

							for (var y in json['gdr'][x]['alleles']) {

								current_node_alleles_alleles = {};
								var current_node_alleles_alleles_url = '';
								current_node_alleles_alleles['id'] = Math.random().toString(36).substring(7);
								//current_node_alleles_alleles['id'] = current_node_name + '_alleles_' + json['gdr'][x]['alleles'][y][0];
								//current_node_alleles_alleles['id'] = current_node_alleles_alleles['id'].replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_').replace('*', 'STAR').replace('#', 'SHARP').replace('/', 'SLASH');
								//current_node_alleles_alleles['text'] = '<span class="changecolor"><b>Allele: </b>' + json['gdr'][x]['alleles'][y][0] + "</span>";
								//current_node_alleles_alleles['text'] = '<span class="changecolor"><b>Allele: </b>' + json['gdr'][x]['alleles'][y][0] + "</span> <a href='" + json['gdr'][x]['alleles'][y][7] + "'>Link</a>";
								//current_node_alleles_alleles['text'] = '<span class="changecolor"><b>Allele: </b>' + "<a href='" + json['gdr'][x]['alleles'][y][7] + "'>" + json['gdr'][x]['alleles'][y][0] + "</a></span>";
								//console.log(json['gdr'][x]['alleles'][y][1]);
								//current_node_alleles_alleles['text'] = '<span class="changecolor' + colors[json['gdr'][x]['alleles'][y][1]] + '"><b>Variation: </b>' + "<a href='" + json['gdr'][x]['alleles'][y][7] + "'>" + json['gdr'][x]['alleles'][y][0] + "</a></span>";
		
								//Commented because: https://github.com/kantale/emodia/issues/55 
								//In case of dosing guideline add guideline link, in case of clinical annotation add variant link

								//Regarding link in leaf.
								//JSTree reverses font color upon hovering. This is ugly when we set a light background color exclusively. 
								//One way to get over this is to make the text in background color a link. The href here is not the one that is followed (see a_attr)
								if (json['gdr'][x]['source'] == 'Clinical Annotation') {
									current_node_alleles_alleles_url = json['gdr'][x]['alleles'][y][7];
									current_node_alleles_alleles['text'] = '<b>Variation: </b>' + '<a href="' + current_node_alleles_alleles_url + '"><span class="changecolor' + colors[json['gdr'][x]['alleles'][y][1]] + '">' + json['gdr'][x]['alleles'][y][0] + "</span></a>";
									
								}
								else {
									current_node_alleles_alleles_url = json['gdr'][x]['url'];
									current_node_alleles_alleles['text'] = '<b>Variation: </b>' + '<a href="' + current_node_alleles_alleles_url + '"><span class="changecolor' + colors[json['gdr'][x]['alleles'][y][1]] + '">' + json['gdr'][x]['alleles'][y][0] + "</span></a>";
									
								}
				
								current_node_name_alleles = current_node_name + ' - ' + json['gdr'][x]['alleles'][y][0];
								current_node_alleles_alleles['state'] = { 'opened' : false, 'selected' : false };
								current_node_alleles_alleles['children'] = [];
								current_node_alleles_alleles['a_attr'] = { 'href' : current_node_alleles_alleles_url, 'target': '_blank' }; 

								//current_node_alleles_alleles['children'].push('<b>Diplotype: </b>' + json['gdr'][x]['alleles'][y][0]);
								//new_HTML += '----> <b>Diplotype: </b>' + json['gdr'][x]['alleles'][y][0] + '</p>\n';

								if (false) {
									if (json['gdr'][x]['alleles'][y][1]) {
										current_node_alleles_alleles['children'].push('<b>Metabolizer Status Processed: </b>' + json['gdr'][x]['alleles'][y][1]);
										//new_HTML += '----> <b>Metabolizer Status Processed: </b>' + json['gdr'][x]['alleles'][y][1] + '</p>\n';

										//console.log(' color:->' + json['gdr'][x]['alleles'][y][1] + '<--');
										if (json['gdr'][x]['alleles'][y][1] == 'Intermediate ') {
											colored_nodes.push([current_node_alleles_alleles['id'], 'orange']);
											//console.log('   Entered');
										}
										else if (json['gdr'][x]['alleles'][y][1] == 'Poor ') {
											//colored_nodes.push([current_node_alleles_alleles['id'], 'red']);
											colored_nodes.push([current_node_alleles_alleles['id'], 'OrangeRed ']);
											//console.log('   Entered');
										}
										else if (json['gdr'][x]['alleles'][y][1] == 'Extensive ') {
											//colored_nodes.push([current_node_alleles_alleles['id'], 'green']);
											colored_nodes.push([current_node_alleles_alleles['id'], 'OliveDrab']);
											//console.log('   Entered');
										}
										else if (json['gdr'][x]['alleles'][y][1] == 'Ultrarapid ') {
											//colored_nodes.push([current_node_alleles_alleles['id'], 'gray']);
											colored_nodes.push([current_node_alleles_alleles['id'], 'PaleGoldenRod']);
											//console.log('   Entered');
										}

									}
									if (json['gdr'][x]['alleles'][y][2]) {
										current_node_alleles_alleles['children'].push('<b>Metabolizer Status: </b>' + json['gdr'][x]['alleles'][y][2].replace("</p>", "").replace("<p>", ""));
										//new_HTML += '----> <b>Metabolizer Status: </b>' + json['gdr'][x]['alleles'][y][2] + '</p>\n';
									}
									if (json['gdr'][x]['alleles'][y][3]) {
										//current_node_alleles_alleles['children'].push('Recommendations: ' + json['gdr'][x]['alleles'][y][3]);
										jtree_modal(current_node_alleles_alleles, json['gdr'][x]['alleles'][y][3], 'Recommendations', current_node_name_alleles);
										//new_HTML += '----> <b>Recommendations: </b>' + json['gdr'][x]['alleles'][y][3] + '</p>\n';
									}
									if (json['gdr'][x]['alleles'][y][4]) {
										//current_node_alleles_alleles['children'].push('Implications: ' + json['gdr'][x]['alleles'][y][4]);
										jtree_modal(current_node_alleles_alleles, json['gdr'][x]['alleles'][y][4], 'Implications', current_node_name_alleles);
										//new_HTML += '----> <b>Implications: </b>' + json['gdr'][x]['alleles'][y][4] + '</p>\n';
									}
									if (json['gdr'][x]['alleles'][y][5]) {
										current_node_alleles_alleles['children'].push('<b>Phenotype: </b>' + json['gdr'][x]['alleles'][y][5].replace("</p>", "").replace("<p>", ""));
										//new_HTML += '----> <b>Phenotype: </b>' + json['gdr'][x]['alleles'][y][5] + '</p>\n';
									}
									if (json['gdr'][x]['alleles'][y][6]) {
										current_node_alleles_alleles['children'].push('<b>Activity Score: </b>' + json['gdr'][x]['alleles'][y][6].replace("</p>", "").replace("<p>", ""));
										//new_HTML += '----> <b>Activity Score: </b>' + json['gdr'][x]['alleles'][y][6] + '</p>\n';
									}
									//if (json['gdr'][x]['alleles'][y][7]) {
									//	current_node_alleles_alleles['children'].push('<a href="' + json['gdr'][x]['alleles'][y][7] + '"><b>Link</b></a>');
										//new_HTML += '----> <b>Activity Score: </b>' + json['gdr'][x]['alleles'][y][6] + '</p>\n';
									//}
								
								}

								//Clinical annotations
								if (false) {
									current_node_alleles_ca = {};
									current_node_alleles_ca['id'] = current_node_name + '_ca_' + json['gdr'][x]['alleles'][y][0];
									current_node_alleles_ca['text'] = 'Clinical Annotations';
									current_node_alleles_ca['state'] = { 'opened' : false, 'selected' : false };
									current_node_alleles_ca['children'] = [];


									//new_HTML += '----> <b>Clinical Annotations:</b></p>'
									for (var z in json['gdr'][x]['alleles'][y][8]) {

										current_clinical_annotation = {};
										current_clinical_annotation['id'] = current_node_name + '_alleles_' + json['gdr'][x]['alleles'][y][0] + '_' + z;
										clinical_annotation_index = (z*1)+1;
										//current_clinical_annotation['text'] = '<b>Clinical Annotation: </b>'  + clinical_annotation_index;
										current_clinical_annotation['text'] = '<b>Clinical Annotation: </b>'  + json['gdr'][x]['alleles'][y][8][z][6];
										current_clinical_annotation['state'] =  { 'opened' : false, 'selected' : false };
										current_clinical_annotation['children'] = [];

										current_clinical_annotation['children'].push('<b>Level of evidence: </b>' + json['gdr'][x]['alleles'][y][8][z][0]);
										//new_HTML += '--------> <b>Level of evidence: </b>' + json['gdr'][x]['alleles'][y][7][z][0] + '</p>\n';

										current_clinical_annotation['children'].push('<b>Type: </b>' + json['gdr'][x]['alleles'][y][8][z][1]);
										//new_HTML += '--------> <b>Type: </b>' + json['gdr'][x]['alleles'][y][7][z][1] + '</p>\n';

										current_clinical_annotation['children'].push('<b>Disease: </b>' + json['gdr'][x]['alleles'][y][8][z][2]); 
										//new_HTML += '--------> <b>Disease: </b>' + json['gdr'][x]['alleles'][y][7][z][2] + '</p>\n';

										current_clinical_annotation['children'].push('<b>OMB Race: </b>' + json['gdr'][x]['alleles'][y][8][z][3]); 
										//new_HTML += '--------> <b>OMB_Race: </b>' + json['gdr'][x]['alleles'][y][7][z][3] + '</p>\n';

										current_clinical_annotation['children'].push('<b>Race notes: </b>' + json['gdr'][x]['alleles'][y][8][z][4]); 
										//new_HTML += '--------> <b>Race_Notes: </b>' + json['gdr'][x]['alleles'][y][7][z][4] + '</p>\n';

										//current_clinical_annotation['children'].push('Clinical Annotation: ' + json['gdr'][x]['alleles'][y][7][z][5]); 
										jtree_modal(current_clinical_annotation, json['gdr'][x]['alleles'][y][8][z][5], "Clinical Annotation", current_node_name_alleles);
										//new_HTML += '--------> <b>Clinical_Annotation: </b>' + json['gdr'][x]['alleles'][y][7][z][5] + '</p>\n'; 

										current_node_alleles_ca['children'].push(current_clinical_annotation);
									
									}
									current_node_alleles_alleles['children'].push(current_node_alleles_ca);
								}
								current_node_alleles['children'].push(current_node_alleles_alleles);
							
								//new_HTML += '<hr>\n';
							}
							current_node['children'].push(current_node_alleles);
							json_tree.push(current_node);
						}

						//$("#recommendations_id")[0].innerHTML = new_HTML;
						$("#recommendations_id")[0].innerHTML = '';

						json_dd2 = [
							'Simple root node',
							{
								'id' : 'node_2',
								'text' : 'Root node with options',
								'state' : { 'opened' : true, 'selected' : true },
								'children' : [ { 'text' : 'Child 1' }, 'Child 2']
							}
							];

						$(function () { $('#jstree_demo_div').jstree('destroy')});

						// Feed the data to jstree
						// Can we make it bigger?
						// https://github.com/deitch/jstree-grid/issues/37 
						$(function () { $('#jstree_demo_div').jstree({
//							"plugins": ["grid"],
							"core" : {
								"data" : json_tree,
								"themes": {
									"name": "proton",
									"responsive": true
								}
							}
//							,"grid": {
//      							"columns": [
//          							{"header": 'Name', "width": 200},
//          							{"header": 'Column1' , "width": 200, "value": 'column1'}
//          						]
//							}
						}); });

						//$(function () { $('#jstree_demo_div').jstree({'core' : {'data' : json_dd2}}); });

						//select_node.jstree
						//changed.jstree
						$('#jstree_demo_div').on('select_node.jstree', function (e, data) {

							var orginal_node = data.instance.get_node(data.selected[0]).original;

							if (typeof orginal_node == 'string' || orginal_node instanceof String) {
								//Do nothing
							}
							else if ('longtext' in orginal_node) {
								//alert(orginal_node.longtext);

								//Put the html in the div
								$("#dialog_message")[0].innerHTML = '<strong>' + orginal_node.lttitle + '</strong><p>' + orginal_node.longtext;
								//$("#dialog_message")[0].setAttribute('title', data.instance.get_node(data.selected[0]).parent);
								//$("#dialog_message")[0].setAttribute('title', orginal_node.lttitle);
								$("#dialog_message")[0].setAttribute('title', 'Recommendations');

								//Show the modal window
								//----
								$(function() {
									$( "#dialog_message" ).dialog({
										modal: true,
										width: 1000,
										buttons: {
											Print : function() {
												// Make the Print button print the modal window and not the complete page
												// Using the JQuery plugin PrintArea : https://github.com/RitsC/PrintArea/blob/master/js/jquery.printarea.js 
												// var this_title = '<strong>' + $('#ui-id-1')[0].innerText + '</strong><p>';
												$('#dialog_message').html($('#dialog_message')[0].innerHTML).printArea(); 
												//window.print(); 
											}, 
											Ok: function() { $( this ).dialog( "close" ); }
										}
									});
  								});
							//----

							} 
							//alert(JSON.stringify(data.instance.get_node(data.selected[0])));
							//alert(data.instance.get_node(data.selected[0]).original.ddd);
							//alert('sdfsdfgsdfg');
						}).jstree();

						//Color nodes
						$('#jstree_demo_div').on('after_open.jstree', function (data) {

							//console.log('data:');
							//console.log(data);

							for (msp in colors) {
								$(".changecolor" + colors[msp]).css("background-color", colors[msp]);
							}

							//Color nodes
							//var colored_nodes_l = colored_nodes.length;
							//console.log('colored_nodes length: ' + colored_nodes_l)
							//for (var colored_nodes_i=0; colored_nodes_i<colored_nodes_l; colored_nodes_i++) {
								//$("#j1_2").css("color","red");
								//console.log(colored_nodes[colored_nodes_i][0] + ' ' + colored_nodes[colored_nodes_i][1]);
							//	$("#" + colored_nodes[colored_nodes_i][0] + " span:first-of-type").css("background-color", colored_nodes[colored_nodes_i][1]);
							//}

						}).jstree();

						// http://stackoverflow.com/questions/8378561/js-tree-links-not-active 
						// If a node in the tree is clicked. Check if it has a href attribute. If it has open href in new tab
						$("#jstree_demo_div").on("select_node.jstree", function (e, data) {
     						var href = data.node.a_attr.href;
     						if (href != '#') {
     							//document.location.href = href; // Same tab
     							var win = window.open(href, '_blank'); // New tab
     						}
						});

						var color_explain =             '<h5>Variant colors:';
						color_explain = color_explain + '<span style="border-style: solid; border-width: 2px; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Intermediate: <span style="color:' + colors["Intermediate Metabolizer"] + '">&#9608;</span></span>';
						color_explain = color_explain + '<span style="border-style: solid; border-width: 2px; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Ultra: <span style="color:' + colors["Ultrarapid Metabolizer"] + '">&#9608;</span></span>';
						color_explain = color_explain + '<span style="border-style: solid; border-width: 2px; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Poor: <span style="color:' + colors["Poor Metabolizer"] + '">&#9608;</span></span>';
						color_explain = color_explain + '<span style="border-style: solid; border-width: 2px; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Extensive: <span style="color:' + colors["Extensive Metabolizer"] + '">&#9608;</span></span>';
						color_explain = color_explain + '<span style="border-style: solid; border-width: 2px; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Unknown: <span style="color:' + colors["Unknown"] + '">&#9608;</span></span>';
						//color_explain = color_explain + '<span style="border-style: solid; padding-right: 15px; padding-left: 15px; padding-top: 5px; padding-bottom: 5px;">Unknown: <span style="color:' + colors["Unknown"] + '">&#9608;</span></span>';
						color_explain = color_explain + '</h5>';
						//https://github.com/kantale/emodia/issues/55 Removed label
						//$("#color_explain")[0].innerHTML =  color_explain;
					}
				}
			);

			$("#button_recommendations_id")[0].disabled = false;

		};

  		// RECOMMENDATIONS BUTTON END

		function process_init_data(json){
			//console.log(json);
			data = json;
			convert_json_to_select(data, true);

			var all_combo_boxes = ["#input_genes_id", "#input_drugs_id", "#combo_ms_id", "#combo_alleles_id"];

			//Check if the django template construction has fetched a string with the upload file filter 
			if (uds instanceof Array) {
				//console.log(uds);

				var total_filter_data = {}; //This will contain the data that we will update the UI later
				var uds_length = uds.length;
				for (var uds_i=1; uds_i<uds_length; uds_i++) {

					//This is one filter set
					data = json;
					for (var combo_box_index in all_combo_boxes) {
						var current_filter_data = {}; //This contains the data of the current filter line 

						var current_combo_box = all_combo_boxes[combo_box_index];

						//Get the filter values of this filter set
						var gene_value = uds[uds_i][combo_box_index];
						if (gene_value == 'null') {
							continue;
						}
						var all_checkboxes = $(current_combo_box).multiselect("widget").find(":checkbox[title='" + gene_value + "']");
						var all_checkboxes_l = all_checkboxes.length;

						//Click all items in the multiselect that match the filter value
						for (var all_checkboxes_i =0; all_checkboxes_i < all_checkboxes_l; all_checkboxes_i++) {
							all_checkboxes[all_checkboxes_i].click();
						}

						data = get_fields(current_combo_box.substring(1), current_filter_data);
						//current_filter_data = data; //In case current_filter_data is not changed from get_fields

						//un - click them 
						for (var all_checkboxes_i =0; all_checkboxes_i < all_checkboxes_l; all_checkboxes_i++) {
							all_checkboxes[all_checkboxes_i].click();
						}

					}


//						$.extend(total_filter_data, data);


					//Put current_filter_data to total_filter_data
					for (g in data) {
						if (!(g in total_filter_data)) {
							total_filter_data[g] = {};
						}
						for (d in data[g]) {
							if (!(d in total_filter_data[g])) {
								total_filter_data[g][d] = {'alleles' : [], 'MSP' : []};
							}
							for (a_index in data[g][d]['alleles']) {
								var allele = data[g][d]['alleles'][a_index];
								var msp = data[g][d]['MSP'][a_index];
								if (total_filter_data[g][d]['alleles'].indexOf(allele) == -1) {
									total_filter_data[g][d]['alleles'].push(allele);
									total_filter_data[g][d]['MSP'].push(msp);
								}
							}
						}
					}
				}

				//Update UI with total_filter_data
				data = total_filter_data;
				convert_json_to_select(data, false);

			}

			//If we have preloaded filter from Tzeni translation "press" the "recommendations" button (#23)
			//console.log(init_translation);
			if (init_translation["INIT_GENE"].length > 0) {
				//Check if data is empty 
				//console.log(data);
				if (Object.keys(data).length == 0) { //http://stackoverflow.com/questions/5223/length-of-a-javascript-object-that-is-associative-array
					//Although we have initial data. There was no much. So show a message (#28)
					$("#recommendations_id")[0].innerHTML = '<strong>No match found</strong>'

					//Deactivate button 
					$("#button_recommendations_id")[0].disabled = true;
				}
				else {
					// "press" the "recommendations" button 
					$("#button_recommendations_id")[0].click();
				}
			}
			$("#recommendations_id")[0].innerHTML = "";
		}

		$("#recommendations_id")[0].innerHTML = "<h3>Initializing. Please Wait..</h3>";

		//Initialize combo boxes 
		$("#input_genes_id").multiselect({
			close : function(event, ui){

				var component = event.target.id;
				get_fields(component, 0);
			},
			selectedText : '# Gene(s) selected'	
		});

		$("#input_drugs_id").multiselect({
			close : function(event, ui){

				var component = event.target.id;
				get_fields(component, 0);
			},
			selectedText : '# Drug(s) selected'	
		});

		$("#combo_ms_id").multiselect({
			close : function(event, ui){

				var component = event.target.id;
				get_fields(component, 0);
			},
			selectedText : '# Metabolizer Status(es) selected'	
		});

		$("#combo_alleles_id").multiselect({
			close : function(event, ui){

				var component = event.target.id;
				get_fields(component, 0);
			},
			selectedText : '# Variations(s) selected'	
		});

		//Fetch data
		//If we have data from Jenny let Django decide the initial data
		if (init_translation["INIT_GENE"].length > 0) {
			 $.post(
			//$.getJSON(
				"fetch_init_json/",
				init_translation, // Init data from Tzeni Translation
				function(json, textStatus) {
					process_init_data(json);
				}
			);
		}
		else {
			//If we don't have data from Jenu then feed from local file 
			process_init_data(fetch_init_data);
		}


//		$("select").multiselect({
//			close : function(event, ui){
//
//				var component = event.target.id;
//				get_fields(component, 0);
//			}
//		});

//		$("#recommendations_id")[0].innerHTML = "";

		//alert(data);
		//console.log(data.length);
		//console.log(data);

		//HANDLE FILE UPLOAD

		function prepareUpload(event) {
			//console.log('id_file pressed');

			document.getElementById("upload_form_id").submit();
		}

		$('#id_file').on('change', prepareUpload);

		//END OF HANDLE FILE UPLOAD 
	} //END OF after_load
