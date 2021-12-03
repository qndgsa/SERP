<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Demo</title>
</head>
<body>

<h1>Cookie demo</h1>

<p>This demo shows how you can create a cookie with Javascript (using jQuery), and read it with PHP.</p>

<?php

/* THIS PORTION IS EXECUTED ON THE SERVER */

// if the cookie "myCookie" is set
if(isset($_COOKIE['myCookie'])){
    echo "<p><b>PHP found this value for <i>myCookie</i>: " .  $_COOKIE['myCookie'] . "</b></p>";
}
else{
    echo "<p><b>PHP did not find a value for <i>myCookie</i>. Give it a value below.<b></p>";
}

?>

<input type="text" id="myInput"/><button id="myButton">Change the cookie value using JS</button>

<!-- make sure you load jQuery and the jQuery cookie plugin -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>

<script>

    /* THIS PORTION OF CODE IS ONLY EXECUTED WHEN THE USER SEES THE PAGE (CLIENT-SIDE) */

    $(function(){
        $('#myButton').click(function(){
            $.cookie('myCookie', $('#myInput').val());
            alert(
                'The value of myCookie is now "'
                + $.cookie('myCookie')
                + '". Now, reload the page, PHP should read it correctly.'
            );
        });
    });

</script>
</body>
</html>