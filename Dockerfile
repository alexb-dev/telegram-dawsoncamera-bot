FROM python:3
ENV TELEGRAM_CAMERA_BOT_TOKEN="1186794145:AAHl7gK5fXGBa0LZqMBvZqs5yfsg0xjoYgg"
RUN mkdir -p /share/Public/cam_motion/Entrance
RUN mkdir -p /share/Public/cam_motion/enrty2
WORKDIR /usr/src/app

COPY . /usr/src/app
#COPY requirements.txt ./
RUN ls -la ./*
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

CMD [ "python", "./camerabot/bot.py" ]
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
