#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder of the
AirBnB Clone repo,using the function do_pack
"""


from fabric.operations import local
from datetime import datetime


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
