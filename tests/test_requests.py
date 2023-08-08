from embedia.tools.requests import HTTPGet, HTTPPost, HTTPPut, HTTPDelete, HTTPPatch
import pytest


@pytest.mark.asyncio
async def test_http_get():
    http_get = HTTPGet()
    response = await http_get.run("https://jsonplaceholder.typicode.com/posts/1")
    assert isinstance(response[0], str)
    assert len(response[0]) > 2
    assert response[1] == 200

    response = await http_get.run("https://jsonplaceholder.typicode.com/postzzs/1")
    assert isinstance(response[0], str)
    assert len(response[0]) == 2
    assert response[1] == 404


@pytest.mark.asyncio
async def test_http_post():
    http_post = HTTPPost()
    response = await http_post.run("https://jsonplaceholder.typicode.com/posts",
                                   {"title": "foo", "body": "bar", "userId": 1},
                                   {"Content-type": "application/json; charset=UTF-8"})
    assert isinstance(response[0], str)
    assert len(response[0]) > 2
    assert response[1] == 201


@pytest.mark.asyncio
async def test_http_put():
    http_put = HTTPPut()
    response = await http_put.run("https://jsonplaceholder.typicode.com/posts/1",
                                  {"title": "foo", "body": "bar", "userId": 1},
                                  {"Content-type": "application/json; charset=UTF-8"})
    assert isinstance(response[0], str)
    assert len(response[0]) > 2
    assert response[1] == 200


@pytest.mark.asyncio
async def test_http_patch():
    http_patch = HTTPPatch()
    response = await http_patch.run("https://jsonplaceholder.typicode.com/posts/1",
                                    {"title": "fooz"},
                                    {"Content-type": "application/json; charset=UTF-8"})
    assert isinstance(response[0], str)
    assert len(response[0]) > 2
    assert response[1] == 200


@pytest.mark.asyncio
async def test_http_delete():
    http_delete = HTTPDelete()
    response = await http_delete.run("https://jsonplaceholder.typicode.com/posts/1")
    assert isinstance(response[0], str)
    assert len(response[0]) == 2
    assert response[1] == 200
