## Install

```bash
$ sudo pip install supervisor
# or you can install it with sudo apt-get install supervisor
```

## settings

```
$ sudo mkdir -p /etc/supervisor/conf.d   # this for put our own program settings
$ sudo mkdir -p /var/log/supervisor      # for logs
$ sudo su - root -c "echo_supervisord_conf > /etc/supervisor/supervisord.conf"
```

change the settings 

```
[supervisord]
...
logfile=/var/log/supervisor/supervisord.log
pidfile=/var/run/supervisord.pid
childlogdir=/var/log/supervisor
...

[include]  # add these two lines for add our own program settings
files=/etc/supervisor/conf.d/*.conf

```

## auto start 

file `/lib/systemd/system/supervisord.service`

```
[Unit]
Description=Process Monitoring and Control Daemon
After=rc-local.service

[Service]
Type=forking
ExecStart=/usr/local/bin/supervisord -c /etc/supervisor/supervisord.conf
SysVStartPriority=99

[Install]
WantedBy=multi-user.target

```

enable it

```bash
$ sudo systemctl enable supervisord.service
$ sudo systemctl start supervisord
```