FROM alpine as base

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    git \
    && apk del .build-deps