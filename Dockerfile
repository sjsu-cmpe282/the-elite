FROM golang:1.12-alpine

RUN apk add --no-cache git

ADD . /app/hello-world

WORKDIR /app/hello-world

RUN go build -o ./bin/hello-world .

CMD ["./bin/hello-world"]
