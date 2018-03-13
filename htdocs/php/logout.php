<?php

exec("python ../python/logout.py");
exec("rm itchat.pkl");
exec("rm QR.png");
exec("rm chatrooms.txt");
exec("rm reply.log");
exec("rm login.log");
exec("cat robot.pid | xargs /bin/kill -2");
exec("rm robot.pid");
exec("rm friendList.txt");
exec("rm newFriends.txt");
exec("rm -r ReceivedMsg/");
exec("rm -r RevokedMsg/");


?>