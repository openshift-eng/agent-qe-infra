FROM golang:alpine as build-env
LABEL maintainer="bmanzari@redhat.com"

ENV GO111MODULE=on
RUN apk --no-cache add git

COPY . /app
WORKDIR /app

RUN ls -lahR && go mod download && go build -o /vnc-recorder

FROM linuxserver/ffmpeg:version-5.1.2-cli
COPY --from=build-env /vnc-recorder /
ENTRYPOINT ["sh"]
