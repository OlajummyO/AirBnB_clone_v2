#!/bin/bash

if ! command -v nginx &>/dev/null; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/{releases/test,shared}

sudo bash -c 'echo "<html><head></head><body>Test HTML file</body></html>" > /data/web_static/releases/test/index.html'

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_content="
server {
    listen 80;
    server_name _;

    location /hbnb_static {
        alias /data/web_static/current/;
    }
}
"

sudo bash -c "echo \"$config_content\" > /etc/nginx/sites-available/default"

# Restart Nginx
sudo service nginx restart

exit 0
