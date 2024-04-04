from fabric.api import local
from datetime import datetime

def do_pack():
    local("mkdir -p versions")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_name = "web_static_{}.tgz".format(timestamp)
    archive_path = "versions/{}".format(archive_name)
    result = local("tar -cvzf {} web_static".format(archive_path))
    if result.failed:
        return None
    else:
        return archive_path
