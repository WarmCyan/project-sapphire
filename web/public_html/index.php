<?php
//***************************************************************************
//
//  File: index.php
//  Date created: 07/29/2018
//  Date edited: 08/05/2018
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

<script>

var svg = d3.select("svg"),
	margin = {top: 20, right: 20, bottom: 20, left: 50},
	width = +svg.attr("width") - margin.left - margin.right,
	height = +svg.attr("height") - margin.top - margin.bottom,
	g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var parseTime = d3.timeParse("%Q");

var x = d3.scaleTime()
    .rangeRound([0, width]);

var y = d3.scaleLinear()
    .rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

	
d3.csv("spacestatstimeline.php", function(d) {
	d.date = parseTime(d.date);
	d.close = +d.content_store_dir_filecount;
	return d;
}, function(error, data) {
	if (error) throw error;	

	x.domain(d3.extent(data, function(d) { return d.date; }));
	y.domain(d3.extent(data, function(d) { return d.content_store_dir_filecount; }));

	g.append("g")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(x))
		.select(".domain")
		.remove();

	g.append("g")
		.call(d3.axisLeft(y))
		.append("text")
		.attr("fill", "#000")
		.attr("transform", "rotate(-90)")
		.attr("y", 6)
		.attr("dy", "0.71em")
		.attr("text-anchor", "end")
		.text("Price ($)");

	g.append("path")
		.datum(data)
		.attr("fill", "none")
		.attr("stroke", "steelblue")
		.attr("stroke-linejoin", "round")
		.attr("stroke-linecap", "round")
		.attr("stroke-width", 1.5)
		.attr("d", line);	
});

</script>

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



<svg id="graph" width="960", height="500"></svg>


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


<?php getFooter(); ?>
