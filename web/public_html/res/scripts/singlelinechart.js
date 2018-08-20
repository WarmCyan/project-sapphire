//***************************************************************************
//
//  File: singlelinechar.js
//  Date created: 08/19/2018
//  Date edited: 08/19/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Abstraction for easily making a linechart
//
//***************************************************************************

function drawSingleLineTimeChart(id, dataurl, datecolname, valcolname, title, vallabel, margin={top: 50, right: 30, bottom: 50, left: 60})
{
	// get the element
	var svg = d3.select(id);
	
	// determine graph height and width
	var width = +svg.attr("width") - margin.left - margin.right;
	var height = +svg.attr("height") - margin.top - margin.bottom;

	// set up the space for where the actual axes will go
	var paddedG = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	
	// set up the function for parsing datetime from the data
	var parseTime = d3.timeParse("%s");
	
	// set up the x and y scaling functions
	var x = d3.scaleTime().rangeRound([0, width]);
	var y = d3.scaleLinear().rangeRound([height, 0]);

	// define the line's points from the data
	var line = d3.line()
		.x(function(d) { return x(d.date); });
		.y(function(d) { return y(d.value); });

	// set up the tooltip
	var tooltip = d3.select("body").append("div")
		.attr("class", "graphTooltip")
		.style("opacity", 0);

	// set up the title
	svg.append("text")
		.attr("x", ((width + margin.left + margin.top) / 2))             
		.attr("y", 0 + (margin.top / 2))
		.attr("text-anchor", "middle")  
		.attr("class", "graphTitle")  
		.text(title);

	// load the data
	d3.csv(dataurl, function(d) {
		return {
			date: d3.timeDay.floor(parseTime(d[datecolname])),
			value: +d[valcolname]
		};
	},
	function(error, data)
	{
		if (error) throw error;

		// set up the domains
		x.domain(d3.extent(data, function(d) { return d.date; }));
		y.domain(d3.extent(data, function(d) { return d.value; }));

		// add the x axis
		paddedG.append("g")
			.attr("transform", "translate(0," + height + ")")
			.attr("class", "graphAxis")
			.call(d3.axisBottom(x).tickFormat(d3.timeFormat("%-m/%-d")))
			.append("text")
				.attr("class", "graphAxisLabel")
				.attr("y", 25)
				.attr("dy", ".7em")
				.attr("x", (width / 2))
				.text("Date");

		// add x axis grid lines
		paddedG.append("g")
			.attr("class", "graphGrid")
			.attr("transform", "translate(0,"+height+")")
			.call(d3.axisBottom(x)
				.ticks(10)
				.tickSize(-height)
				.tickFormat(""));
		
		// add the y axis
		paddedG.append("g")
			.attr("class", "graphAxis")
			.call(d3.axisLeft(y))
			.append("text")
				.attr("class", "graphAxisLabel")
				.attr("transform", "rotate(-90)")
				.attr("y", 0 - margin.left)
				.attr("dy", "1.5em")
				.attr("x", 0 - (height / 2))
				.attr("text-anchor", "middle")
				.text(vallabel);

		// add y axis grid lines
		paddedG.append("g")
			.attr("class", "graphGrid")
			.call(d3.axisLeft(y)
				.ticks(10)
				.tickSize(-width)
				.tickFormat(""));
		 
		// plot the line
		paddedG.append("path")
			.datum(data)
			.attr("fill", "none")
			.attr("stroke", "steelblue")
			.attr("stroke-linejoin", "round")
			.attr("stroke-linecap", "round")
			.attr("stroke-width", 1.5)
			.attr("d", line);	

		// plot the line points
		paddedG.selectAll(".graphDot")
			.data(data)
			.enter().append("circle")
				.attr("class", "graphDot")
				.attr("cx", function(d) { return x(d.date); })
				.attr("cy", function(d) { return y(d.value); })
				.attr("r", 4)
				.on("mouseover", function(d) {
					tooltip.transition()
						.duration(100)
						.style('opacity', '.9');
					tooltip.html(d.date + "</br>" + d.value)
						.style("left", (d3.event.pageX) + "px")
						.style("top", (d3.event.pageY) + "px");
				})
				.on("mouseout", function(d) {
					tooltip.transition()
						.duration(100)
						.style("opacity", "0");
				});
	});
}
