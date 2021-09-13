<html>

<?php
session_start();
require_once('./library.php');
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);

$user_id=$_POST["user_id"];;
$exp_id=$_POST["exp_id"];;
$window_width=$_POST["window_width"];;
$window_height=$_POST["window_height"];;
$test_url=$_POST["test_url"];;
$action=$_POST["action"];;

$query1="INSERT INTO serp.exp_data (exp_id, user_id, test_url, window_width, window_height, config_id, entry_config, start)VALUES($exp_id,$user_id,$test_url,$window_width,$window_height,$config_id,$sequence,date("Y-m-d H:i:s"));";
$result=mysql_query($query1);


?>


</html>