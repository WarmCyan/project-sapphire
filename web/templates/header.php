<?php
//***************************************************************************
//
//  File: header.php
//  Date created: 07/29/2018
//  Date edited: 08/03/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Functions for getting the header html for a page
//
//***************************************************************************

function getHeader($title)
{
	$version = "0.1.1";
	
	$html = <<<HTML

<html>
	<head>
		<link rel='stylesheet' href='res/styles/frontend.css'>
		<title>$title</title>
	</head>

	<body>
		<div id='header'>
			<div id='header-left'>
				<img src='res/images/header_394x100.png' />
			</div> <!-- /header-left -->
			<div id='header-version'>
				<p>v$version</p>
			</div> <!-- /header-version -->
			
			<div id='header-right'>
				<a href="http://digitalwarriorlabs.com"><img src='res/images/white_no_title100x100.png'/></a>
			</div> <!-- /header-right -->

			<div style='clear: both;'></div>
		</div> <!-- /header -->

		<div id='content'>
	
HTML;
	
	echo($html);
}

?>
