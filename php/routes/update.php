<?php

require __DIR__ . '/../classes/ApiEndpoint.php';

class Endpoint extends ApiEndpoint {
    function get($request) {
        $command = "git fetch && git status 2>&1";
        $output = array();
        $result = '';

        chdir('/home/www-data/door-control');
        exec($command, $output, $result);

        return array(200, array(
            'directory' => getcwd(),
            'command' => $command,
            'output' => $output,
            'result' => $result
        ));
    }

    function post($request) {
        $command = "git pull && rsync -av --delete --delete-excluded"
            . " --include='php/***' --include='python/***' --include='www/***'"
            . " --filter 'protect database.db' --exclude='*'"
            . " /home/www-data/door-control/ /srv/door-control/ 2>&1";
        $output = array();
        $result = '';

        chdir('/home/www-data/door-control');
        exec($command, $output, $result);

        return array(200, array(
            'directory' => getcwd(),
            'command' => $command,
            'output' => $output,
            'result' => $result
        ));
    }
}
