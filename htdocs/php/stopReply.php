<?php


exec("cat robot.pid | xargs /bin/kill -9");
exec("rm reply.log");
exec("rm robot.pid");

?>