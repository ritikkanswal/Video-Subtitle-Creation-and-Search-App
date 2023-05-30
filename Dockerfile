FROM python:latest
ARG SSH_PRIVATE_KEY
RUN apt-get update
RUN apt-get install -y libavcodec58         
RUN apt-get install -y libavformat58
RUN apt-get install -y libc6
RUN apt-get install -y libfreetype6
RUN apt-get install -y libavutil56
RUN apt-get install -y liblept5
RUN apt-get install -y libpng16-16
RUN apt-get install -y libswscale5
RUN apt-get install -y libtesseract4
RUN apt-get install -y libutf8proc2
RUN apt-get install -y zlib1g
RUN apt install ffmpeg -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get install ./ccextractor_0.88+ds1-1_amd64.deb
RUN export DJANGO_SETTINGS_MODULE=SubtitleTimeTracker.settings



