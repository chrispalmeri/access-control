<?php

require __DIR__ . '/../classes/SqlQuery.php';
require __DIR__ . '/../classes/ApiEndpoint.php';

class Endpoint extends ApiEndpoint {
     function get($request) {
        $db = new SqlQuery();

        $queryString = 'SELECT * FROM "events";';

        $db->query($queryString);
        return array($db->status, $db->result);
     }
}
