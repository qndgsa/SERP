<html>

<?php
session_start();
require_once('./library.php');
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);

$user_id=$_POST["user_id"];;
$exp_id=$_POST["exp_id"];;
$link_id=$_POST["link_id"];;
$time=$_POST["time"];;
$action=$_POST["action"];;

if ($action == "close_page")
{
    $query=" UPDATE serp.exp_data SET end = date("Y-m-d H:i:s") WHERE exp_id = $exp_id";
    $result=mysqli_query($query);
}else{
    $query=" INSERT INTO  serp.user_mouse (exp_id, user_id, x, y, date)VALUES($exp_id,$user_id,$x,$y,date("Y-m-d H:i:s"))";
    $result=mysqli_query($query);
}




?>


</html>