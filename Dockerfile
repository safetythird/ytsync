FROM debian:jessie

RUN apt-get update; apt-get install -y python-pip;
RUN pip install ipython youtube-dl

RUN mkdir -p /yt/.ytsync
WORKDIR /yt

CMD /bin/bash
