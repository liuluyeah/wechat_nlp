<?php

if (!file_exists("QR.png") && !file_exists("itchat.pkl"))
	exec("python ../python/login.py > login.log 2>&1 &");

?>