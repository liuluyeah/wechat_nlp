<?php

exec("python ../python/checkNew.py");

$handle = fopen("newFriends.txt", "r");

http_response_code(200);
header("Content-type: application/json");

$newFriends = array();

while($friend = fgets($handle)) {
	array_push($newFriends, $friend);
}

echo json_encode($newFriends);

fclose($handle);

?>