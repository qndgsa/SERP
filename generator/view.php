<html>

<?php
session_start();
require_once('./library.php');
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);

$user_id=$_POST["user_id"];;
$exp_id=$_POST["exp_id"];;
$view=$_POST["view"];;
$action=$_POST["action"];;

$query="INSERT INTO serp.user_view (exp_id, user_id, view, date)VALUES($exp_id,$user_id,$view,date("Y-m-d H:i:s"))";
$result=mysql_query($query);


?>


</html>