import subprocess
import dotenv
import os

dotenv.load_dotenv('.env')


def get_mesh_ip():
    cmd = f"kubectl get svc seldon-mesh -n {os.environ['SELDON_NAMESPACE']} -o jsonpath='{{.status.loadBalancer.ingress[0].ip}}'"
    return subprocess.check_output(cmd, shell=True).decode('utf-8')