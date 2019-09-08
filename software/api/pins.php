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


$response = array(
  'pin' => $pin
);


// if POST
if ($data && $data['state']) {
  $command = 'gpio write ' . $pin . ' ' . $smap[$data['state']];
  exec($command, $output, $result);

  //$response['command'] = $command;
  //$response['result'] = $result;
}

// always
$response['value'] = exec('gpio read ' . $pin);


$json = json_encode($response);

header('Content-Type: application/json');
header('Cache-Control: no-cache');
print_r($json);
