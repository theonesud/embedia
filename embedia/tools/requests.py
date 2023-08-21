import json
from typing import Optional

import aiohttp

from embedia.core.tool import Tool


class HTTPGet(Tool):
    def __init__(self):
        super().__init__(name="HTTP Get",
                         desc="Make a HTTP GET request",
                         args={'url': 'The URL to make the request to',
                               'headers': 'Optional headers dictionary to send with the request'})

    async def _run(self, url: str, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text(), 0


class HTTPPost(Tool):
    def __init__(self):
        super().__init__(name="HTTP Post",
                         desc="Make a HTTP POST request",
                         args={'url': 'The URL to make the request to',
                               'data': 'The data to send with the request',
                               'headers': 'Optional headers dictionary to send with the request'})

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), 0


class HTTPPut(Tool):
    def __init__(self):
        super().__init__(name="HTTP Put",
                         desc="Make a HTTP PUT request",
                         args={'url': 'The URL to make the request to',
                               'data': 'The data to send with the request',
                               'headers': 'Optional headers dictionary to send with the request'})

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), 0


class HTTPDelete(Tool):
    def __init__(self):
        super().__init__(name="HTTP Delete",
                         desc="Make a HTTP DELETE request",
                         args={'url': 'The URL to make the request to',
                               'headers': 'Optional headers dictionary to send with the request'})

    async def _run(self, url: str, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url, headers=headers) as response:
                return await response.text(), 0


class HTTPPatch(Tool):
    def __init__(self):
        super().__init__(name="HTTP Patch",
                         desc="Make a HTTP PATCH request",
                         args={'url': 'The URL to make the request to',
                               'data': 'The data to send with the request',
                               'headers': 'Optional headers dictionary to send with the request'})

    async def _run(self, url: str, data: dict, headers: Optional[dict] = None):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=json.dumps(data), headers=headers) as response:
                return await response.text(), 0
