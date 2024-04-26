import aiohttp
import uuid
from utils import get_mesh_ip
import requests


class APIController():
    def __init__(self, session=None, target='chatgpt'):
        self.session = str(uuid.uuid4()) if not session else session
        print('using memory_id:', self.session, 'target:', target)
        self.target = f'{target}-chat-memory'
        self.endpoint = f"http://{get_mesh_ip()}/v2/models/{self.target}/infer"


    def _build_request(self, question):
        inference_request = {
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
                    "data": [question],
                    "parameters": {"content_type": "str"},
                },
                {
                    "name": "memory_id", 
                    "shape": [1, 1],
                    "datatype": "BYTES", 
                    "data": [self.session],
                    "parameters": {"content_type": "str"},
                }
            ],
            "parameters": {"kwargs": "{'max_tokens': 100, 'ignore_eos': 'False'}"}
        }
        headers = {
            "Content-Type": "application/json",
            "seldon-model": f"{self.target}.pipeline"
        }
        return inference_request, headers


    async def async_send(self, text):
        inference_request, headers = self._build_request(text)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.endpoint, json=inference_request, headers=headers) as response:
                json = await response.json(content_type='text/plain')
                return json['outputs'][0]['data'][0]
            
    def sync_send(self, text):
        inference_request, headers = self._build_request(text)
        response = requests.post(self.endpoint, json=inference_request, headers=headers)
        values = self.unpack_response(response)
        return values
    
    def unpack_response(self, response):
        data = [output['data'] for output in response.json()['outputs'] if output['name'] == 'content']
        return data[0][0] if data else None
