<?php
ini_set("display_errors", "stderr");

error_reporting(E_ALL);

$SERVER = 'hcdm3.cs.virginia.edu';
$USERNAME = 'zw3hk';
$PORT = 3306;
$PASSWORD = 'Fall2021!!';
$DATABASE = 'serp';
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);
$expire = time() + 60 * 60 * 24; //1day

if (!empty($_COOKIE["user"])){
//    if(isset($_COOKIE['knowledge'])&&$_COOKIE['knowledge'] == "yes"){
//        setcookie("knowledge", "");
//        $str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
//        $len = strlen($str)-1;
//        $random_str = '';
//        for ($i=0;$i<8;$i++) {
//            $num=mt_rand(0,$len);
//            $random_str .= $str[$num];
//        }
//
//        $zero = 0;
//        $time = "N/A";
//        $feedback = "knowledge exist";
//
//        $insert_basic = $db_connection->prepare("INSERT INTO serp.exp_data (exp_id, user_id, test_url, window_width, window_height, query, sequence, start, end, feedback)VALUES(?,?,?,?,?,?,?,?,?,?);");
//        $insert_basic->bind_param("ssssssssss", $random_str, $_COOKIE["user"], $_COOKIE["url"], $zero, $zero,$_COOKIE["query"],$_COOKIE["sequence"], $time, $time, $feedback);
//        $insert_basic->execute();
//
//    } else
    if (isset($_COOKIE['basic'])&&isset($_COOKIE['user_action'])&&isset($_COOKIE['user_view'])&&isset($_POST['feedback'])&&isset($_COOKIE['knowledge'])){
        setcookie("knowledge", "");
        $basic = json_decode($_COOKIE['basic']);
//        $mouse_movement = json_decode($_COOKIE['mouse_movement']);
        $user_action = json_decode($_COOKIE['user_action']);
        $user_view = json_decode($_COOKIE['user_view']);

//        foreach ($mouse_movement as $postion){
//            $insert = $db_connection->prepare("INSERT INTO  serp.user_mouse (exp_id, user_id, x, y, date)VALUES( ?, ?, ?, ?, ?)");
//            $insert->bind_param("sssss", $basic[1], $basic[0], $postion[0], $postion[1], $postion[2]);
//            $insert->execute();
//        }

        $insert_basic = $db_connection->prepare("INSERT INTO serp.exp_data (exp_id, user_id, test_url, window_width, window_height, query, sequence, start, end, knowledge, feedback)VALUES(?,?,?,?,?,?,?,?,?,?,?);");
        $insert_basic->bind_param("sssssssssss", $basic[0], $_COOKIE["user"], $_COOKIE["url"], $basic[1], $basic[2],$_COOKIE["query"],$_COOKIE["sequence"], $basic[3], $basic[4], $_COOKIE['knowledge'], $_POST['feedback']);
        $insert_basic->execute();

        $update_used = $db_connection->prepare("UPDATE serp.config_data SET answered = answered + 1 WHERE URL = ?");
        $update_used->bind_param("s", $_COOKIE["url"]);
        $update_used->execute();


        foreach ($user_action as $action){
        //            if ($action[1] == "close_page"){
        //                $insert_action = $db_connection->prepare("INSERT INTO serp.user_action(exp_id, user_id, action, link_id, date)VALUES(?,?,?,?,?)");
        //                $insert_action->bind_param("sssss", $basic[0], $_COOKIE["user"], $action[1], $action[0], $action[2]);
        //                $insert_action->execute();
        //
        //                $update_action = $db_connection->prepare("UPDATE serp.exp_data SET end = ? WHERE exp_id = ?");
        //                $update_action->bind_param("ss",$action[2], $basic[1]);
        //                $update_action->execute();
        //            }else{
                $insert_action = $db_connection->prepare("INSERT INTO serp.user_action(exp_id, user_id, action, link_id, date)VALUES(?,?,?,?,?)");
                $insert_action->bind_param("sssss", $basic[0], $_COOKIE["user"], $action[1], $action[0], $action[2]);
                $insert_action->execute();
        //           }
        }

        foreach ($user_view as $view){
            $insert_view = $db_connection->prepare("INSERT INTO serp.user_view (exp_id, user_id, view, date)VALUES(?,?,?,?);");
            $insert_view->bind_param("ssss", $basic[1], $basic[0], $view[0], $view[1]);
            $insert_view->execute();
        }

        setcookie("basic", '');
        //setcookie("mouse_movement", '');
    }else{
        echo $_COOKIE['basic'];
        echo "<br>";
        echo $_COOKIE['user_action'];
        echo "<br>";
        echo $_COOKIE['user_view'];
        echo "<br>";
        echo $_POST['feedback'];
        echo "<br>";
        setcookie("url", "");
        setcookie("query", "");
        setcookie("sequence", "");
        setcookie("topic0", "");
        setcookie("topic1", "");
        setcookie("basic", '');
        setcookie("mouse_movement", '');

//        echo "
//        <script>
//            alert('Reading data error!');
//            window.location.href='index.html';
//        </script>";
    }
    setcookie("user_action", '');
    setcookie("user_view", '');

    $update_round_robin = $db_connection->prepare("UPDATE serp.round_robin SET done = 1 WHERE amazon_id = ? AND URL = ?");
    $update_round_robin ->bind_param("ss",$_COOKIE['user'], $_COOKIE['url']);
    $update_round_robin ->execute();

    setcookie("url", '');
    setcookie("query", '');
    setcookie("sequence", '');
    setcookie("topic0", "");
    setcookie("topic1", "");


    $s ="SELECT * FROM serp.round_robin WHERE amazon_id = \"". $_COOKIE['user']."\"";
    $html_list = mysqli_query($db_connection,$s);
    while($row = mysqli_fetch_array($html_list)){
        $next_url = $row["URL"];
        $query = $row["query"];
        $sequence = $row["sequence"];
        $topic0 = $row["topic0"];
        $topic1 = $row["topic1"];
        $done = $row["done"];

        if($done == 0){
            setcookie("url", $next_url, $expire,'/');
            setcookie("query", $query, $expire,'/');
            setcookie("sequence", $sequence, $expire,'/');
            setcookie("topic0", $topic0, $expire,'/');
            setcookie("topic1", $topic1, $expire,'/');

            echo "
                <script>
                    alert('Thank you! Please proceed to next test!');
                    window.location.href='knowledge.php';
                </script>";
            break;
        }
    }

    if(!mysqli_fetch_array($html_list)){
        $str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        $len = strlen($str)-1;
        $random_str = '';
        for ($i=0;$i<16;$i++) {
            $num=mt_rand(0,$len);
            $random_str .= $str[$num];
        }
        $update_finished = $db_connection->prepare("UPDATE serp.user_config SET finished = ? WHERE amazon_id = ?;");
        $update_finished ->bind_param("ss",$random_str, $_COOKIE['user']);
        $update_finished ->execute();

        //setcookie("user", "");
        setcookie("knowledge", "");
        setcookie("url", '');
        setcookie("query", '');
        setcookie("sequence", '');
        setcookie("topic0", "");
        setcookie("topic1", "");

        echo "
                <script>
                    alert('The test is finished,Thank you for participating. Don\'t forget to fill out the rest of the survey and enter your compilation verification code: $random_str');
                    window.location.href='index.html';
                </script>";
    }


} else {
    echo "
        <script>
            alert('Please login first!');
            window.location.href='index.html';
        </script>";
}
mysqli_close($db_connection);


