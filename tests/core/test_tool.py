import pytest
from tests.definitions import SleepTool, PrintTool
from embedia.utils.exceptions import DeniedByUserError


@pytest.mark.asyncio
async def test_sleep_tool():
    sleeptool = SleepTool()
    output = await sleeptool()
    assert output[0] == None
    assert output[1] == 0


@pytest.mark.asyncio
async def test_print_tool(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    printtool = PrintTool()
    output = await printtool('Hello World')
    assert output[0] == None
    assert output[1] == 0


@pytest.mark.asyncio
async def test_print_denied(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    printtool = PrintTool()
    with pytest.raises(DeniedByUserError):
        await printtool('Hello World')
