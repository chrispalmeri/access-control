<?php

$command = "git pull && rsync -av --delete --delete-excluded --include='php/***' --include='python/***' --include='www/***' --filter 'protect database.db' --exclude='*' /home/www-data/door-control/ /srv/door-control/ 2>&1";
$output = array();
$result = '';

chdir('/home/www-data/door-control');
exec($command, $output, $result);

$response = array(
    'directory' => getcwd(),
    'command' => $command,
    'output' => $output,
    'result' => $result
);

$json = json_encode($response);

header('Content-Type: application/json');
header('Cache-Control: no-cache');
print_r($json);
