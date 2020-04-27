FROM python:3
RUN mkdir -p /share/Public/cam_motion/Entrance
RUN mkdir -p /share/Public/cam_motion/enrty2
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

#COPY . .

CMD [ "python", "./bot.py" ]
#CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
