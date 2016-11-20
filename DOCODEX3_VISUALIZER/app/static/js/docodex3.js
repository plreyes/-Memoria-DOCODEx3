SERVER = "http://localhost:5000"
$('#docode_m').val(400);

// - ------------------------------------------------

/*BlockUI*/
function blockUI_init(message){
  $.blockUI({ 
    message: message,
    css: { 
      border: 'none', 
      padding: '15px', 
      backgroundColor: '#000', 
      '-webkit-border-radius': '10px', 
      '-moz-border-radius': '10px', 
      opacity: .5, 
      color: '#fff',
      fontSize: "1.5em"
    } 
  });
}

// - ------------------------------------------------

function compare_segment_barchart(s){
	blockUI_init('Procesando ...');
	$(".sc").hide();
  generated = $("#segment-"+s+" .generated").val();
  if(generated == 1){
  	$("#segment-"+s).show();
  }else{
  	//ftsv = DOCODE_JSON['segments'][s]['sv_keys'].map(function(k){return DOCODE_JSON['fulltext_vector'][k]; });
  	ftsv = DOCODE_JSON['segments'][s]['s_ftv'];
    console.log(ftsv);
  	barchart_ft_segment(VOCABULARY, DOCODE_JSON['segments'][s]['sv_keys'], ftsv, "#segment-"+s+" .bc-s-fulltext");
  	barchart_ft_segment(VOCABULARY, DOCODE_JSON['segments'][s]['sv_keys'], DOCODE_JSON['segments'][s]['sv_values'], "#segment-"+s+" .bc-s-segment");
  	//Linechart
    s_ftv = [], sv = []
    for (i = 0; i < DOCODE_JSON['segments'][s]['sv_values'].length; i++) { 
      s_ftv.push([i, DOCODE_JSON['segments'][s]['s_ftv'][i]]);
      sv.push([i, DOCODE_JSON['segments'][s]['sv_values'][i]]);
    }
    linechart_data = [{data: s_ftv, label: 'Texto'}, {data: sv, label: 'Segmento'}]
    console.log(linechart_data);
    draw_linechart("#segment-"+s+" .docode-segment-compare-linechart", linechart_data, 'Palabra', 'Frecuencia'); 
    
    $("#segment-"+s+" .generated").val(1);
  	$("#segment-"+s).show();
  	bc_scroll();
  }
  $.unblockUI();
}

function bc_scroll(){
  var subCatContainer = $(".bc-scroll");
  subCatContainer.scroll(function() {
      subCatContainer.scrollLeft($(this).scrollLeft());
  });
}


function barchart_fulltext(vocabulary, vector, element_id){
	$(element_id).html('');	
	
	var margin = {top: 20, right: 20, bottom: 80, left: 40},
	    width = vector.length*10,
	    height = 400 - margin.top - margin.bottom;
	
	var x = d3.scale.ordinal()
	    .rangeBands([0, width],.1);
	
	var y = d3.scale.linear()
	    .range([height, 0]);
	
	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");
	
	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");
	
	var svg = d3.select(element_id).append("svg")
	    .attr("width", width)
	    .attr("height", height + margin.top + margin.bottom)
	  	.append("g")
	    	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  x.domain(vocabulary);
  y.domain([0, d3.max(vector)]);
  
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-1em")
            .attr("dy", "-0.5em")
            .attr("transform", "rotate(-90)" );
  
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);
  
  i=-1;
  data = vocabulary.map(function(v){i += 1; return [v,vector[i]]})
  svg.selectAll(".bar")
     .data(data)
     .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d){return x(d[0]); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d){return y(d[1]); })
	      .attr("height", function(d) { return height - y(d[1]); });
}

function barchart_ft_segment(vocabulary, indexes, vector, element_id){
	$(element_id).html('');	
	var margin = {top: 20, right: 20, bottom: 80, left: 40},
	    width = indexes.length*10,
	    height = 400 - margin.top - margin.bottom;
	
	var x = d3.scale.ordinal()
	    .rangeBands([0, width],.1);
	
	var y = d3.scale.linear()
	    .range([height, 0]);
	
	var xAxis = d3.svg.axis()
	    .scale(x)
	    .orient("bottom");
	
	var yAxis = d3.svg.axis()
	    .scale(y)
	    .orient("left");
	
	var svg = d3.select(element_id).append("svg")
	    .attr("width", width)
	    .attr("height", height + margin.top + margin.bottom)
	  	.append("g")
	    	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  x.domain(indexes.map(function(i){ return vocabulary[i]}));
  y.domain([0, d3.max(vector)]);
  
  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")  
            .style("text-anchor", "end")
            .attr("dx", "-1em")
            .attr("dy", "-0.5em")
            .attr("transform", "rotate(-90)" );
  
  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);
  
  i=-1;
  data = indexes.map(function(v){i += 1; return [vocabulary[v],vector[i]]})
  svg.selectAll(".bar")
     .data(data)
     .enter().append("rect")
	      .attr("class", "bar")
	      .attr("x", function(d){return x(d[0]); })
	      .attr("width", x.rangeBand())
	      .attr("y", function(d){return y(d[1]); })
	      .attr("height", function(d) { return height - y(d[1]); });
}

function histogram(data, container_id){
  $(container_id).html('');
  // Generate a Bates distribution of 10 random variables.
  var values = data;

  // A formatter for counts.
  var formatCount = d3.format(",.0f");

  var margin = {top: 10, right: 30, bottom: 30, left: 30},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x = d3.scale.linear()
      .domain([0, 1])
      .range([0, width]);

  // Generate a histogram using twenty uniformly-spaced bins.
  var data = d3.layout.histogram()
      .bins(x.ticks(50))
      (values);

  var y = d3.scale.linear()
      .domain([0, d3.max(data, function(d) { return d.y; })])
      .range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var svg = d3.select(container_id).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var bar = svg.selectAll(".bar")
      .data(data)
    .enter().append("g")
      .attr("class", "bar")
      .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });

  bar.append("rect")
      .attr("x", 1)
      .attr("width", x(data[0].dx) - 1)
      .attr("height", function(d) { return height - y(d.y); });

  bar.append("text")
      .attr("dy", ".75em")
      .attr("y", 6)
      .attr("x", x(data[0].dx) / 2)
      .attr("text-anchor", "middle")
      .text(function(d) { return formatCount(d.y); });

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);
}


//Generamos tabla con segmentos de texto
function segments_table(){
  html  = " <thead>"
  html += "   <th>ID</th>"
  html += "   <th>Palabra Inicial</th>"
  html += "   <th>Palabra Final</th>"
  html += "   <th>Estilo Segmento</th>"
  html += "   <th>0.075</th>"
  html += "   <th>Opciones</th>"
  html += " </thead>"
  html += " <tbody>"
                $.each(DOCODE_JSON['segments'],function(s){
  html += "   <tr>"
  html += "   <td>"+s+"</td>"
  html += "   <td>"+DOCODE_JSON['segments'][s]['initial_word']+"</td>"
  html += "   <td>"+DOCODE_JSON['segments'][s]['final_word']+"</td>"
  html += "   <td>"+DOCODE_JSON['segments'][s]['s_style'].toFixed(3)+"</td>"
  html += "   <td>"; if(DOCODE_JSON['segments'][s]['s_style'] >= DOCODE_JSON['style']-0.075){ html += 'No Plagio' }else{ html += "<b class='text-danger'>Plagio<b>" }; html += "</td>";
  html += "   <td>"
  html += "       <a role='button' class='btn' onClick=compare_segment_barchart("+s+")>Visualizar</a></td>"
  html += "   </tr>"
                });
  html += " </tbody>"
  return html;
}

function matrices(m, pv, segments, style, thresholds){
  //Creamos un vector de plagio comparable con lo obtenido por el algoritmo.
  //Consideramos un segmento de m items como plagio si a lo menos un item del segmento es plagio
  pvc = []
  for(i = 0; i < segments.length; i++){ 
    s = pv.slice(segments[i]['initial_word'], segments[i]['final_word']);
    if(s.indexOf(1) > -1){ //Encontramos plagio en al menos un elemento
      pvc = $.merge( pvc, s.map(function(x){return 1;}) );
    }else{
      pvc = $.merge( pvc, s.map(function(x){return 0;}) );
    }
  }

  html = ""
  $.each(thresholds, function(i){
    pv2 = pv.map(function(w){ return 0; }); 
    sd  = style - thresholds[i]
    $.each(segments, function(j){
      if(segments[j]['s_style'] < sd){
        for(k = segments[j]['initial_word']; k<segments[j]['final_word']; k++){
          pv2[k] = 1;
        }
      }
    });

    tp = 0, fp = 0, tn = 0, fn = 0;
    for(j=0; j<pv.length; j++){
      if(pvc[j] == 1 && pv2[j] == 1){
        tp += 1
      }else if(pvc[j] == 1 && pv2[j] == 0){
        fp += 1
      }else if(pvc[j] == 0 && pv2[j] == 0){
        tn += 1
      }else if(pvc[j] == 0 && pv2[j] == 1){
        fn += 1
      }
    }
    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f_measure = (2*precision*recall)/(precision+recall)
    html += "<div class='thumbnail'>"
    html += "  <div class='caption'>"
    html += "   <h3>Threshold "+thresholds[i]+"</h3>"
    html += "   <table class='table table-bordered'>"
    html += "     <thead>"
    html += "       <th></th>"
    html += "       <th>P</th>"
    html += "       <th>N</th>"
    html += "     </thead>"
    html += "     <tbody>"
    html += "       <tr>"
    html += "         <td><b>P</b></td>"
    html += "         <td>"+tp+"</td>"
    html += "         <td>"+fn+"</td>"
    html += "       </tr>"
    html += "       <tr>"
    html += "         <td><b>N</b></td>"
    html += "         <td>"+fp+"</td>"
    html += "         <td>"+tn+"</td>"
    html += "       </tr>"
    html += "     </tbody>"
    html += "   </table>"
    html += "   <table class='table'>"
    html += "     <thead>"
    html += "       <th>Precision</th>"
    html += "       <th>Recall</th>"
    html += "       <th>F-measure</th>"
    html += "     </thead>"
    html += "     <tbody>"
    html += "       <tr>"
    html += "         <td>"+precision+"</td>"
    html += "         <td>"+recall+"</td>"
    html += "         <td>"+f_measure+"</td>"
    html += "       </tr>"
    html += "     </tbody>"
    html += "   </table>"
    html += "  </div>"
    html += "</div>"

  });

  return html;
}