<html>
<head>
<meta http-equiv="refresh" content="0; url=result.php" />
</head>>
<style>
#submitting
{
	margin-top: 250px;
	margin-left: 300px;
	height:100px;
	width:300px;
	border: solid brown 5px;
	text-align: center;
}
</style>
</head>
<body>
<div id="submitting" ><p text-align="center">
running</p>
<img src ="ajax-loader-answer.gif">
</div>

<?php 
$content = $_POST['content'];
$file = "file.cpp";
$Saved_File = fopen($file, 'w');
fwrite($Saved_File, $content);
fclose($Saved_File);
?>
</body>
</html>