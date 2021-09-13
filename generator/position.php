<html>

<?php
session_start();
require_once('./library.php');
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);

$user_id=$_POST["user_id"];;
$exp_id=$_POST["exp_id"];;
$x=$_POST["x"];;
$y=$_POST["y"];;
$action=$_POST["action"];;

$query=" INSERT INTO  serp.user_mouse (exp_id, user_id, x, y, date)VALUES($exp_id,$user_id,$x,$y,date("Y-m-d H:i:s"))";
$result=mysql_query($query);


?>


</html>