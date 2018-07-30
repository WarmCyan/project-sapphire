<?php
//***************************************************************************
//
//  File: index.php
//  Date created: 07/29/2018
//  Date edited: 07/29/2018
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

<h1>Hello World!</h1>

<h2>Execution Units</h2>
<?php 
	$units = getExecutionUnits();
	
	foreach ($units as $name => $info)
	{
		echo("<p><b>Unit '" . $name . "'</b></p>");
		echo("<p>&nbsp;&nbsp;Status: " . $units[$name]["status"] . "</p>");
		echo("<p>&nbsp;&nbsp;Last Schedule Poll: " . $units[$name]["lastpoll"] . "</p>");
	}

?>

<?php getFooter(); ?>
