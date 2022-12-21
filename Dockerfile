FROM debian:stretch as build

RUN apt update -y && apt install -y \
	pkg-config libglib2.0-dev libxml2-dev libcurl3-dev libtagc0-dev wget libid3-3.8.3-dev build-essential

WORKDIR /build
RUN wget http://savannah.nongnu.org/download/castget/castget-2.0.1.tar.bz2 && tar -xf castget-*
RUN cd castget-* && ./configure && make && mv src/castget /build/

FROM debian:stretch

RUN apt update -y && apt install -y \
	libglib2.0 libxml2 libcurl3 libtagc0 libid3-3.8.3v5 ffmpeg python3

COPY --from=build /build/castget /usr/bin/

RUN useradd --create-home castget
USER castget

WORKDIR /home/castget/
COPY docker-entrypoint.sh /home/castget/docker-entrypoint.sh
COPY transcode.py /home/castget/transcode.py

ENTRYPOINT ["/home/castget/docker-entrypoint.sh"]
