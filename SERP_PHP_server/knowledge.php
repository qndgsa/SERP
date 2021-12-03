<html lang="en">
<head>
    <title>SERP</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css" rel="stylesheet">
    <!-- Material Design for Bootstrap -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.16/css/mdb.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0-alpha1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min.js"></script>

</head>
<style>
    @import url('https://fonts.googleapis.com/css?family=Josefin+Sans&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        list-style: none;
        font-family: 'Josefin Sans', sans-serif;
    }

    body {

    }

    .login-box {
        width: 780px;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: #000000;
    }

    .login-box h1 {
        float: left;
        font-size: 40px;
        border-bottom: 6px solid #000000;
        margin-bottom: 50px;
        padding: 13px 0;
    }

    .textbox {
        width: 100%;
        overflow: hidden;
        font-size: 20px;
        padding: 8px 0;
        margin: 8px 0;
        border-bottom: 1px solid #000000;
    }

    .textbox i {
        width: 26px;
        float: left;
        text-align: center;
    }

    .textbox input {
        border: none;
        outline: none;
        background: none;
        color: #000000;
        font-size: 18px;
        width: 80%;
        float: left;
        margin: 0 10px;
    }


</style>
<body>
<script>
    function no() {
        $.cookie('knowledge', "no");
        window.location.href = $.cookie('url');
    }

    function yes() {
        $.cookie('knowledge', "yes");
        window.location.href = $.cookie('url');
    }
</script>
<br>
<div class="login-box">
    <div class="container">
        <div class="jumbotron cloudy-knoxville-gradient">
            <div class="container">
                <h3>In next part you will be requested to evaluate the efficiency of <span style="color: #3875d7"
                            ><?php echo $_COOKIE['topic1']; ?></span> in treating <span style="color: #993333"
                            ><?php echo $_COOKIE['topic0']; ?></span>.
                </h3>
                <br>
                <h3> Please use the links in next page to determine the answer to the question presented in the query box. When you are confident in the answer, click the “Answer Question” button
                </h3>
                <br>
                <p>Before you continue, please answer this question:</p>
                <h2>Do you have pre-existing knowledge regarding above treatment? </h2>
            </div>
            <div class="row">
                <div class="col">
                    <button class="btn tempting-azure-gradient" onclick="yes()">Yes, I do</button>
                </div>
                <div class="col">
                    <button class="btn peach-gradient" onclick="no()">Not a lot</button>
                </div>
                <div class="col">
                    <button class="btn young-passion-gradient" onclick="no()">None</button>
                </div>
            </div>
        </div>
    </div>
</div>

</body>