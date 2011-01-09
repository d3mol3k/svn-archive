<?php

include ('../lib/functionsnew.php');
include('otv_funcs.php');

session_start();


if(!isset($_SESSION["gatekeeper"]))
{
   	header("HTTP/1.1 401 Unauthorized"); 
}
else
{
	$cleaned = clean_input($_GET);
    $conn=pg_connect("dbname=gis user=gis");
	$sess_cond = (isset($cleaned["pssn"])) ?  
		" AND photosession=$cleaned[pssn] ": "";
	$q=("SELECT pan.*,AsText(ann.xy) FROM panoramas pan ".
					",annotations ann WHERE pan.userid=".
						"$_SESSION[gatekeeper] AND pan.parent IS NULL ".
						"AND ann.id=pan.annid ".
						"$sess_cond ORDER BY pan.id DESC ".
						"LIMIT $cleaned[n] OFFSET ". 
							($cleaned["pg"]*$cleaned["n"]));
	$result=pg_query($q);

	$result_all=pg_query
		("SELECT * FROM panoramas WHERE userid=$_SESSION[gatekeeper] AND ".
		"parent IS NULL $sess_cond");
	$num_photos=pg_num_rows($result_all);

	$data = array();
	if(($cleaned['pg']+1)*$cleaned['n'] >= $num_photos)
		$data['lst'] = 1;

	while($row=pg_fetch_array($result,null,PGSQL_ASSOC))
	{
		$curRow = array();
		$curRow['x']=$curRow['y']=0;
		$m=array();
		if($row['astext']!=null)
		{
		$a = preg_match ("/POINT\((.+)\)/",$row['astext'],$m);
		list($curRow['x'],$curRow['y'])= explode(" ",$m[1]);
		}
			
		$curRow["id"] = $row["id"];
		$curRow["ispano"] = ($row["ispano"])?1:0;

		$result2=pg_query("SELECT * FROM panoramas WHERE parent=".
							"$row[id]");
		$curRow["parent"] = (pg_num_rows($result2)>0) ? true:false;
		$data['photos'][] = $curRow;
	}

	pg_close($conn);

	header("Content-type: application/json");
	echo json_encode($data);
}

?>
