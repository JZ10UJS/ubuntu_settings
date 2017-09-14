#!/usr/bin/python
# coding: utf-8

"""
为了方便最小化打包odoo的各项addon

"""

import shutil
import datetime
import os
import sys
import subprocess
from os.path import join as path_join

depends = set([])
copy_paths = set([])
handled_addons = set([])


def handle_addon(path, addon, flag=False):
    print 'handing addon: %s %s' % (addon, '' if not flag else '\tauto install...') 
    if addon != 'base':
        copy_paths.add(path)
    with open(path_join(path, '__manifest__.py')) as f:
        config = eval(f.read())
        for d in config['depends']:
            if d not in handled_addons:
                depends.add(d)
    handled_addons.add(addon)
    addon in depends and depends.remove(addon)


def handle_auto_install(path):
    updated = True
    while updated:
        for d in os.listdir(path):
            if d not in handled_addons and os.path.exists(path_join(path, d, '__manifest__.py')):
                with open(path_join(path, d, '__manifest__.py')) as f:
                    config = eval(f.read())
                    if config.get('auto_install') and all(i in handled_addons for i in config['depends']):
                        handle_addon(path_join(path,d), d, True)
                        updated = True
                        break
        else:
            updated = False


def handle_own_path(op):
    for d in os.listdir(op):
        if d not in handled_addons and os.path.exists(path_join(op, d, '__manifest__.py')):
            handle_addon(path_join(op, d), d)
    handle_auto_install(op)


def handle_with_src(src_path):
    src_addon_path = [os.path.join(src_path, 'addons'), os.path.join(src_path, 'odoo/addons')]
    while depends:
        for p in src_addon_path:
            for d in os.listdir(p):
                if d in depends:
                    handle_addon(path_join(p, d), d)
    for path in src_addon_path:
        handle_auto_install(path)


def main(op, src_path):
    handle_own_path(op)
    handle_with_src(src_path)
    # print 'depends are:', depends
    print 'addons are:', sorted(handled_addons)
    # print 'copy_paths are:', copy_paths

    i = raw_input('Enter [Y/N] to copy: ')
    if i != 'Y':
        return 
    new_path = start_copy_to(op, src_path)
    print 'Copy Done!'
    i = raw_input('Enter [Y/N] to make new docker iamge: ')
    if i != 'Y':
        return
    make_docker_image(new_path)
    print 'Make Done!'


def make_new_dir():
    p = 'odoo_%s' % datetime.date.strftime(datetime.date.today(), '%Y-%m-%d')
    i = 1
    name = p
    while os.path.exists(name):
        name = p + '_' + str(i)
        i += 1
    return name


def make_docker_image(new_path):
    docker_path = '/home/todd/Documents/deploy/zj_dep_aliyun'
    src_path = path_join(docker_path, 'odoo_src')
    if os.path.exists(src_path):
        print 'removing old src'
        shutil.rmtree(src_path)
    shutil.copytree(new_path, src_path)
    print 'copy src code to %s from %s' % (src_path, new_path)
    os.chdir(docker_path)
    print 'change dir to docker image making path'
    subprocess.call(['git', 'init'])
    print 'git init done'
    subprocess.call(['git', 'add', '.'])
    print 'git add done'
    subprocess.call(['git', 'commit', '-m', 'Add new package %s' % new_path.rsplit('/')[-1]])
    print 'git commit done'
    subprocess.call(['docker', 'build', '-f', path_join(docker_path, 'Dockerfile'), '-t', 'odoo:%s' % new_path.rsplit('/')[-1], '.'])


def start_copy_to(op, src_path):
    new_dir = make_new_dir()
    print 'make new dir:', new_dir
    print 'start copy origin odoo with out addons.'
    def ignore(src, names):
        s = set([])
        for name in names:
            if name == 'addons' and not path_join(src, name).endswith('odoo/addons'):
                s.add(name)
            if name.startswith('.'):
                s.add(name)
            if name.endswith('po') and name != 'zh_CN.po':
                s.add(name)
        return s
    shutil.copytree(src_path, new_dir, ignore=ignore)
    print 'start copy self define addons...'
    shutil.copytree(op, path_join(new_dir, 'addons'))
    print 'start copy self depends origin addons...'
    for p in copy_paths:
        new_p = path_join(new_dir, 'addons', p.rsplit('/')[-1])
        if not os.path.exists(new_p):
            shutil.copytree(p, new_p, ignore=ignore)
    return new_dir


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print '\nUsage:\n\tpython make_odoo_minify.py <own-addon-path> <odoo-source-path>\n'
        sys.exit()
    own_path, src_path = sys.argv[1], sys.argv[2]
    main(own_path, src_path)
