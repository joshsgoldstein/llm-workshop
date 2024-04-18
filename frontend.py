#!/usr/bin/env python3
from logic import APIController
from typing import List, Tuple
from nicegui import Client, ui
import asyncio


llm = APIController()

messages: List[Tuple[str, str, str]] = []
thinking: bool = False


@ui.refreshable
async def chat_messages() -> None:
    for name, text in messages:
        ui.chat_message(text=text, name=name, sent=name == 'You')
    if thinking:
        ui.spinner(size='3rem').classes('self-center')
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)


@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        global thinking
        message = text.value
        messages.append(('You', text.value))
        thinking = True
        text.value = ''
        chat_messages.refresh()
        response = await llm.send(message)
        messages.append(('Bot', response))
        thinking = False
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration: none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            text = (ui
                .input(placeholder='message')
                .props('rounded outlined input-class=mx-3')
                .classes('w-full self-center')
                .on('keydown.enter', send)
            )


ui.run(port=7070, title='Chat with GPT-3 (example)')