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
cms_name = "dockercms"

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
    args = (get_request, base_url + "/containers?state=running")
    print_command(args)
    print("Listing running images...")
    return process_command(args)

def list_images():
    args = (get_request, base_url + "/images")
    print_command(args)
    print("Listing images...")
    return process_command(args)

def create_image(filepath):
    args = (post_request, "-F", "file=@{}".format(filepath), base_url + "/images")
    print_command(args)
    print("Creating image for {}...".format(filepath))
    return process_command(args)

def tag_image(id, tag):
    body = json.dumps({"tag": tag})
    args = (patch_request, base_url + "/images/{}".format(id), "-d", body)
    print_command(args)
    print("Updating tag for id: {} to {}...".format(id, tag))
    return process_command(args)

def create_container(id, ports):
    body = json.dumps({"image": str(id), "publish": str(ports)})
    args = (post_request, base_url + "/containers", "-d", body)
    print_command(args)
    print("Creating container for image: {}".format(id))
    return process_command(args)

def set_container_state(id, state):
    body = json.dumps({"state": state})
    args = (patch_request, base_url + "/containers/{}".format(id), "-d", body)
    print_command(args)
    print("Setting container {} to {}".format(id, state))
    return process_command(args)


# Image tests

# Test 1: Create an image
def test_create_image():
    print_test_header("Test 1: Create an image")
    new_image = create_image("dockerfiles/sshd.Dockerfile")
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

# Test 4: Create a container
def test_create_container(id):
    print_test_header("Test 4: Create a container")
    new_container = create_container(id, "5001:5002")
    return new_container["id"]

# Test 5: Inspect specific container
def test_inspect_container(id):
    print_test_header("Test 5: Inspect container")
    args = (get_request, base_url + "/containers/{}".format(id))
    print_command(args)
    print("Inspecting container {}...".format(id))
    process_command(args)

# Test 6: View logs for specific container
def test_view_logs(id):
    print_test_header("Test 6: View logs for container")
    args = (get_request, base_url + "/containers/{}/logs".format(id))
    print_command(args)
    print("Viewing logs for {}...".format(id))
    process_command(args)

# Test 7: List all containers
def test_list_containers():
    print_test_header("Test 7: List all containers")
    list_containers()

# Test 8: Stop container
def test_stop_container(id):
    print_test_header("Test 8: Stop a container")
    set_container_state(id, "stopped")
    

# Test 9: List all running containers
def test_list_running_containers():
    print_test_header("Test 9: List running containers")
    list_running_containers()

# Test 10: Restart container
def test_restart_container(id):
    print_test_header("Test 10: Restart a container")
    set_container_state(id, "running")
    list_running_containers()


# Deletion tests

# Test 11: Delete a container
def test_delete_container(id):
    print_test_header("Test 11: Delete a container")
    set_container_state(id, "stopped")
    args = (delete_request, base_url + "/containers/{}".format(id))
    print_command(args)
    print("Deleting container {}...".format(id))
    process_command(args)
    list_containers()

# Test 12: Force delete all containers
def test_delete_all_containers():
    print_test_header("Test 12: Delete all containers")
    args = (delete_request, base_url + "/containers")
    print_command(args)
    print("Deleting all containers...")
    process_command(args)
    list_containers()

# Test 13: Delete an image
def test_delete_image(id):
    print_test_header("Test 13: Delete an image")
    args = (delete_request, base_url + "/images/{}".format(id))
    print_command(args)
    print("Deleting image {}...".format(id))
    process_command(args)
    list_images()

# Test 14: Force delete all images
def test_delete_all_images():
    print_test_header("Test 14: Delete all images")
    args = (delete_request, base_url + "/images")
    print_command(args)
    print("Deleting all images...")
    process_command(args)
    list_images()


# Docker swarm tests

# Test 15: List all services
def test_list_services():
    print_test_header("Test 15: List all services")
    args = (get_request, base_url + "/services")
    print_command(args)
    print("Listing all services...")
    process_command(args)

# Test 16: List all nodes in the swarm
def test_list_nodes():
    print_test_header("Test 16: List all nodes")
    args = (get_request, base_url + "/nodes")
    print_command(args)
    print("Listing all nodes...")
    process_command(args)

def wait():
    pass
    #input("Press enter to continue")

# Call all the tests
image_id = test_create_image()
wait()
test_update_image(image_id)
wait()
test_list_images()
wait()

container_id = test_create_container(image_tag)
wait()
test_inspect_container(container_id)
wait()
test_view_logs(cms_name)
wait()
test_list_containers()
wait()
test_stop_container(container_id)
wait()
test_list_running_containers()
wait()
test_restart_container(container_id)
wait()

test_delete_container(container_id)
wait()
test_delete_all_containers()
wait()
test_delete_image(image_tag)
wait()
test_delete_all_images()
wait()

test_list_services()
wait()
test_list_nodes()
wait()
