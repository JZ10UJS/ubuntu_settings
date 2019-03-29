# ubuntu theme

install Flatabulous theme

see website "http://www.jianshu.com/p/463f229c0a20"


# iptables add rule

```sh

$ iptables -I INPUT -p tcp -m multiport --dports 8088 -m comment --comment "zhangjie horizon test port" -j ACCEPT
$ service iptables save

```


# switch css

```html
<html>
<head>
<style>
.switch {
    display: inline-block;
    position: relative;
    width: 63px;
    margin: 6px 0 0;
}

.switch input {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 24px;
    z-index: 5;
    opacity: 0;
    cursor: pointer;
    margin: 0;
}

.switch label {
    position: relative;
    display: inline-block;
    -webkit-transition: 0.4s;
    transition: 0.4s;
    background: #f6f6f6;
    border: 1px solid #e5e5e5;
    border-radius: 11px;
    height: 22px;
    width: 53px;
    margin: 0;
}

.switch label:after {
    content: '';
    position: absolute;
    top: 2px;
    left: 3px;
    z-index: 2;
    background: #bcbcbc;
    width: 18px;
    height: 18px;
    border-radius: 100%;
    -webkit-transition: 0.6s;
    transition: 0.6s;
}
.switch input:checked + label {
    background-color: #1c5a80;
    border-color: #1c5a80;
}

.switch input:checked + label:after {
    left: 32px;
    background-color: #ffffff;
}
</style>
</head>
<body>
<div class="switch">
    <input type="checkbox" id="batchSwitcher">
    <label></label>
</div>
</body>
</html>
```

# python profile
``` py
from functools import wraps
import cProfile

class profile(object):
    def __init__(self, fname=None):
        self.fname = fname

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            profile = cProfile.Profile()
            result = profile.runcall(f, *args, **kwargs)
            profile.dump_stats(self.fname or ("%s.cprof" % (f.func_name,)))
            return result

        return wrapper

p = profile("zj_profile.cprof")
def fib(n):
    if n < 3:
        return 1
    return fib(n-1) + fib(n-2)
fib = p(fib) # 将要profile的函数，进行wrap
fib(20)  # 调用函数，函数执行完毕后，创建出 zj_profile.cprof 文件
```
```sh
$ pip install flameprof
$ flameprof --format=log zj_profile.cprof | ./flamegraph.pl > func_flame.svg
```
