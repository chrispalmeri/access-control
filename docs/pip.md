# pip

Package "python3-aiohttp" has old bug where background tasks are cancelled
before `app.on_shutdown` and `app.on_cleanup` run so they have no effect.

`sudo apt-get install -y python3-pip python3-dev`

`sudo pip3 install --system setuptools wheel aiohttp`

Not using pip "gpiod" because it is not the same as package "python3-libgpiod",
it does not have the same methods.

## Example

```
while keepon:
    await read(app)
```

```
async def shutdown(app):
    global keepon
    keepon = False
    await app['my_task']
```

```
app.on_shutdown.append(reader.shutdown)
```

However, `lines.event_wait()` can still raise "InterruptedError" no matter
how cleanly you do everything else, so I kinda don't care.

Using the packages and catching any errors is simpler, since the gpio interrupts
will get force stopped anyway.

## Future

The latest version (pip) of aiohttp takes 60 seconds to stop because it is
waiting for you to close websockets before it forces it. The package version bug
handily kills everything right away.
