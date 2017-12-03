# Docker Container Management System
Name: Padraig Redmond
Student number: C15755659

This system allows controlling of docker container and images through a RESTful API.

## Setup
Clone repo to home directory and cd into docker-cms directory.
##### Build Image
`docker build -t dockercms  .`
##### Run Container
```
docker run -d -v ~/dockercms/myapp:/myapp -p 80:8080 --mount type=bind,source=/var/run/docker.sock,destination=/var/run/docker.sock --name dockercms dockercms
```
The `-v` argument allows changes to be made to the app.py script without having to rebuild the image.
The `--mount` argument allows the container to run commands on the vm itself, rather than running commands internally.

## Endpoints
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



## Running Nginx as a Service
docker service create --detach=true --replicas 10 -p 80:80 --name web nginx