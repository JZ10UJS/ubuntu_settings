# download and install shadowsocks-qt5

```sh
$ sudo add-apt-repository ppa:hzwhuang/ss-qt5
$ sudo apt-get update
$ sudo apt-get install shadowsocks-qt5

```

if dependency error of "libappindicator1"

```sh
sudo apt-get -f install libappindicator1 libindicator7

```

then reinstall shadowsocks-qt5


# set ss config

open ss client, File > "Import configuration from gui-config.json".
select the gui-config.json, will load the ss account infomation.

then set the proxy pac. in ubuntu,
System settings > Network > Network Proxy, select the "Automatic" method,
and the URL e.g. file:///home/<your_name>/Documents/ss/auto.pac


# SSR

`
python local.py -s us01.fk360.bid -p 51416 -k LyUTo7 -m aes-256-cfb -o auth_sha1_v4 -O tls1.2_ticket_auth -v

python local.py -s us.vonc.tk -p 37997 -k IHZAUm -m aes-256-cfb -o auth_sha1_v4 -O tls1.2_ticket_auth -v
`