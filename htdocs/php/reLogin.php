<?php

exec("python ../python/logout.py");
exec("rm itchat.pkl");
exec("rm QR.png");
exec("rm chatrooms.txt");
exec("rm reply.log");
exec("python ../python/login.py > login.log 2>&1 &");

?>