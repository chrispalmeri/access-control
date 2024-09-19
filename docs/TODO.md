# To do

https://pages.nist.gov/800-63-3/sp800-63b.html#reqauthtype

revealable password field

per user salt
10,000 rounds pbk

+1 round using server secret salt, not stored in db

https://docs.python.org/3/library/hashlib.html#key-derivation

https://www.slingacademy.com/article/python-ways-to-hash-a-password/#Three_Ways_to_Hash_a_Password

https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md

https://scotthelme.co.uk/boosting-account-security-pwned-passwords-and-zxcvbn/

---

`apt get install python3-pyotp` https://github.com/pyauth/pyotp

need to store random_base32 in db

store last timestamp and code (or hash of code) to deny using the same one again

## Layout Changes

  * add connection diagram or image
  * check that diptrace setup is repeatable
  * brief directions, plus link to Mouser project

## Code changes

show database size - also is there a memory limit or anything?

  * DEBUG messages for user edited, user deleted
  * "Connected" styling
  * add database restored event log - at least show if restore completed, currently no feedback
    * obviously refresh events afterward
  * refactor events (differentiate specific status from operational event)
    * entry made, door propped, door forced - independent of door open/close
    * lock unlocked/locked - independent of user validated
    * led on, led off
    * buzzer
    * login/logout
    * http?
  * if it gets laggy then edit webhook to send event - so web does not need to hit api every time
    * pretty sure that won't happen and the complexity to keep the ui accurate won't be worth it
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

dip switch to send 12V to relay?
also, both 12V jack and terminals next to each other
label the switch with "double check your power draw first"

---

here's a werid thing, the socket can still be up, but api down,
cause of name resolution I guess, like network switch is up but router is down

--- 

https://packages.ubuntu.com/search?suite=default&section=all&arch=any&keywords=aiohttp&searchon=names

https://github.com/maximdanilchenko/aiohttp-apispec
