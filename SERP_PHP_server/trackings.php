<?php
session_start();
ini_set("display_errors", "stderr");

error_reporting(E_ALL);

//if (isset($_COOKIE['basic'])){
    //$basic = json_decode($_COOKIE['basic']);
if(isset($_COOKIE['user_action'])){
    $array =json_decode($_COOKIE['user_action']);
    $pos = $_GET['pos'];
    $t = date("m/d/Y, h:i:s A");
    $action = 'click link';
    $arr = [$pos, $action, $t];
    array_push($array,$arr);
    setcookie("user_action",  json_encode($array));
}else{
    $pos = $_GET['pos'];
    $t = date("m/d/Y, h:i:s A");
    $action = 'click link';
    $tamp = [$pos, $action, $t];
    $array = [$tamp];
    setcookie("user_action",  json_encode($array));
}
setcookie("clicked",  "yes");



//    $insert_action = $db_connection->prepare("INSERT INTO serp.user_action (exp_id, user_id, action, link_id, date) VALUES(?,?,?,?,?);");
//    $str1 = "test";
//    $insert_action->bind_param("sssss", $str1, $str1, $action, $pos, $t);
//    $insert_action->execute();
//    $insert_action->close();
//}
?>

