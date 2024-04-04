#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py)
"""

from fabric.api import *
from datetime import datetime
import os.path

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<username>'
env.key_filename = '<path_to_ssh_key>'

def do_clean(number=0):
    """
    Deletes out-of-date archives.
    """
    number = int(number)
    if number < 1:
        number = 1

    try:
        # Delete unnecessary archives in the versions folder
        with lcd("versions"):
            local("ls -t | tail -n +{} | xargs -d '\n' rm -rf".format(number))

        # Delete unnecessary archives in the /data/web_static/releases folder
        run("ls -t /data/web_static/releases | tail -n +{} | xargs -d '\n' rm -rf".format(number))

        return True
    except:
        return False
