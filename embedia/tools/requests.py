from embedia.tool import Tool
import aiohttp
from typing import Optional
import json


class HTTPGet(Tool):
    def __init__(self):
        super().__init__(name="HTTP Get",
                         desc="Make a HTTP GET request",
                         examples="https://www.google.com",
                         args="url: str, headers: Optional[dict] = None",
                         returns="response: str, status: int")

    async def _run(self, url: str, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text(), response.status


class HTTPPost(Tool):
    def __init__(self):
        super().__init__(name="HTTP Post",
                         desc="Make a HTTP POST request",
                         examples="https://www.google.com",
                         args="url: str, data: dict, headers: Optional[dict] = None",
                         returns="response: str, status: int")

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), response.status


class HTTPPut(Tool):
    def __init__(self):
        super().__init__(name="HTTP Put",
                         desc="Make a HTTP PUT request",
                         examples="https://www.google.com",
                         args="url: str, data: dict, headers: Optional[dict] = None",
                         returns="response: str, status: int")

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), response.status


class HTTPDelete(Tool):
    def __init__(self):
        super().__init__(name="HTTP Delete",
                         desc="Make a HTTP DELETE request",
                         examples="https://www.google.com",
                         args="url: str, headers: Optional[dict] = None",
                         returns="response: str, status: int")

    async def _run(self, url: str, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                return await response.text(), response.status


class HTTPPatch(Tool):
    def __init__(self):
        super().__init__(name="HTTP Patch",
                         desc="Make a HTTP PATCH request",
                         examples="https://www.google.com",
                         args="url: str, data: dict, headers: Optional[dict] = None",
                         returns="response: str, status: int")

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), response.status
