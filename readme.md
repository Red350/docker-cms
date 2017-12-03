# Docker Container Management System
Padraig Redmond C15755659  
CMS running on: 35.189.226.205:80

This system allows controlling of docker containers and images through a RESTful API.  
  
Though the assignment only required the API to run as a script, I managed to get it running as a Docker container with the use of the `--mount` argument shown below.  
  
Because of this, it was neccessary to explicity avoid deleting the dockercms container and image when the force delete endpoints are called.

## Repo Link
https://github.com/Red350/docker-cms

## Video Link
https://youtu.be/wpR80bMJAJo

## Setup
Clone the repo to your home directory and cd into docker-cms directory.
##### Build Image
`docker build -t dockercms .`
##### Run Container
```
docker run -d -v ~/docker-cms/myapp:/myapp -p 80:8080 --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock --name dockercms dockercms
```
The `-v` argument allows changes to be made to the app.py script without having to rebuild the image.  
  
The `--mount` argument allows the container to run commands on the vm itself, rather than running commands internally.

## Endpoints
After following the steps in setup, the API can be connected to using the following endpoints.  
  
I've also provided example cURL commands for each endpoint.  
  
| Method | Endpoint                  | Description                 | Example cURL call                                                                                                         |
|--------|---------------------------|-----------------------------|---------------------------------------------------------------------------------------------------------------------------|
| GET    | /containers               | List all containers         | curl -s -H 'Accept: application/json' -X GET http://localhost:80/containers                                               |
| GET    | /containers?state=running | List running containers     | curl -s -H 'Accept: application/json' -X GET http://localhost:80/containers?state=running                                 |
| GET    | /containers/<id>          | Inspect container           | curl -s -H 'Accept: application/json' -X GET http://localhost:80/containers/<id>                                          |
| GET    | /containers/<id>/logs     | View logs for a container   | curl -s -H 'Accept: application/json' -X GET http://localhost:80/containers/<id>/logs                                     |
| GET    | /images                   | List all images             | curl -s -H 'Accept: application/json' -X GET http://localhost:80/images                                                   |
| GET    | /services                 | List all services           | curl -s -H 'Accept: application/json' -X GET http://localhost:80/services                                                 |
| GET    | /nodes                    | List all nodes in the swarm | curl -s -H 'Accept: application/json' -X GET http://localhost:80/nodes                                                    |
| POST   | /images                   | Create a new image          | curl -s -H 'Accept: application/json' -X POST -F file=@Dockerfile http://localhost:80/images                              |
| POST   | /containers               | Create a new container      | curl -s -H 'Accept: application/json' -X POST http://localhost:80/containers -d {"publish": "5001:5002", "image": "<id>"} |
| PATCH  | /containers/<id>          | Change a container's state  | curl -s -H 'Accept: application/json' -X PATCH http://localhost:80/containers/<id>  -d {"state": "stopped"}               |
| PATCH  | /images/<id>              | Change an image's tag       | curl -s -H 'Accept: application/json'-X PATCH http://localhost:80/images/<id>  -d {"tag": "newtag:1.0"}                   |
| DELETE | /containers/<id>          | Delete a container          | curl -s -H 'Accept: application/json' -X DELETE http://localhost:80/containers/<id>                                       |
| DELETE | /containers               | Force delete all containers | curl -s -H 'Accept: application/json' -X DELETE http://localhost:80/containers                                            |
| DELETE | /images/<id>              | Delete an image             | curl -s -H 'Accept: application/json' -X DELETE http://localhost:80/images/<id>                                           |
| DELETE | /images                   | Force delete all images     | curl -s -H 'Accept: application/json' -X DELETE http://localhost:80/images                                                |

## Running the Tests
Use the following format to run the tests:  
  
`python3 cmstests.py <url/ip> <port>`  
  
So to run the tests on the server while the CMS is on port 80:  
  
`python3 cmstests.py localhost 80`  
  
There will be a small delay while the server is building the image for the first test, but after that they should run quite quickly.

## Running Nginx as a Service
The following is a command to run Nginx as a service. 
  
`docker service create --detach=true --replicas 10 -p 80:80 --name nginx nginx`
