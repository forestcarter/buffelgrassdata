
var svg = d3.select('#svg1');
margin = {top: 20, right: 20, bottom: 65, left: 40},
width = +svg.attr("width") - margin.left - margin.right,
height = +svg.attr("height") - margin.top - margin.bottom;

var xScaleLinear = d3.scaleLinear().range([0, height]);
var xScaleBand = d3.scaleBand().rangeRound([0, height+60]);

d3.text('colorsahps.txt', function(err, data) {

    data = data
        .split('\n')
        .map(d =>
	     d.split(' ').filter(d => d !== '')
	    )
	.filter(d => d.length)
	.map(d => {
	    return { v: d[0], r: +d[1], g: +d[2], b: +d[3] };
	});

    //update values
    console.log(`MYVAL ${data[0].v}`);
    document.getElementById(`scale1`).innerHTML = "No Data";
    for(var i =2; i<9;i++){
	document.getElementById(`scale${i}`).innerHTML = `${data[i*2-3].v}`;
    }
    console.log(JSON.stringify(data));

   
    xScaleBand.domain(data.map(d => d.v));
    var g = svg.append('g');
    g.selectAll('rectangle')
	.data(data)
	.enter().append('rect')
	.attr('class', 'rectangle')
	.attr('x', 0)
	.attr('y', function(d) { return xScaleBand(d.v); })
	.attr('width', 40)
	.attr('height', 20)
	.style('fill', function(d) { return `rgb(${d.r}, ${d.g}, ${d.b})`; });

});

