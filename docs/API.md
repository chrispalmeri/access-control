# API

## users

### POST /users

Request

Only `name` is required

```json
{
    "name": "First Last",
    "pin": "0000",
    "card": 23456,
    "facility": 789
}
```

Response 200 or 422

### GET /users

Response 200

```json
[
    {
        "id": 1,
        "name": "First Last",
        "pin": "0000",
        "card": 23456,
        "facility": 789
    }
]
```

### GET /users/{id}

Response 200 or 404

```json
{
    "id": 1,
    "name": "First Last",
    "pin": "0000",
    "card": 23456,
    "facility": 789
}
```

### PUT /users/{id}

Request

Provide at least one property

```json
{
    "name": "First Last",
    "pin": "0000",
    "card": 23456,
    "facility": 789
}
```

Response 200 or 404 or 422

### DELETE /users/{id}

Response 204

## events

### GET /events

Response 200

```json
[
    {
        "id": 1,
        "time": "2021-03-06T18:32:19.961Z",
        "channel": "DEBUG",
        "message": "User 2 created"
    }
]
```

## update

### GET /update

not implemented

### POST /update

not implemented

## database

### GET /database

not implemented

### POST /database

not implemented

## reboot

### POST /reboot

not implemented

# Errors

Response 500

```json
{
    "error": "Something went wrong"
}
```
