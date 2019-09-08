<?php

// Capture get and post data
$post = file_get_contents('php://input');
if(!empty($post)) {
  $data = json_decode($post, true);
}
foreach($_GET as $key => $value) {
  $data[$key] = $value;
}

// Capture info from url (/api/pins/led/on)
$string = preg_replace('/\?.*/', '', $_SERVER['REQUEST_URI']);
$parts = explode('/', $string);
if(array_key_exists(3, $parts)) {
  $resource = $parts[3];
}
if(array_key_exists(4, $parts)) {
  $data['state'] = $parts[4];
}

// GET /api/pins/led/on
// POST /api/pins/led/ {state: on}

$rmap = array(
  'led' => 3,
  'buzzer' => 2,
  'lock' => 6
);

$smap = array(
  'on' => 1,
  'off' => 0
);

$pin = $rmap[$resource];

// if no state then should return the current state

$command = 'gpio write ' . $pin . ' ' . $smap[$data['state']];

// 'gpio write 3 1' turn led on
// 'gpio write 3 0' turn led off

exec($command, $output, $result);

$response = array(
  'pin' => $pin,
  'command' => $command,
  'result' => $result
);

$json = json_encode($response);

header('Content-Type: application/json');
header('Cache-Control: no-cache');
print_r($json);
