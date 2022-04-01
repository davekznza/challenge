# Docker

## Overview

Run a simple NodeJS application and expose it on port 8080.

## Steps

Install npm and nodejs (I'm using Ubuntu):
```sh
$ sudo apt install npm nodejs

$ node -v
v10.19.0
```

Create image directory:
```sh
$ mkdir ~/cowsay
$ cd ~/cowsay
```

Download app src, extract and remove archive file:
```sh
$ wget https://<redacted>/dockerise_me.zip
$ unzip dockerise_me.zip
$ rm dockerise_me.zip
```

Create a `package.json` file to describe our app and dependencies:
```sh
$ cat << EOF > package.json
{
  "name": "cowsay",
  "version": "1.0.0",
  "description": "Cowsay Moooo...",
  "author": "dave <redacted>",
  "main": "main.js",
  "scripts": {
    "start": "node main.js"
  },
  "dependencies": {
  }
}
EOF
```

Create our `Dockerfile`:
```sh
$ cat << EOF > Dockerfile
# Using node:10, had issues with node:16
FROM node:10

# Set environment variable which our app references
ENV FOOBAR="Foo Bar"

# Create our apps workdir
WORKDIR /app

# Copy our package.json across, wildcard used to ensure package-lock.json is also included
COPY package*.json ./

# Install dependecies and update
RUN npm install
RUN npm update

# Bundle app source
COPY . .

# App binds to 8080/tcp we'll expose that
EXPOSE 8080

# Run our app
CMD [ "node", "main.js" ]
EOF
```

Build our image, tag it `cowsay:latest`:
```sh
$ docker build --no-cache=true --tag cowsay:latest .
```

Build output:
```sh
Sending build context to Docker daemon  4.608kB
Step 1/9 : FROM node:10
 ---> 28dca6642db8
Step 2/9 : ENV FOOBAR="Foo Bar"
 ---> Running in 710ee1964518
Removing intermediate container 710ee1964518
 ---> b327b4f30cf1
Step 3/9 : WORKDIR /app
 ---> Running in bef7cef915bc
Removing intermediate container bef7cef915bc
 ---> 35aaf200b965
Step 4/9 : COPY package*.json ./
 ---> f62972546c54
Step 5/9 : RUN npm install
 ---> Running in f2c586a3acc9
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN cowsay@1.0.0 No repository field.
npm WARN cowsay@1.0.0 No license field.

up to date in 0.55s
found 0 vulnerabilities

Removing intermediate container f2c586a3acc9
 ---> 1bf8257bb6d2
Step 6/9 : RUN npm update
 ---> Running in 9936f843878e
Removing intermediate container 9936f843878e
 ---> e0a5e8c953d3
Step 7/9 : COPY . .
 ---> 5d1733bfaade
Step 8/9 : EXPOSE 8080
 ---> Running in 75e7e58286c9
Removing intermediate container 75e7e58286c9
 ---> cdb0f9428b67
Step 9/9 : CMD [ "node", "main.js" ]
 ---> Running in 62d62f90a542
Removing intermediate container 62d62f90a542
 ---> b0ed7c563456
Successfully built b0ed7c563456
Successfully tagged cowsay:latest
```

Start our container detached (local port 8080 -> container port 8080):
```sh
$ docker run -d -p 8080:8080 --name cowsay cowsay:latest
9a916092efbbf85010557e41f216cf15ce04426a10293719e3b49ac220b87b5e
```

Check to see container is started and running:
```sh
$ docker ps -a
CONTAINER ID   IMAGE               COMMAND                  CREATED          STATUS                        PORTS                                       NAMES
9a916092efbb   cowsay:latest       "docker-entrypoint.s…"   4 seconds ago    Up 3 seconds                  0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   cowsay
```

Access app at http://localhost:8080 via browser or curl to verify it's running as expected:
```sh
$ curl -i localhost:8080

HTTP/1.1 200 OK
Content-Type: text/plain
Date: Thu, 31 Mar 2022 09:03:26 GMT
Connection: keep-alive
Transfer-Encoding: chunked

     ________________________________________
    < mooooooooooooooooooooooooooooooooooooo >
     ----------------------------------------
           \
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
```

Cleanup:
```sh
$ docker stop cowsay
$ docker rm cowsay
$ docker rmi cowsay
```