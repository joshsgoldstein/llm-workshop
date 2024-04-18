from utils import get_mesh_ip
import requests


SD_IP = "https://34.23.166.69"  # use this SEP
# SELDON_MESH_GATEWAY = "http://35.196.70.25"
SELDON_MESH_GATEWAY = "http://34.73.221.94"
KIND_CLUSTER = "http://localhost:8080"

PIPELINE_NAME = "laszlo-rag-seldon-core-v2"
NAMESPACE = "seldon-mesh"


endpoint = f"{SELDON_MESH_GATEWAY}/v2/models/laszlo-rag-seldon-core-v2/infer"


request = {
    "inputs": [
        {
            "name": "role",
            "shape": [1, 1],
            "datatype": "BYTES",
            "data": ["user"],
            "parameters": {"content_type": "str"},
        },
        {
            "name": "content",
            "shape": [1, 1],
            "datatype": "BYTES",
            "data": ["tell me about seldon core"],
            "parameters": {"content_type": "str"},
        },
        {
            "name": "memory_id",
            "shape": [1, 1],
            "datatype": "BYTES",
            "data": ["b2"],
            "parameters": {"content_type": "str"},
        },
    ]
}
headers = {
    "Seldon-Model": f"{PIPELINE_NAME}.pipeline",
    "Host": f"{NAMESPACE}.inference.seldon",
    "Content-Type": "application/json",
}
print(headers)
r = requests.post(endpoint, json=request, headers=headers, verify=False)
print(r)
print(r.json()["outputs"])
