# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 Joshua Watt <JPEWhacker@gmail.com>
#
# Dockerfile to build a bitbake hash equivalence server container
#
# From the root of the bitbake repository, run:
#
#   docker build -f contrib/hashserv/Dockerfile .
#

FROM alpine:3.18.4

RUN apk add --no-cache \
    python3 \
    py3-virtualenv \
    py3-pip

# Setup virtual environment
RUN mkdir /opt/hashserver
WORKDIR /opt/hashserver

ENV VIRTUAL_ENV=/opt/hashserver/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -U pip

COPY contrib/hashserv/requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

COPY bin/bitbake-hashserv ./bin/
COPY lib/hashserv ./lib/hashserv/
COPY lib/bb ./lib/bb/
COPY lib/codegen.py ./lib/
COPY lib/ply ./lib/ply/
COPY lib/bs4 ./lib/bs4/

ENTRYPOINT ["./bin/bitbake-hashserv"]
