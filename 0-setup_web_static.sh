#!/usr/bin/env bash
#script that sets up your web servers for the deployment of web_static
apt-get -y update
apt-get install -y nginx
/etc/init.d/nginx start

# create the following direcories and files
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

echo "Hello configuration successful" > /data/web_static/releases/test/index.html

# Check if /data/web_static/current exists and remove it
if [ -d "/data/web_static/current" ]
then
	sudo rm -rf /data/web_static/current
fi

# create a symbolic link 
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data to ubuntu user and group

chown ubuntu:ubuntu -R /data

#Update the Nginx configuration to serve the content

file=/etc/nginx/sites-available/default
rm $file
echo -e "server {
    listen 80 default_server;
    root /usr/share/nginx/html;
    index index.html index.htm;
    add_header X-Served-By $HOSTNAME;
    location /redirect_me {
        return 301 https://www.youtube.com;
    }
    location /hbnb_static {
        alias /data/web_static/current;
    }
}" > $file

# Test Nginx configuration and reload Nginx to apply changes
nginx -t
service nginx reload

#restart Nginx after updating the configuration:
service nginx restart
