from flask import Flask, Response, render_template, request
import json
from subprocess import Popen, PIPE
import os
from tempfile import mkdtemp
from werkzeug import secure_filename
import sys

app = Flask(__name__)
app.debug = True

# This is used to prevent the CMS from deleting itself
cms_name = "dockercms"

@app.route("/")
def index():
    return """
Available API endpoints:<br/>
<br/>
GET /containers                     List all containers<br/>
GET /containers?state=running      List running containers (only)<br/>
GET /containers/<id>                Inspect a specific container<br/>
GET /containers/<id>/logs           Dump specific container logs<br/>
GET /images                         List all images<br/>
<br/>
<br/>
POST /images                        Create a new image<br/>
POST /containers                    Create a new container<br/>
<br/>
PATCH /containers/<id>              Change a container's state<br/>
PATCH /images/<id>                  Change a specific image's attributes<br/>
<br/>
DELETE /containers/<id>             Delete a specific container<br/>
DELETE /containers                  Delete all containers (including running)<br/>
DELETE /images/<id>                 Delete a specific image<br/>
DELETE /images                      Delete all images<br/>

"""

@app.route('/containers', methods=['GET'])
def containers_index():
    """
    List all containers
 
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers | python -mjson.tool
    curl -s -X GET -H 'Accept: application/json' http://localhost:8080/containers?state=running | python -mjson.tool

    """
    if request.args.get('state') == 'running': 
        output = docker('ps')
        resp = json.dumps(docker_ps_to_array(output))
         
    else:
        output = docker('ps', '-a')
        resp = json.dumps(docker_ps_to_array(output))

    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['GET'])
def images_index():
    """
    List all images 
    """
    output = docker("images")
    
    resp = json.dumps(docker_images_to_array(output))
    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['GET'])
def containers_show(id):
    """
    Inspect specific container

    """
    output = docker("inspect", str(id))

    resp = output

    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>/logs', methods=['GET'])
def containers_log(id):
    """
    Dump specific container logs

    """
    output = docker("logs", str(id))
    resp = str(docker_logs_to_object(id, output))
    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['DELETE'])
def images_remove(id):
    """
    Delete a specific image
    """
    docker ('rmi', id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

@app.route('/containers/<id>', methods=['DELETE'])
def containers_remove(id):
    """
    Delete a specific container - must be already stopped/killed

    """
    docker("rm", id)
    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

@app.route('/containers', methods=['DELETE'])
def containers_remove_all():
    """
    Force remove all containers - dangrous!

    """
    containers_raw = docker('ps', '-a')
    containers_array = docker_ps_to_array(containers_raw)

    deleted_containers = []
    for container in containers_array:
        # Stops and deletes every container
        # Checks if each container has the same name as this container, to prevent it from deleting itself!
        if container["name"] != cms_name: 
            id = container["id"]
            docker("stop", id)
            docker("rm", id)
            deleted = {"id": id}
            deleted_containers.append(deleted)

    # Returns the ids of the deleted containers
    resp = json.dumps(deleted_containers)
    return Response(response=resp, mimetype="application/json")

@app.route('/images', methods=['DELETE'])
def images_remove_all():
    """
    Force remove all images - dangrous!

    """
    images_raw = docker("images")
    images_array = docker_images_to_array(images_raw)
    
    deleted_images = []
    for image in images_array:
        # Force deletes every image
        # Checks if each image belongs to this cms, to prevent it from deleting itself!
        if image["name"] != cms_name:
            id = image["id"]
            docker("rmi", str(id), "-f")
            deleted = {"id": id}
            deleted_images.append(deleted)
 
    # Returns the ids of the deleted images
    resp = json.dumps(deleted_images)
    return Response(response=resp, mimetype="application/json")


@app.route('/containers', methods=['POST'])
def containers_create():
    """
    Create container (from existing image using id or name)

    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "my-app"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e"}'
    curl -X POST -H 'Content-Type: application/json' http://localhost:8080/containers -d '{"image": "b14752a6590e","publish":"8081:22"}'

    """
    body = request.get_json(force=True)
    image = body['image']
    args = ('run', '-d')

    # Add the port if it is provided
    ports = body['publish']
    if ports != None:
        args = args + ('-p', ports)

    id = docker(*(args + (image,)))[0:12]
    return Response(response='{"id": "%s"}' % id, mimetype="application/json")


@app.route('/images', methods=['POST'])
def images_create():
    """
    Create image (from uploaded Dockerfile)

    curl -H 'Accept: application/json' -F file=@Dockerfile http://localhost:8080/images

    """
    dockerfile = request.files['file']
    dockerfile.save(secure_filename("Dockerfile"))

    # Check if a tag was supplied
    tag = request.args.get('tag')
    if tag == None:
        docker("build", ".")
    else:
        docker("build", "-t", str(tag), ".")

    # Get the id of the newly created image, and return it
    images = docker_images_to_array(docker("images"))
    new_image_id = {"id": images[0]["id"]}
    
    resp = json.dumps(new_image_id)
    return Response(response=resp, mimetype="application/json")


@app.route('/containers/<id>', methods=['PATCH'])
def containers_update(id):
    """
    Update container attributes (support: state=running|stopped)

    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "running"}'
    curl -X PATCH -H 'Content-Type: application/json' http://localhost:8080/containers/b6cd8ea512c8 -d '{"state": "stopped"}'

    """
    body = request.get_json(force=True)
    try:
        state = body['state']
        if state == 'running':
            docker('restart', id)
        elif state == "stopped":
            docker('stop', id)
    except:
        pass

    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")

@app.route('/images/<id>', methods=['PATCH'])
def images_update(id):
    """
    Update image attributes (support: name[:tag])  tag name should be lowercase only

    curl -s -X PATCH -H 'Content-Type: application/json' http://localhost:8080/images/7f2619ed1768 -d '{"tag": "test:1.0"}'

    """
    body = request.get_json(force=True)
    tag = body['tag']
    docker("tag", id, tag)

    resp = '{"id": "%s"}' % id
    return Response(response=resp, mimetype="application/json")


@app.route('/services', methods=['GET'])
def services_index():
    """
    List all services
    """
    output = docker("service", "ls")
    
    resp = json.dumps(docker_services_to_array(output))
    return Response(response=resp, mimetype="application/json")
    


@app.route('/nodes', methods=['GET'])
def nodes_index():
    """
    List all nodes in the swarm
    """
    output = docker("node", "ls")
    
    resp = json.dumps(docker_nodes_to_array(output))
    return Response(response=resp, mimetype="application/json")


def docker(*args):
    cmd = ['docker']
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout_decoded = stdout.decode("utf-8")
    stderr_decoded = stderr.decode("utf-8")
    if stderr_decoded.startswith('Error'):
        print('Error: {0} -> {1}'.format(' '.join(cmd), stderr_decoded))
    return stderr_decoded + stdout_decoded

# 
# Docker output parsing helpers
#

#
# Parses the output of a Docker PS command to a python List
# 
def docker_ps_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['image'] = c[1]
        each['name'] = c[-1]
        each['ports'] = c[-2]
        all.append(each)
    return all

#
# Parses the output of a Docker logs command to a python Dictionary
# (Key Value Pair object)
def docker_logs_to_object(id, output):
    logs = {}
    logs['id'] = id
    all = []
    for line in output.splitlines():
        all.append(line)
    logs['logs'] = all
    return logs

#
# Parses the output of a Docker image command to a python List
# 
def docker_images_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[2]
        each['tag'] = c[1]
        each['name'] = c[0]
        all.append(each)
    return all

#
# Parses the output of a Docker services command to a python List
# 
def docker_services_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        each = {}
        each['id'] = c[0]
        each['name'] = c[1]
        each['mode'] = c[2]
        each['replicas'] = c[3]
        each['image'] = c[4]
        each['ports'] = c[5]
        all.append(each)
    return all

#
# Parses the output of a Docker node command to a python List
# 
def docker_nodes_to_array(output):
    all = []
    for c in [line.split() for line in output.splitlines()[1:]]:
        print(len(c), file=sys.stderr)
        offset = 1 if len(c) == 6 else 0
        each = {}
        each['id'] = c[0]
        each['hostname'] = c[1 + offset]
        each['status'] = c[2 + offset]
        each['availability'] = c[3 + offset]
        each['leader'] = len(c) == 6
        all.append(each)
    return all

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
