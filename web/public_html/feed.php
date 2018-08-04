<?php
//***************************************************************************
//
//  File: feed.php
//  Date created: 08/04/2018
//  Date edited: 08/04/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Page that contains (for now) the raw feed
//
//***************************************************************************

include_once('../includes/utility.php');
include_once('../templates/header.php');
include_once('../templates/footer.php');

include_once('../includes/db_connection.php');



$articles = array();
$con = new Connection();
$results = $con->query("SELECT * FROM Articles WHERE content IS NOT NULL ORDER BY timestamp LIMIT 20");
while ($record = $results->fetch_object()) { array_push($articles, $record); }

//var_dump($articles);

getHeader("Sapphire");

?>

<h1>Feed</h1>

<?php

for ($i = 0; $i < count($articles); $i++)
{
	echo("<h3>" . $articles[$i]->title . "</h3>");
	echo("<p>" . nl2br($articles[$i]->content) . "</p>");
}

?>
