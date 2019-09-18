<?php

$command = 'git pull && rsync -av --delete code/ /var/www/html 2>&1';
$output = array();
$result = '';

chdir('/var/tmp/access-control');
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
