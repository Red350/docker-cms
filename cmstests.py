import unittest
import json
from subprocess import Popen, PIPE

ip = "localhost"
debug = True

class CmsTests(unittest.TestCase):

    test_command = "nope"
    test_output = ""

    def test_curl(self):
        args = ("-s", "-X", "GET", "-H", "'Accept: application/json'", "http://localhost:80/containers")
        self.__save_test_command(args)

        output = json.loads(curl(*args))
        self.__save_test_output(output)

        self.assertEqual(1,1)

    def tearDown(self):
        if debug:
            print("Command:")
            print(self.test_command)
            print("Response:")
            print(self.test_output)
            input("Press enter to continue")

    def __save_test_command(self, args):
        self.test_command = "curl" + " ".join(args)

    def __save_test_output(self, output):
        self.test_output = json.dumps(output, indent=4, sort_keys=True)

def print_test_header(header):
    num_symbols = len(header) + 4
    print("#" * num_symbols)
    print("# " + header + " #")
    print("#" * num_symbols)

def print_command(args):
    print("curl" + " ".join(args))

def print_output(output):
    print(json.dumps(json.loads(output), indent=4, sort_keys=True))

def wait():
    input("Press enter to continue")

def curl(*args):
    cmd = ['curl']
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
    print("Listing containers...")
    args = ("-s", "-X", "GET", "-H", "'Accept: application/json'", "http://{}:80/containers".format(ip))
    print_output(curl(*args))

def list_images():
    print("Listing images...")
    args = ("-s", "-X", "GET", "-H", "'Accept: application/json'", "http://{}:80/images".format(ip))
    print_output(curl(*args))

# Image tests

# Test 1: Add an image
def test_add_image():
    list_containers()
    list_images()

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