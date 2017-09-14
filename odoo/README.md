
```python
$ cp fabfile.py <odoo_src_path>
```

```python
$ python make_odoo_minify.py <own_addons_path> <odoo_src_path>
```
this will collect minify odoo with required addons in current dir
and create a direcotry 'odoo_yyyy-mm-dd'

```python
$ cd <odoo_yyyy-mm-dd>
$ fab -l   # this will show the deploy command
$ fab deploy_ubuntu -H <host,host> -u <username> -p <password> -P
```
If you only have to deploy code to only one machine `-P` is not required.


