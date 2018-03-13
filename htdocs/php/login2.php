<?php

if (!file_exists("QR.png"))
	exec("python ../python/login.py > login.log 2>&1 &");

?>