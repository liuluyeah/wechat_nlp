<?php

exec("python ../python/autoReply.py > reply.log 2>&1 & echo $! > robot.pid");

?>