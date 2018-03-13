<?php

exec("python ../python/updateChatroom.py");

$handle = fopen("chatrooms.txt", "r");

http_response_code(200);
header("Content-type: application/json");

$chatrooms = array();

while($chatroom = fgets($handle)) {
	array_push($chatrooms, $chatroom);
}

echo json_encode($chatrooms);

fclose($handle);

?>