<?php
ini_set("display_errors", "stderr");

error_reporting(E_ALL);

$SERVER = 'hcdm3.cs.virginia.edu';
$USERNAME = 'zw3hk';
$PORT = 3306;
$PASSWORD = 'Fall2021!!';
$DATABASE = 'serp';
$db_connection = new mysqli($SERVER, $USERNAME, $PASSWORD, $DATABASE);

setcookie("user", '');
setcookie("url", '');
setcookie("query", '');
setcookie("sequence", '');

$round_robin = [];
$expire = time() + 60 * 60 * 24; //1day
if (mysqli_connect_errno()) {
    echo "
        <script>
            alert('Failed to connect to MySQL');
            window.location.href='index.html';
        </script>";
}

if (isset($_POST['ID'])) {
    $amazon_id = $_POST["ID"];

    $find_user ="SELECT * FROM serp.user_config WHERE amazon_id = ?";
    $stmt = $db_connection->prepare($find_user);
    $stmt->bind_param("s", $_POST['ID']);
    $stmt->execute();
    $stmt->bind_result($id, $amazon,$finished);
    $result = $stmt->fetch();

    if($finished !=""){
        echo "
                <script>
                    alert('The test is finished, Thank you for participating. Don\'t forget to fill out the rest of the survey and enter your compilation verification code: $finished');
                    window.location.href='index.html';
                </script>";
    }
    else if (empty($result)) {
        $insert = $db_connection->prepare("insert into serp.user_config (amazon_id) values (?);");
        $insert->bind_param("s", $_POST["ID"]);
        $insert->execute();

//        $find_entry = mysqli_query($db_connection,"select entry_file from serp.config_query_data;");
//
//        while($entry = mysqli_fetch_row($find_entry)) {
//            $q = "SELECT URL,query,sequence,topic0, topic1 FROM serp.config_data WHERE entry_file =\"".$entry[0]."\" AND answered < 3 ORDER BY used ASC limit 1;";
            $q = "SELECT URL,query,sequence,topic0, topic1 FROM serp.config_data WHERE answered < 3 ORDER BY used ASC limit 1;";
//            $html_list = mysqli_query($db_connection, $q);
            $html_list = mysqli_query($db_connection, $q);
            while($row = mysqli_fetch_row($html_list)){
                $url = $row[0];
                $query = $row[1];
                $sequence = $row[2];
                $topic0 = $row[3];
                $topic1 = $row[4];

                $update_used = $db_connection->prepare("UPDATE serp.config_data SET used = used + 1 WHERE URL = ?");
                $update_used->bind_param("s", $url);
                $update_used->execute();

                $insert = $db_connection->prepare("insert into serp.round_robin (amazon_id, URL, query ,sequence, topic0, topic1) values (?, ?, ?, ?, ?, ?);");
                $insert->bind_param("ssssss", $amazon_id,$url, $query, $sequence, $topic0, $topic1);
                $insert->execute();
            }
//        }

        setcookie("user", $amazon_id, $expire);
        header("Location: start.php");
    }else{
        setcookie("user", $amazon_id, $expire);
        setcookie("continue", "ture", $expire);
        header("Location: start.php");
    }

}else{
    echo "
        <script>
            alert('Error on read user!');
            window.location.href='index.html';
        </script>";
}
mysqli_close($db_connection);
?>