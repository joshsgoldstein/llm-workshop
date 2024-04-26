import requests
import uuid
from utils import get_mesh_ip
import click
from api_controller import APIController


@click.command()
@click.option(
    '--memory_id',
    default=None,
    help='memory_id of conversation'
)
@click.option(
    '--target',
    prompt='the target llm. Choices: local, openai, local-gpu',
    help='the target llm. Choices: local, openai, local-gpu'
)
def chat(target, memory_id):
    assert target in ['local', 'openai', 'local-gpu'], "target must be either local, local-gpu or chatgpt"
    api = APIController(session=memory_id, target=target)

    while True:
        text = input("Enter text: ")
        if text == 'exit':
            break
        response = api.sync_send(text)
        print(response)


if __name__ == '__main__':
    chat()