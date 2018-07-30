<?php
//***************************************************************************
//
//  File: utility.php
//  Date created: 07/29/2018
//  Date edited: 07/29/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Useful common functions
//
//***************************************************************************

$configJson = false;

// thanks to https://stackoverflow.com/questions/834303/startswith-and-endswith-functions-in-php 
function startsWith($haystack, $needle)
{
     $length = strlen($needle);
     return (substr($haystack, 0, $length) === $needle);
}
function endsWith($haystack, $needle)
{
    $length = strlen($needle);

    return $length === 0 || 
    (substr($haystack, -$length) === $needle);
}

function readConfig()
{
	global $configJson;
	
	$configString = file_get_contents("/home/dwl/conf/sapphire_config.json");
	$configJson = json_decode($configString, true);
}

function checkLazyLoadConfig() { if (!$configJson) { readConfig(); } }

function getStatsDir()
{
	global $configJson;
	
	checkLazyLoadConfig();
	if (!endsWith($configJson, '/')) { $configJson['stats_dir'] .= '/'; }

	return $configJson['stats_dir'];
}

function getExecutionUnits()
{
	$units = array();

	// get all files in stats dir
	$files = scandir(getStatsDir());
	foreach($files as $file)
	{
		// check if status file
		$matches = array();
		$result = preg_match("/([\w|\_]*)\_status/", $file, $matches);
		if ($result == 1)
		{
			// read the content of the file
			$status = file_get_contents(getStatsDir() . $file);
			
			// store info in array
			$unitName = $matches[1];
			if (!array_key_exists($unitName, $units)) { $units[$unitName] = array(); }
			$units[$unitName]["status"] = $status;
		}
		
		// check if poll timestamp
		$matches = array();
		$result = preg_match("/([\w|_]*)_poll_timestamp/", $file, $matches);
		if ($result == 1)
		{
			// read the content of the file
			$timestamp = file_get_contents(getStatsDir() . $file);
			$timestampDT = date_create_from_format('Y-m-d H:i:s', $timestamp, new DateTimeZone('UTC'));
			$timestampDT->setTimezone(new DateTimeZone('America/Chicago'));
			$timestamp = $timestampDT->format('H:i:s (m/d/Y)');
				
 			
			// store info in array
			$unitName = $matches[1];
			if (!array_key_exists($unitName, $units)) { $units[$unitName] = array(); }
			$units[$unitName]["lastpoll"] = $timestamp;
		}
	}

	return $units;
}

?>
