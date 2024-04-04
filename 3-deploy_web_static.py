#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
"""

from fabric.api import *
from datetime import datetime
import os.path

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path_to_ssh_key>'

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "web_static_{}.tgz".format(timestamp)
        archive_path = "versions/{}".format(archive_name)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except:
        return None

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename without extension>
        filename = os.path.basename(archive_path)
        filename_no_ext = os.path.splitext(filename)[0]
        run('mkdir -p /data/web_static/releases/{}/'.format(filename_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(filename, filename_no_ext))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -f /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        # linked to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(filename_no_ext))

        return True
    except:
        return False

def deploy():
    """
    Creates and distributes an archive to your web servers.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

