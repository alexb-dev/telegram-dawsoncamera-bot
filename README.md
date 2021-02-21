# <p align="center">camerabot - a Telegram Bot to send pics from camera

![unit_tests](https://github.com/alexb-dev/telegram-dawsoncamera-bot/workflows/unit_tests/badge.svg)

Telegram bot to send new pictures from cameras (assuming camera saves them at the local folder).

Support multiple folders with images.
Note, the bot is not working with camera directly, it only cheks for images in specific folders.
(For example for Hikvision cameras save motion detected images over FTP)

It also draws a box around the region where the motion has occured.
(By comparing first and last files in series)

direct run:  

````python3 bot.py````

running via docker: 

```./docker_build```

```./docker_run```


API token needs to be set accordingly 

```export TELEGRAM_CAMERA_BOT_TOKEN=""``` 

or in docker environment variables  

```ENV TELEGRAM_CAMERA_BOT_TOKEN=""```
AVB
