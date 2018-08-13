<?php
//***************************************************************************
//
//  File: index.php
//  Date created: 07/29/2018
//  Date edited: 08/12/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Home page
//
//***************************************************************************

include_once('../includes/utility.php');
include_once('../templates/header.php');
include_once('../templates/footer.php');


getHeader("Sapphire");

?>


<p><a href="feed.php">Feed</a></p>


<p><a href="https://github.com/WildfireXIII/project-sapphire">https://github.com/WildfireXIII/project-sapphire</a></p>


<h1>Server Status</h1>

<?php

// get data
$lastContentScrape = getLastContentScrape();
$lastFeedScrape = getLastFeedScrape();
$articleCount = getArticleContentCount();
$totalSpace = getSpaceUtilization();

?>
<p>Last content scrape: <?php echo($lastContentScrape); ?></p>
<p>Last feed scrape: <?php echo($lastFeedScrape); ?></p>
<p>articles: <?php echo($articleCount); ?></p>
<p>space: <?php echo($totalSpace); ?></p>



<svg class="graph" width="960", height="500"></svg>
</br>
</br>


<div id='stats_box'>
	<h2>Execution Units</h2>
	<?php 
		$units = getExecutionUnits();
		
		foreach ($units as $name => $info)
		{
			echo("<p><b>Unit '" . $name . "'</b></p>");
			echo("<ul>");
			echo("<li>Status: " . $units[$name]["status"] . "</li>");
			echo("<li>Last Schedule Poll: " . $units[$name]["lastpoll"] . "</li>");
			echo("</ul>");
		}
	?>
</div>

<script>

var svg = d3.select(".graph");
var margin = {top: 50, right: 30, bottom: 50, left: 60};
var width = +svg.attr("width") - margin.left - margin.right;
var height = +svg.attr("height") - margin.top - margin.bottom;
var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%s");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.value); });

var tip = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

// title
svg.append("text")
	.attr("x", ((width + margin.left + margin.top) / 2))             
	//.attr("y", 0 - (margin.top / 2))
	.attr("y", 0 + (margin.top / 2))
	.attr("text-anchor", "middle")  
	.attr("class", "title")  
	.text("Article Count over Time");
	
d3.csv("spacestatstimeline.php", function(d) {
	console.log(d);
	//d.date = parseTime(d.date);
	//d.content_store_dir_filecount = +d.content_store_dir_filecount;
	//return d;
	return {
		date: d3.timeDay.floor(parseTime(d.time)),
			value: +d.content_store_dir_filecount
	};

}, function(error, data) {
	if (error) throw error;	

	x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain(d3.extent(data, function(d) { return d.value; }));

	// x axis
	g.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr("class", "axis")
		.call(d3.axisBottom(x).tickFormat(d3.timeFormat("%-m/%-d")))
		//.select(".domain")
		.append("text")
			.attr("class", "axisLabel")
			.attr("y", 25)
			.attr("dy", ".7em")
			.attr("x", (width / 2))
			.text("Date");
		
	// y axis
	g.append("g")
		.attr("class", "axis")
		.call(d3.axisLeft(y))
		.append("text")
			.attr("class", "axisLabel")
			.attr("transform", "rotate(-90)")
			.attr("y", 0 - margin.left)
			.attr("dy", "1.5em")
			.attr("x", 0 - (height / 2))
			.attr("text-anchor", "middle")
			.text("Article Count");

	// x axis grid lines
	g.append("g")
		.attr("class", "grid")
		.attr("transform", "translate(0,"+height+")")
		.call(d3.axisBottom(x)
			.ticks(10)
			.tickSize(-height)
			.tickFormat(""));
	 
	// y axis grid lines
	g.append("g")
		.attr("class", "grid")
		//.attr("transform", "translate(0,"+height+")")
		.call(d3.axisLeft(y)
			.ticks(10)
			.tickSize(-width)
			.tickFormat(""));

	// graph line
	g.append("path")
		.datum(data)
		.attr("fill", "none")
		.attr("stroke", "steelblue")
		.attr("stroke-linejoin", "round")
		.attr("stroke-linecap", "round")
		.attr("stroke-width", 1.5)
		.attr("d", line);	

	// graph points
	g.selectAll(".dot")
		.data(data)
		.enter().append("circle")
			.attr("class", "dot")
			.attr("cx", function(d) { return x(d.date); })
			.attr("cy", function(d) { return y(d.value); })
			.attr("r", 4)
			.on("mouseover", function(d) {
				tip.transition()
					.duration(100)
					.style('opacity', '.9');
				tip.html(d.date + "</br>" + d.value)
					.style("left", (d3.event.pageX) + "px")
					.style("top", (d3.event.pageY) + "px");
			})
			.on("mouseout", function(d) {
				tip.transition()
					.duration(100)
					.style("opacity", "0");
			});
});

</script>

<?php getFooter(); ?>
