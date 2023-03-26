<p align="center">
  <a href="https://amalgjose.files.wordpress.com/2021/02/fast_api_ppt.png"><img src="https://amalgjose.files.wordpress.com/2021/02/fast_api_ppt.png" height="200"></a>
</p>

<p align="center">
    <em>Messenger & Viber Chatbot Using Python for Nepal Banks Open Source Project 
        (Personal Project with no affiliation or copyright)</em>
</p>

---

**Source Code**:

https://github.com/Poojan670/messenger-viber-chatbot-python.git

---

Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.

FastAPI is a Web framework for developing RESTful APIs in Python. FastAPI is based on Pydantic and type hints to validate, serialize, and deserialize data and automatically auto-generate OpenAPI documents.

A Facebook chatbot is an automated software application that interacts with users via Facebook Messenger based on pre-programmed answers and keywords. Once installed, these chatbots are your 24/7 frontline agents.

A Viber chatbot gives you the option of messaging many subscribers simultaneously. Define a target audience within your subscriber base and message them. Send birthday greetings, offer seasonal coupons, and more.

<p align="center">
  <a href="https://website-assets-fw.freshworks.com/attachments/ck340ov180hsy65g0yxb6gbhb-1-chatbots-for-marketing-smm.one-half.png"><img src="https://website-assets-fw.freshworks.com/attachments/ck340ov180hsy65g0yxb6gbhb-1-chatbots-for-marketing-smm.one-half.png" alt="Chatbots" height="200"></a>
</p>

## Project Description

_Messsenger & Viber Chatbot Using Python & FastAPI_

_Postgres is used as the main database for this application (Optional)_


## Requirements

Python 3.8 +

PostgreSQL 

Fastapi 0.8 +


## Helpful References and Docs

_Official Facebook & Viber docs_

## Pre-requirements

_You will need to setup your facebook developer account at https://developers.facebook.com/_

_You will also need to setup your chatbot for pages for both fb & viber_

_you will need official https(ssl) legit site to work it in either testing or production_

__(You can use ngrok for custom routing of your local server on a https:// server for testing purposes)_

**_Application Setup_**

_setup .env in the main root directory_

```console
FB_PAGE_TOKEN=
CALLBACK_VERIFY_TOKEN=
MESSENGER_BOT_NAME=
SERVER_HOST=
SERVER_PORT=
POSTGRES_SERVER=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
PRIMARY_RECEIVER_ID=
SECONDARY_RECEIVER_ID=
SECOND_APP_TOKEN=
WEBHOOK_SERVER_URL=
VIBER_BOT_NAME=
VIBER_AUTH_TOKEN=
```

**Create database in postgres**
open psql terminal

```console
$ create database *your database*
```

_or create a database manually using PgAdmin4(comes along with postgres installation)_

Setup a virtual environment
```console
$ python -m venv env
$ pip install -r requirements.txt
```

_start FastAPI server_

```console
$ py main.py

# Using uvicorn
$ uvicorn main:app --reload
```

And Bingo, you're good to go.

Navigate to http://localhost:<your:port>/docs to access the server docs

# Using Local Server with Ngrok Tunneling

```console
if your running on 8000 port

Using choco or any other package manager

$ choco install ngrok

# Sign up and get your auth token for ngrok

$ ngrok config add-authtoken TOKEN

Start ngrok by running the following command.
$ ngrok http 8000

```
& Bingo you're good to go, facebook/viber should now accept your new tunneled remote https link 

# Setup Chatbot on Production Using Gunicorn

** Ubuntu Setup

Start by creating and opening a systemd socket file for Gunicorn with sudo privileges:

```console
Setup a gunicorn socket if you havent

$ sudo nano /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

Setup a chatbot gunicorn service file
```console
$ sudo nano /etc/systemd/system/chatbot.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/root/myprojectdir
ExecStart=/home/root/messenger-chat/env/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          messenger-chat.main:app

[Install]
WantedBy=multi-user.target

activate the service :

sudo systemctl enable chatbot.service
sudo systemctl start chatbot.service
```

Use nginx as reverse proxy

```console
server{
       listen 80;
       ssl /var/your ssl
       server_name your.server.com; 
       location / {
           include proxy_params;
           proxy_pass http://unix:/run/gunicorn.sock;
       }
}
```

# Setup Application with Docker

Using Makefile

```console
$ make build
$ make run
```

Using docker compose 

```console
$ docker compose up
```

