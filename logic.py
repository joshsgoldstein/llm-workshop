from utils import get_mesh_ip
import requests
import aiohttp
import uuid


class APIController():
    endpoint = f"http://{get_mesh_ip()}/v2/models/rag-seldon-core-v2/infer"

    def __init__(self):
        self.state_id = str(uuid.uuid4())

    def _build_openai_request(self, text):
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
                        "data": [self.state_id]
                    }
                ]
        }
        headers = {
            "Content-Type": "application/json",
            "seldon-model": "rag-seldon-core-v2.pipeline"
        }
        return request, headers

    async def send(self, text):
        request, headers = self._build_openai_request(text)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, json=request, headers=headers) as response:
                json = await response.json(content_type='text/plain')
                return json['outputs'][0]['data']

    def sync_send(self, text):
        request, headers = self._build_openai_request(text)
        return requests.post(self.endpoint, json=request, headers=headers)