"""

Sample bot that wraps ChatGPT but makes responses use all-caps.

"""
from typing import AsyncIterable
from fastapi import FastAPI, Form, Response
from fastapi.responses import HTMLResponse
from fastapi_poe import PoeBot
from fastapi_poe.client import stream_request
from fastapi_poe.types import (
    PartialResponse,
    QueryRequest,
    SettingsRequest,
    SettingsResponse,
)

class ChatGPTAllCapsBot(PoeBot):
    async def get_response(self, query: QueryRequest) -> AsyncIterable[PartialResponse]:
        async for msg in stream_request(query, "ChatGPT", query.access_key):
            yield msg.model_copy(update={"text": msg.text.upper()})

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(server_bot_dependencies={"ChatGPT": 1})

fastapi_app = FastAPI()

@fastapi_app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <form method="post">
        <input type="text" name="query" />
        <input type="submit" />
    </form>
    """

@fastapi_app.post("/")
async def chatgpt_allcapsbot_endpoint(query: str = Form(...)):
    bot = ChatGPTAllCapsBot()
    responses = []
    async for response in bot.get_response(QueryRequest(query=query)):
        responses.append(response)
    return responses
