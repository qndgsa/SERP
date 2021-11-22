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


if(!empty($_COOKIE["user"])){
    $amazon_id = $_COOKIE["user"];

    if(isset($_COOKIE["continue"])){
        setcookie("continue", '');

        $s ="SELECT * FROM serp.round_robin WHERE amazon_id = \"". $amazon_id."\"";
        $html_list = mysqli_query($db_connection,$s);
        while($row = mysqli_fetch_array($html_list)){
            $url = $row["URL"];
            $query = $row["query"];
            $sequence = $row["sequence"];
            $topic0 = $row["topic0"];
            $topic1 = $row["topic1"];
            $done = $row["done"];
            if($done == 0){
                setcookie("url", $url, $expire,'/');
                setcookie("query", $query, $expire,'/');
                setcookie("sequence", $sequence, $expire,'/');
                setcookie("topic0", $topic0, $expire,'/');
                setcookie("topic1", $topic1, $expire,'/');

                echo "
                <script>
                    alert('Welcome back, you test will continue! ');
                    window.location.href='knowledge.php';
                </script>";
            }
        }

    }else{
//        $insert = $db_connection->prepare("UPDATE serp.user_config SET knowledge = 0 WHERE amazon_id = ?");
//        $insert->bind_param("s", $amazon_id);
//        $insert->execute();

        $s ="SELECT * FROM serp.round_robin WHERE amazon_id = \"". $amazon_id."\"";
        $html_list = mysqli_query($db_connection,$s);
        while($row = mysqli_fetch_array($html_list)){
            $url = $row["URL"];
            $query = $row["query"];
            $sequence = $row["sequence"];
            $done = $row["done"];
            $topic0 = $row["topic0"];
            $topic1 = $row["topic1"];

            if($done == 0){
                setcookie("url", $url, $expire,'/');
                setcookie("query", $query, $expire,'/');
                setcookie("sequence", $sequence, $expire,'/');
                setcookie("topic0", $topic0, $expire,'/');
                setcookie("topic1", $topic1, $expire,'/');

                echo "
                <script>
                    alert('Thank you for participating, you test will start now! ');
                    window.location.href='knowledge.php';
                </script>";
                break;
            }
        }
    }

//    else if(isset($_COOKIE['knowledge'])&&$_COOKIE['knowledge'] == "yes"){
//        $insert = $db_connection->prepare("UPDATE serp.user_config SET knowledge = 1 WHERE amazon_id = ?");
//        $insert->bind_param("s", $amazon_id);
//        $insert->execute();
//        echo "
//        <script>
//            alert('Thank you for participating, but the test is not available at is moment.');
//            window.location.href='index.html';
//        </script>";
//    }else{
//        header("location:index.html");
//    }
}else{
    echo "
        <script>
            alert('Please login first!');
            window.location.href='index.html';
        </script>";
}
mysqli_close($db_connection);

