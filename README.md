# Instances Blog

a very simple blog based on flask. Goal is to serve the page within the first TCP roundtrip (around 14kB).

- using absolutely minimal css framework
- using system fonts stack
- reduce http requests where ever possible

## Features

### pages

The Blog will render all Markdown files in the pages subfolder.

### projects

todo

### dashboards

todo

## Installation

*on Debian(based) Server, using nginx and Gunicorn*

![Architecture](https://miro.medium.com/max/1400/1*zGC7qRcsw4G9I9u9KjMqaQ.png)


### Step 1: OS Dependencies
- python3
- python3-pip
- python3-venv
- python3-dev
- nginx

`sudo apt-get install python3-pip python3-dev nginx`

### Step 2: clone project

Website is served from here:

`cd /var/www/`

Clone the repository:

`sudo git clone https://github.com/alexladda/instance-blog`

Change owner

`sudo chown -R $USER:$USER instance-blog`

### Step 3: virtual environment

Create and activate virtual environment

`python3 -m venv env`
`source env/bin/activate`

Install instance-blog dependencies:

`python -m pip install -r requirements.txt`

this will be installed:
click==7.1.2
Flask==1.1.2
Flask-Markdown==0.3
gunicorn==20.1.0
itsdangerous==1.1.0
Jinja2==2.11.3
Markdown==3.3.4
MarkupSafe==1.1.1
Werkzeug==1.0.1

### Step 4: systemd

Deploy to systemd:

doublecheck the paths and settings:

`vim app.service`

symlink said file from systemd folder:

`sudo ln -s app.service /etc/systemd/system/ ./app.service`

`sudo systemctl start app`

`sudo systemctl enable app`

(the file `app.sock` is created)

### Step 5: configure nginx

`vim /etc/nginx/sites-available/instance-<n>.net`

    server {

           server_name instance-1.net;

           root /var/www/instance-blog;
           index index.html;

           location / {
                    try_files $uri $uri/ =404;
                    include proxy_params;
                    proxy_pass http://unix:/var/www/instance-blog/app.sock;
           }
    }

`ln -s /etc/nginx/sites-available/instance-1.net /etc/nginx/sites-enabled/instance-1.net`

test configuration:

`sudo nginx -t`

start / restart configuration:

`sudo systemctl restart nginx`
