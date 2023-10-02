import pytest
from embedia.utils.exceptions import DefinitionError, UserDeniedError

from tests.core.definitions import (
    PrintTool,
    PrintToolBroken1,
    PrintToolBroken2,
    PrintToolBroken3,
    SleepTool,
)


@pytest.mark.asyncio
async def test_sleep_tool():
    sleeptool = SleepTool()
    output = await sleeptool()
    assert output.output == "done"
    assert output.exit_code == 0


@pytest.mark.asyncio
async def test_print_tool(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    printtool = PrintTool()
    output = await printtool("Hello World")
    assert output.output == "done"
    assert output.exit_code == 0


@pytest.mark.asyncio
async def test_print_denied(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    printtool = PrintTool()
    with pytest.raises(UserDeniedError) as e:
        await printtool("Hello World")
    error_str = str(e)
    error_str = error_str.replace('"', "'")
    assert "Tool: PrintTool Details: {'text': 'Hello World'}" in error_str


@pytest.mark.asyncio
async def test_print_tool_error(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken1()
    error_str = str(e)
    error_str = error_str.replace('"', "'")
    assert (
        "PrintToolBroken1._run expects parameters: ['self', 'texts'], got: ['self', 'text']"
        in error_str
    )

    printtool = PrintToolBroken2()
    with pytest.raises(TypeError) as e:
        await printtool("Hello World")
    error_str = str(e)
    error_str = error_str.replace('"', "'")
    assert (
        "Func: PrintToolBroken2._run output expected type: <class 'embedia.schema.tool.ToolReturn'>"
        in error_str
    )

    printtool = PrintToolBroken3()
    with pytest.raises(NotImplementedError) as e:
        await printtool("Hello World")
    error_str = str(e)
    error_str = error_str.replace('"', "'")
    assert (
        "Please call `Tool` init method from your subclass init method with the Tool's documentation"
        in error_str
    )
