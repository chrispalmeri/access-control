# To do

## Layout Changes

  * add connection diagram or image
  * check that diptrace setup is repeatable
  * brief directions, plus link to Mouser project

## Code changes

  * DEBUG messages for user edited, user deleted
  * api endpoint to get last unknown card (from logs)
  * "Connected" styling

you are not using svelte-spa-router for anything yet  
not sure if $users in two places is ideal in UserList

  * move api docs from `docs` to `/api` component
  * add database restored event log - at least show if restore completed, currently no feedback
    * obviously refresh events afterward
  * Authentication
  * refactor events (differentiate specific status from operational event)
    * entry made, door propped, door forced - independent of door open/close
    * lock unlocked/locked - independent of user validated
    * led on, led off
    * buzzer
    * login/logout
    * http?
  * if it gets laggy then edit webhook to send event - so web does not need to hit api every time
  * rename event channels like physicalAccess,remoteAccess,serverStatus,hardwareStatus,humanResources,codeDebug
  * user export/import csv
    * so, basically just break db backup/restore into two - users, and events - that's all that is is the db anyway
  * include state in websocket data instead of generic notification
  * 'gpio' package, change 'entry' to 'output'
  * increasing timeout for bad pin or card attempts
  * reboot command
  * upgrade command
  * beep or something on startup, so you know when it is ready after a power cycle
  * add control buttons on homepage, would need api first
  * ping websocket periodically, power loss still shows connected
  * way to delete events
  * websocket connects/disconnects when firefox scrapes a page preview - auth would stop that

## Dev setup

  * move `install.sh` into `backend/` ?
  * log ip address
  * smarter install/update script depending on what changed
  * split docs/make consistent for each windows dev, orange pi stage, nano pi prod
  * add git cheatsheet to various-scripts repo

## Ideas

  * make a simple and an advanced version, neo is cheaper than neo core
  * slim project box instead of in-wall
  * use 3.3 from board instead of 5v divider on contacts
  * transistor or resistor arrays

Would it be possible to go to doorctl.com
and have it connect websockets to any devices on local network?
and somehow sign in to all of them
that would be super cool

---

aiohttp want you to do state like this
but your 'device' stuff is pretty separated from 'app'

```py
app['database'] = conn
app['broadcaster'] = broadcast
```

---

`return web.json_response({'error': '404: Not Found'}, status=404)` seems better than
`raise web.HTTPNotFound()`

but maybe need a try/catch middleware instead of changing it everywhere
https://github.com/yuvalherziger/aiohttp-catcher

I don't know if you can provide the "allowed methods" thing using `json_response`

<!--
also this doesn't work
`raise web.HTTPBadRequest(body=None, content_type=None)`
cause there is a bug where `body` cannot be a string (it's bytes, or maybe a full response object)
and `content_type` doesn't affect default response either
-->

---

you usually get a hardware loop startup log in webui on restart.
i guess it gets hit with a last websocket, and then hits the api,
but the api doesn't respond til service is back up.

...so why don't you try to reconnect automatically
