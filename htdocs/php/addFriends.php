<?php

$chatroom = $_GET["add"];

exec("python ../python/addFriends.py ".$chatroom);

http_response_code(200);

?>