from os.path import expanduser

def executeDockerCommand(*args):
    return subprocess.check_output(["docker"] + list(args)).strip()

def docker_inspect(fmt, mcn):
    return executeDockerCommand("inspect", "-f", fmt, mcn)

def docker_port(machine):
    output = executeDockerCommand("port", machine, "22")
    tokens = output.split(':')
    return tokens[1]

def get_host_vars(m):
    home = expanduser("~")
    ip = [docker_inspect("{{.NetworkSettings.IPAddress}}", m)]
    ssh_vars = {
         "ansible_port": docker_port(m),
         "ansible_host": "localhost",
         "ansible_private_key_file": home+ "/.ssh/" + "id_rsa",
         "ansible_user": "root",
         "ansible_become_user": "root",
         "ansible_become_password": "root"
    }
    hostConnectionDetails = {"hosts": ip, "vars": ssh_vars}
    return hostConnectionDetails

class DockerInventory():
      def __init__(self):
          self.inventory = {} # Ansible Inventory

          machines = executeDockerCommand("ps", "-q").splitlines()
          json_data = {m: get_host_vars(m) for m in machines}

          print json.dumps(json_data)

DockerInventory()
