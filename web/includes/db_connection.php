<?php
//***************************************************************************
//
//  File: db_connection.php
//  Date created: 08/04/2018
//  Date edited: 08/04/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: File with an object to help with querying the database
//
//***************************************************************************

include_once('utility.php');

class Connection
{
	private $connection;

	public function __construct()
	{
		$params = getDBConfig();
		$this->connection = new mysqli($params["host"], $params["user"], $params["password"], $params["db"]);
		mysqli_set_charset($this->connection, "utf8");  
	}
	public function query($sql) { return $this->connection->query($sql); }
}


?>
