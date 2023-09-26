from typing import AsyncIterable
from fastapi import FastAPI, Form
from fastapi_poe import PoeBot
from fastapi_poe.client import stream_request
from fastapi_poe.types import (
    PartialResponse,
    QueryRequest,
    SettingsRequest,
    SettingsResponse,
)

# 您的訪問鍵
access_key = "Yz8iDdVhBI5KscIHGIZvIXky504FBO8x"

class ChatGPTBot(PoeBot):
    async def get_response(self, query: QueryRequest) -> AsyncIterable[PartialResponse]:
        async for msg in stream_request(query, "ChatGPT", access_key):
            yield msg

    async def get_settings(self, setting: SettingsRequest) -> SettingsResponse:
        return SettingsResponse(server_bot_dependencies={"ChatGPT": 1})

fastapi_app = FastAPI()

@fastapi_app.post("/chatgpt")
async def chatgpt_endpoint(query: str = Form(...)):
    bot = ChatGPTBot()
    responses = []
    async for response in bot.get_response(QueryRequest(query=query)):
        responses.append(response)
    return responses

