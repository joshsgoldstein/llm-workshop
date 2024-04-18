from utils import get_mesh_ip
import requests


SD_IP = "https://34.23.166.69" # use this SEP
SELDON_MESH_GATEWAY = "http://35.196.70.25"
KIND_CLUSTER = "http://localhost:8080"

PIPELINE_NAME = "rag-seldon-core-v2"
NAMESPACE = "seldon"

    
endpoint = f"{SD_IP}/v2/models/rag-seldon-core-v2/infer"



request = {
            "inputs": [
                {
                    "name": "role", 
                    "shape": [1, 1],
                    "datatype": "BYTES", 
                    "data": ['user'],
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
                }
            ]
        }
headers = {
    "Seldon-Model": f"{PIPELINE_NAME}.pipeline",
    "Host": f"{NAMESPACE}.inference.seldon",
    "Content-Type": "application/json"
}
print(headers)
r = requests.post(endpoint, json=request, headers=headers, verify=False)
print(r)
print(r.json()['outputs'])


