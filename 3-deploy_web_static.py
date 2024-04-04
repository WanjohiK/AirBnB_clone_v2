#!/usr/bin/python3
"""
creates and distributes an archive to your web servers,
using the function deploy
"""
from fabric.operations import local, run, put
from datetime import datetime
from fabric.api import *
import os
import re


env.hosts = ['100.25.104.17', '35.174.205.159']
env.user = "ubuntu"


@runs_once
def do_pack():
    """
    generates a .tgz archive from the contents of the web_static
    """

    try:
        local("mkdir -p versions")
        time = datetime.now()
        dateformat = '%Y%m%d%H%M%S'
        date = time.strftime(dateformat)

        file_path = "versions/web_static__{}.tgz".format(date)
        local("tar -czvf {} web_static".format(file_path))
        return file_path

    except Exception:
        return None


def do_deploy(archive_path):
    """ deploys web_static.tgz to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    result = put(archive_path, "/tmp")
    if result.failed:
        return False

    rex = r'^versions/(\S+).tgz'
    match = re.search(rex, archive_path)
    filename = match.group(1)
    result = put(archive_path, "/tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run("mkdir -p /data/web_static/releases/{}/".format(filename))
    if result.failed:
        return False
    result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
                 .format(filename, filename))
    if result.failed:
        return False
    result = run("rm /tmp/{}.tgz".format(filename))
    if result.failed:
        return False
    result = run("mv /data/web_static/releases/{}"
                 "/web_static/* /data/web_static/releases/{}/"
                 .format(filename, filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/releases/{}/web_static"
                 .format(filename))
    if result.failed:
        return False
    result = run("rm -rf /data/web_static/current")
    if result.failed:
        return False
    result = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
                 .format(filename))
    if result.failed:
        return False

    print('New version deployed!')

    return True


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    tar = do_pack()
    if tar is None:
        return False
    return do_deploy(tar)
