from utils import get_mesh_ip
import requests


SD_IP = ""
endpoint = f"http://{get_mesh_ip()}/v2/models/rag-seldon-core-v2/infer"

def send_request(text, state_id):
    request = {
        "inputs": 
            [
                {
                    "name": "input",
                    "shape": [1],
                    "datatype": "BYTES",
                    "data": [text],
                    "parameters": {"content_type": "str"},
                },
                {
                    "name": "state_id", 
                    "shape": [1, 1],
                    "datatype": "BYTES", 
                    "data": [state_id]
                }
            ]
    }
    headers = {
        "Content-Type": "application/json",
        "seldon-model": "rag-seldon-core-v2.pipeline"
    }
    r = requests.post(endpoint, json=request, headers=headers)
    return r.json()['outputs'][0]['data'][0]


if __name__ == '__main__':
    state_id = input('Enter your state_id: ')
    while True:
        text = input('Enter your message: ')
        if text == 'exit':
            break
        r = send_request(text, state_id)
        print(r)
