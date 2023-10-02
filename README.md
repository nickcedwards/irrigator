# irrigator
Python application for controlling and monitoring my irrigation system

## Web-app
Refer to this helpful how-to for instructions: https://medium.com/geekculture/deploying-flask-application-on-vps-linux-server-using-nginx-a1c4f8ff0010

`webapp.py` contains a basic [flask](https://flask.palletsprojects.com/en/3.0.x/) webapp which is served using [gunicorn](https://gunicorn.org/) and (nginx)[https://www.nginx.com/]. Gunicorn provides the WSGI interface to the Flask app, and this is reverse-proxied via nginx.

### Install dependencies
   sudo apt install nginx

## Set the gunicorn service up
Copy `example_conf\gunicorn-service` to `/etc/systemd/system/irrigatorapp.service`, then run
   pip install flask gunicorn
   sudo servicectl start irrigatorapp

## Set nginx up
   sudo apt install nginx
   sudo ln -s /etc/nginx/sites-available/irrigatorapp /etc/nginx/sites-enabled
   systemctl daemon-reload
   sudo servicectl restart nginx

