<?php

require __DIR__ . '/../classes/SqlQuery.php';
require __DIR__ . '/../classes/ApiEndpoint.php';

class Endpoint extends ApiEndpoint {
     function get($request) {
        $db = new SqlQuery();
        $queryString = 'SELECT * FROM "users"';

        if(!empty($request['id'])) {
            $id = $db->escape($request['id']);
            $queryString .= ' WHERE "id" = ' . $id;
        }

        $queryString .= ';';
        $db->query($queryString);
        return array($db->status, $db->result);
     }

     function post($request) {
        $db = new SqlQuery();
    
        $keys = array();
        $values = array();

        $whitelist = array(
            'name',
            'pin',
            'card',
            'facility',
        );

        foreach($request as $key => $value) {
            if(!empty($value) && in_array($key, $whitelist)) {
                $value = $db->escape($value);

                array_push($keys, '"' . $key . '"');
                array_push($values, '\'' . $value . '\'');
            }
        }

        if(in_array('"name"', $keys)) {
            $queryString = 'INSERT INTO "users" ( ' . implode(', ', $keys) . ' ) ';
            $queryString .= 'VALUES ( ' . implode(', ', $values) . ' );';
        
            $db->query($queryString);
            return array($db->status, $db->result);
        } else {
            return array(400, array(
                'error' => 'missing required "name"'
            ));
        }
    }

    function put($request) {
        if(!empty($request['id'])) {
            $db = new SqlQuery();
            $id = $db->escape($request['id']);

            $combined = array();

            $whitelist = array(
              'name',
              'pin',
              'card',
              'facility',
            );
      
            foreach($request as $key => $value) {
              if(!empty($value) && in_array($key, $whitelist)) {
                $value = $db->escape($value);
      
                array_push($combined, '"' . $key . '" = \'' . $value . '\'');
              }
            }

            if(count($combined) > 0) {
                $queryString =  'UPDATE "users" SET ' . implode(', ', $combined) . '  WHERE "id" = ' . $id . ';';

                $db->query($queryString);
                return array($db->status, $db->result);
            } else {
                return array(400, array(
                    'error' => 'missing input'
                ));
            }
        } else {
            return array(400, array(
                'error' => 'missing id'
            ));
        }
    }

    function delete($request) {
        if(!empty($request['id'])) {
            $db = new SqlQuery();
            $id = $db->escape($request['id']);

            $queryString = 'DELETE FROM "users" WHERE "id" = ' . $id . ';';

            $db->query($queryString);
            return array($db->status, $db->result);
        } else {
            return array(400, array(
                'error' => 'missing id'
            ));
        }
    }
}
