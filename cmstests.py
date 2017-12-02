import json
from subprocess import Popen, PIPE

base_url = "http://localhost:80"
get_request = "-X GET"
post_request = "-X POST"
patch_request = "-X PATCH"
delete_request = "-X DELETE"
accept_json = "-H 'Accept: application/json'"
base_curl_command = ['curl', '-s', accept_json]

image_tag = "sshd"

def print_test_header(header):
    num_symbols = len(header) + 4
    print("\n" +"#" * num_symbols)
    print("# " + header + " #")
    print("#" * num_symbols + "\n")

def print_command(args):
    print("Executing command...")
    print(" ".join(base_curl_command) + " ".join(args))

def print_output(output):
    print(json.dumps(output, indent=4, sort_keys=True))

# Makes a curl request with the supplied args
def curl(*args):
    cmd = base_curl_command[:]
    for sub in args:
        cmd.append(sub)
    print(cmd)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout_decoded = stdout.decode("utf-8")
    stderr_decoded = stderr.decode("utf-8")
    if stderr_decoded.startswith('Error'):
        print('Error: {0} -> {1}'.format(' '.join(cmd), stderr_decoded))
    return stderr_decoded + stdout_decoded

# Prints the output of a curl request as json, and returns that json
def process_command(args):
    output = json.loads(curl(*args))
    print_output(output)
    return output

def list_containers():
    args = (get_request, base_url + "/containers")
    print_command(args)
    print("Listing containers...")
    return process_command(args)

def list_running_containers():
    args = (get_request, base_url + "/containers?=running")
    print_command(args)
    print("Listing running images...")
    return process_command(args)

def list_images():
    args = (get_request, base_url + "/images")
    print_command(args)
    print("Listing images...")
    return process_command(args)

def add_image(filepath):
    args = (post_request, "-F", "file=@{}".format(filepath), base_url + "/images")
    print_command(args)
    print("Creating image for {}...".format(filepath))
    return process_command(args)

def tag_image(id, tag):
    tag_json = json.dumps({"tag": tag})
    args = (patch_request, base_url + "/images/{}".format(id), "-d", tag_json)
    print_command(args)
    print("Updating tag for id: {} to {}...".format(id, tag))
    return process_command(args)


# Image tests

# Test 1: Create an image
def test_add_image():
    print_test_header("Test 1: Create an image")
    new_image = add_image("dockerfiles/sshd.Dockerfile")
    return new_image["id"]

# Test 2: Update image tag
def test_update_image(image_id):
    print_test_header("Test 2: Update image tag")
    tag_image(image_id, image_tag)

# Test 3: List all images
def test_list_images():
    print_test_header("Test 3: List all images")
    list_images()

# Container tests

# Test 6: Create a container

# Test 7: Inspect specific container

# Test 8: View logs for specific container

# Test 9: List all containers

# Test 10: Stop container

# Test 11: List all running containers

# Test 12: Restart container




# Deletion tests

# Test 13: Delete a container

# Test 14: Force delete all containers

# Test 4: Delete an image

# Test 5: Force delete all images


# Docker swarm tests

# Test 15: List all services

# Test 16: List all nodes in the swarm

# Call all the tests
#test_add_image()
#test_list_images()
#test_update_image()

#list_containers()
#list_images()
