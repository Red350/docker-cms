import json
from subprocess import Popen, PIPE

base_url = "http://localhost:80"
get_request= "-X GET"
accept_json = "-H 'Accept: application/json'"
base_curl_command = ['curl', '-s', accept_json]

def print_test_header(header):
    num_symbols = len(header) + 4
    print("#" * num_symbols)
    print("# " + header + " #")
    print("#" * num_symbols)

def print_command(args):
    print("Executing command...")
    print("curl -s" + " ".join(args))

def print_output(output):
    print(json.dumps(json.loads(output), indent=4, sort_keys=True))

def curl(*args):
    cmd = base_curl_command
    for sub in args:
        cmd.append(sub)
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    stdout_decoded = stdout.decode("utf-8")
    stderr_decoded = stderr.decode("utf-8")
    if stderr_decoded.startswith('Error'):
        print('Error: {0} -> {1}'.format(' '.join(cmd), stderr_decoded))
    return stderr_decoded + stdout_decoded

def list_containers():
    args = (get_request, base_url + "/containers")
    print_command(args)
    print("Listing containers...")
    print_output(curl(*args))

def list_running_containers():
    args = (get_request, base_url + "/containers?=running")
    print_command(args)
    print("Listing running images...")
    print_output(curl(*args))

def list_images():
    args = ("-s", "-X", "GET", "-H", "'Accept: application/json'", "http://{}:80/images".format(ip))
    print_command(args)
    print("Listing images...")
    print_output(curl(*args))


# Image tests

# Test 1: Add an image
def test_add_image():
    list_containers()
#list_images()

# Test 2: List all images

# Test 3: Update image tag

# Test 4: Delete an image

# Test 5: Force delete all images


# Container tests

# Test 6: Create a container

# Test 7: Inspect specific container

# Test 8: View logs for specific container

# Test 9: List all containers

# Test 10: Stop container

# Test 11: List all running containers

# Test 12: Restart container

# Test 13: Delete a container

# Test 14: Delete all containers


# Swarm tests

# Test 15: List all services

# Test 16: List all nodes in the swarm

test_add_image()
