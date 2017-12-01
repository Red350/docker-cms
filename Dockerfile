############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################
# Set the base image to Ubuntu
FROM ubuntu:latest
MAINTAINER Padraig Redmond
Label org.label-schema.group="monitoring"
# Update the sources list
RUN apt-get update
# Install Python and Basic Python Tools
RUN apt-get install -y python3 python3-pip
#copy app.py into /app folder 
ADD /myapp /myapp
# Upgrade  PIP
RUN pip3 install --upgrade pip
# Get pip to download and install requirements:
RUN pip3 install -r /myapp/requirements.txt

# Install curl and docker
RUN apt-get install -y curl
RUN curl -fsSL get.docker.com|sh

# Expose ports
EXPOSE 8080
# Set the default directory where CMD will execute
WORKDIR /myapp
# Set the default command to execute
# when creating a new container
# i.e. using Flask to serve the application
CMD python3 app.py
