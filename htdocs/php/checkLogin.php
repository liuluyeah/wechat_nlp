<?php

$handle = popen("python ../python/checkLogin.py", "r");
$state = fread($handle, 10);
pclose($handle);


http_response_code(200);
header("Content-type: application/json");

$ret = array();
if ($state == 200) {

	$ret["loginState"] = 200;

} else {

	if (file_exists("itchat.pkl"))
		$ret["loginState"] = 201;

	else if (file_exists("QR.png"))
		$ret["loginState"] = 400;

	else
		$ret["loginState"] = 404;
}

echo json_encode($ret);

?>