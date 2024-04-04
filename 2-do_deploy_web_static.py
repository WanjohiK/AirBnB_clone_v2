#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers
"""
from fabric.operations import local, run, put
from datetime import datetime
from fabric.api import env
import os
import re


env.hosts = ['100.25.104.17', '35.174.205.159']
env.user = "ubuntu"


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
    try:
        try:
            if os.path.exists(archive_path):
                arc_tgz = archive_path.split("/")
                arg_save = arc_tgz[1]
                arc_tgz = arc_tgz[1].split('.')
                arc_tgz = arc_tgz[0]

                """Upload archive to the server"""
                put(archive_path, '/tmp')

                """Save folder paths in variables"""
                uncomp_fold = '/data/web_static/releases/{}'.format(arc_tgz)
                tmp_location = '/tmp/{}'.format(arg_save)

                """Run remote commands on the server"""
                run('mkdir -p {}'.format(uncomp_fold))
                run('tar -xvzf {} -C {}'.format(tmp_location, uncomp_fold))
                run('rm {}'.format(tmp_location))
                run('mv {}/web_static/* {}'.format(uncomp_fold, uncomp_fold))
                run('rm -rf {}/web_static'.format(uncomp_fold))
                run('rm -rf /data/web_static/current')
                run('ln -sf {} /data/web_static/current'.format(uncomp_fold))
                run('sudo service nginx restart')
                return True
            else:
                print('File does not exist')
                return False
        except Exception as err:
            print(err)
            return False
    except Exception:
        print('Error')
        return False
