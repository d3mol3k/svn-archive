<?php
include('header.php.inc');
?>
<center>

<h3 class="tablelabel">Edits<!-- so far-->:</h3>

<table border="0" id="list">
<tr>
  <th>time (latest first)</th>
  <th>optype</th>
  <th>element</th>
  <th>user</th>
  <th>changeset</th>
</tr>

<?php

$results = $db->query('SELECT timestamp, op_type, element_type, osm_id, user_name, changeset FROM edits ORDER BY timestamp DESC LIMIT 500');
while ($data = $results->fetchArray()) {
   $timestamp    = $data[0];
   $optype       = $data[1];
   $element_type = $data[2];
   $osm_id       = $data[3];
   $user         = $data[4];
   $changeset    = $data[5];
   
   $timestamp = eregi_replace("T", " at ", $timestamp);
   $timestamp = eregi_replace("Z", "", $timestamp);             
   
   $timestamp = eregi_replace("Z", "", $timestamp);
   
   $user_url = urlencode($user);
   $user_url = str_replace("+", "%20", $user_url);
   
   print "<tr>";
   print "<td>".$timestamp."</td>";
   print "<td>".$optype."</td>";
   print "<td><a href=\"http://www.openstreetmap.org/browse/$element_type/$osm_id\" title=\"browse the OpenStreetMap element\">$element_type:$osm_id</a></td>";
   print "<td><a href=\"http://www.openstreetmap.org/user/".$user_url."\" title=\"osm user page\">$user</a></td>";
   print "<td><a href=\"http://www.openstreetmap.org/browse/changeset/".$changeset."\">$changeset</a></td>\n";
   print "</tr>\n";                          
      
}            
?>

</td></tr>
</table>
</center>
<?php
include('footer.php.inc');
?>
