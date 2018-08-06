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

<p><a href="feed.php">Feed</a></p>


<p><a href="https://github.com/WildfireXIII/project-sapphire">https://github.com/WildfireXIII/project-sapphire</a></p>


<h1>Server Status</h1>

<?php

// get data
$lastContentScrape = getLastContentScrape();
$lastFeedScrape = getLastFeedScrape();
$articleCount = getArticleContentCount();
$totalSpace = getSpaceUtilization();

$statsTimeline = getStatsTimeline();

echo("<script>var data = " . $statsTimeline . ";</script>");

?>
<p>Last content scrape: <?php echo($lastContentScrape); ?></p>
<p>Last feed scrape: <?php echo($lastFeedScrape); ?></p>
<p>articles: <?php echo($articleCount); ?></p>
<p>space: <?php echo($totalSpace); ?></p>

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
