
var svg = d3.select('svg');
margin = {top: 20, right: 20, bottom: 30, left: 40},
width = +svg.attr("width") - margin.left - margin.right,
height = +svg.attr("height") - margin.top - margin.bottom;

var xScaleLinear = d3.scaleLinear().range([0, height]);
var xScaleBand = d3.scaleBand().rangeRound([0, height]);

d3.text('colors.txt', function(err, data) {

    data = data
        .split('\n')
        .map(d =>
	     d.split(' ').filter(d => d !== '')
	    )
	.filter(d => d.length)
	.map(d => {
	    return { v: d[0], r: +d[1], g: +d[2], b: +d[3] };
	});

    console.log(JSON.stringify(data));

    // render strings for use as Sass variables (choose not to go this route)
    var sassStrings = data.map(d => `$name${d.v}: rgb(${d.r}, ${d.g}, ${d.b});`);

    //       console.log(sassStrings);
    xScaleBand.domain(data.map(d => d.v));
    var g = svg.append('g');
    g.selectAll('rectangle')
	.data(data)
	.enter().append('rect')
	.attr('class', 'rectangle')
	.attr('x', 0)
	.attr('y', function(d) { return xScaleBand(d.v); })
	.attr('width', 40)
	.attr('height', 40)
	.style('fill', function(d) { return `rgb(${d.r}, ${d.g}, ${d.b})`; });

});
