#!/usr/bin/python
# coding: utf-8

"""
Usage:
    fab deploy_ubuntu -H host1,host2 -u login_user -p password -P  # -P means execute code on all hosts in the same time
"""

from __future__ import with_statement

from fabric.api import *

tar_name = 'odoo-10.0.tar.gz'


def _download_req_src_code():
    with lcd('.'):
        local('mkdir pkg-src')
        cmd = ['pip', 'download', '-r', 'requirements.txt',
               '--no-binary', ':all:',
               '-i', 'https://pypi.douban.com/simple',
               '-d', 'pkg-src',
               '--no-cache-dir']
        local(' '.join(cmd))


def build():
    includes = ['addons', 'odoo', 'pkg-src', 'odoo-bin']
    excludes = [tar_name, 'fabfile*']
    with lcd('.'):
        with settings(warn_only=True):
            if local('test -d pkg-src').failed:
                _download_req_src_code()

        cmd = ['tar', '-czf', '%s' % tar_name]
        cmd.extend(['--exclude="%s"' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % tar_name
_REMOTE_BASE_DIR = '/usr/share/odoo'


def _copy_code():
    with settings(warn_only=True):
        if local('test -f %s' % tar_name).failed:
            build()

    new_deploy = False
    with settings(warn_only=True):
        if run('test -d %s' % _REMOTE_BASE_DIR).failed:
            sudo('mkdir -p %s' % _REMOTE_BASE_DIR)
            new_deploy = True

    # delete old tar file, and copy new
    run('rm -f %s', _REMOTE_TMP_TAR)
    put('%s' % tar_name, _REMOTE_TMP_TAR)

    # extract src code from tar file
    with cd(_REMOTE_BASE_DIR):
        sudo('tar -xzf %s' % _REMOTE_TMP_TAR)

    return new_deploy


def deploy_ubuntu():
    new_deploy = _copy_code()

    # install odoo dependencies
    if new_deploy:
        _install_u_dependencies()

    # 删除tar文件以及 pkg-src文件夹
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f %s' % _REMOTE_TMP_TAR)
        sudo('rm -rf pkg-src')


def _install_u_dependencies():
    with settings(warn_only=True):
        if run('test -d /usr/bin/pip').failed:
            _install_u_python_dependencies()
    with settings(warn_only=True):
        if run('test -d /usr/bin/psql').failed:
            _install_u_psql_dependencies()

    _install_u_odoo_dependencies()


def _install_u_python_dependencies():
    sudo('apt-get install -y python-dev python-pip')
    sudo('pip install -U pip')


def _install_u_psql_dependencies():
    sudo('apt-get install -y postgresql-client')


def _install_u_odoo_dependencies():
    depends = ['libldap2-dev', 'libsasl2-dev',  # python-ldap
               'libpq-dev',  # psycopg2
               'libxml2-dev', 'libxslt1-dev',  # libxml2 and lxml
               'libjpeg-dev',  # pillow
               'node-less',  # less
               'zlib1g-dev',  # for install python src pkg (.zip) type
               ]
    cmd = 'apt-get install -y ' + ' '.join(depends)
    sudo(cmd)

    with cd(_REMOTE_BASE_DIR):
        sudo('pip install pkg-src/* --no-index -f ./pkg-src ')


def deploy_centos():
    new_deploy = _copy_code()

    # _install_u odoo dependencies
    if new_deploy:
        _install_c_dependencies()

    # 删除tar文件以及 pkg-src文件夹
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f %s' % _REMOTE_TMP_TAR)
        sudo('rm -rf pkg-src')


def _install_c_dependencies():
    with settings(warn_only=True):
        if run('test -f /etc/yum.repos.d/epel.repo').failed:
            sudo('yum install -y epel-release')

    with settings(warn_only=True):
        if run('test -d /usr/bin/pip').failed:
            _install_c_python_dependencies()
    with settings(warn_only=True):
        if run('test -d /usr/bin/psql').failed:
            _install_c_psql_dependencies()

    _install_c_odoo_dependencies()


def _install_c_python_dependencies():
    sudo('yum install -y python-devel python-pip')
    sudo('pip install -U pip')


def _install_c_psql_dependencies():
    sudo('yum install -y postgresql-devel')


def _install_c_odoo_dependencies():
    depends = ['openldap-devel',
               'libxml2-devel', 'libxslt-devel',
               'libjpeg-devel',
               'nodejs-less', 'zlib-devel']
    cmd = 'yum install -y ' + ' '.join(depends)
    sudo(cmd)

    with cd(_REMOTE_BASE_DIR):
        sudo('pip install pkg-src/* --no-index -f ./pkg-src ')
