<?php
//***************************************************************************
//
//  File: query_manager.php
//  Date created: 08/04/2018
//  Date edited: 08/04/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Class to abstract some of the nasty query stuff
//
//***************************************************************************


// NOTE: Not really sure if this will be necessary or not? (probably do this to
// be safe)
class QueryManager extends Connection
{
	private $table;
	private $connection;
	
	public function __construct($table)
	{
		$this->setTable($table);
		$this->connection = new Connection();
	}
		
	public function getTable() { return $this->table; }
	public function setTable($name) { $this->table = '`' . $name . '`'; }
	public function getConnection() { return $this->connection; }

	// query templates
	public function getAll()
	{
		$result_array = array();
		$result = parent::query('select * from ' . $this->table);
		while ($record = $result->fetch_object()) { array_push($result_array, $record); }
		return $record;
	}
	public function getByID($id)
	{
		return parent::query('select * from ' . $this->table . ' where id = ' . $id)->fetch_object();
	}
	public function getWhere($where)
	{
		$result_array = array();
		$result = parent::query('select * from ' . $this->table . ' where ' . $where);
		while ($record = $result->fetch_object()) { array_push($result_array, $record); }
		return $record;
	}

	public function update($setterList, $where)
	{
		$setterString = "";
		for ($i = 0; $i < count($setterList); $i++)
		{
			$setterString .= $setterList[$i][0] . " = " . $setterList[$i][1];
			if ($i <= count($setterList) - 1) { $setterString .= ", "; }
		}
		parent::query('update ' . $this->table . ' set ' . $setterString . ' where ' . $where);
	}
}

?>

