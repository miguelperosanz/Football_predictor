
// set the dimensions and margins of the graph
var width = 350
    height = 350
    margin = 30

// The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
var radius = Math.min(width, height) / 2 - margin


// append the svg object to the div called 'my_dataviz'
var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var color =["#98abc5", "#8a89a6", "#7b6888"]


  var data = d3.selectAll('.values_full_before').nodes();


  //we create this variable, for the values to be readeable in the console
  var pie = d3.pie()   
  .value(function(d) {return d.innerHTML; })(data);



  var u = svg.selectAll("path")
  .data(pie)

  u
    .enter()
    .append('path')
    .attr('d', d3.arc()
      .innerRadius(0)
      .outerRadius(radius)
    )

    .attr('fill', function(d,i){ return color[i] })
    .attr("stroke", "white")
    .style("stroke-width", "5px")
    .style("opacity", 0.2)




    update(u);

    

function update() {


  var data = d3.selectAll('.values').nodes();


  var pie = d3.pie()   //we create this variable, for the values to be readeable in the console
  .value(function(d) {return d.innerHTML; })(data);

  if (pie[0].value + pie[0].value + pie[0].value < 90) {
    var annotations = ["", "", ""];
  } else {
    var annotations = ["Home win", "Draw game", "Away win"];
  }


  var u = svg.selectAll("path")
  .data(pie)


  u
    .enter()
    .append('path')
    .merge(u)
    .transition()
    .duration(3000)
    .attr('d', d3.arc()
      .innerRadius(0)
      .outerRadius(radius)
    )

    .attr('fill', function(d,i){ return color[i] })
    .attr("stroke", "white")
    .style("stroke-width", "5px")
    .style("opacity", 1)

    var arcGenerator = d3.arc()
    .innerRadius(0)
    .outerRadius(radius*1.5)
  
    
    svg
    .selectAll('annotationsss')
    .data(pie)
    .enter()
    .append('text')
  
    .text(function(d,i){ return annotations[i] })
    .attr("transform", function(d) { return "translate(" + arcGenerator.centroid(d) + ")";  })
    .style("text-anchor", "middle")
    .style("font-size", 17)




}

// Initialize the plot with the first dataset

