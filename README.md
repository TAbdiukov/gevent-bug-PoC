# gevent-bug-PoC
Proof of Concept of a bug present in Gevent but not Flask

This is the Minimal Reproducible Example (MRE) to reproduce this bug. I also added a workaround function.

Discussion [on Google Groups](https://groups.google.com/g/gevent/c/s5yWD3GSPc0)

## The problem

Gevent, unlike Flask, incorrectly handles proxy requests (where the WSGI server operates as a proxy).

The bug manifests itself in `request.url`, but may also affect other logic

```
Expected: http://frogfind.com/hello/?q=foobar
Reality: http://frogfind.com/http://frogfind.com/hello/?q=foobar
```

**Note:** The URL is correct in stdout, but incorrect in the variable.

## Steps to reproduce

For the demo, I use this URL: `http://frogfind.com/?q=foobar`

### Usual steps

1. git clone
2. cd
3. pip install -r requirements

### Set up browser HTTP proxy

For example, I will use Firefox + FoxyProxy
1. [Get FoxyProxy](https://getfoxyproxy.org/downloads/)) ("Proxy Downloads & Instructions - FoxyProxy Standard")
2. Set up HTTP proxy on `127.0.0.1` port `5000`. Refer to the screenshot below,

![74b635a8069290ad6b7e3c253cb01efd.png](/_images/74b635a8069290ad6b7e3c253cb01efd.png)

### Observe no bug in Flask

1. Run app using Flask, `python main.py -s flask` 
2. Access `http://frogfind.com/?q=foobar` via proxy.

![ab88cfb5700839316761071489c26f8a.png](/_images/ab88cfb5700839316761071489c26f8a.png)

### Observe bug in Gevent

1. Run app using Gevent, `python main.py -s gevent` or just `python main.py`
2. Access `http://frogfind.com/?q=foobar` via proxy.

![70622f591543b8206f61f95f79ba1c0f.png](/_images/70622f591543b8206f61f95f79ba1c0f.png)

-------------------------------
**Tim Abdiukov**
