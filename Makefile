build:
    docker build -t myimage .

run:
    docker run -d --name mycontainer -p 80:80 myimage
