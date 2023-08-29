import pytest
from tests.core.definitions import SleepTool, PrintTool, PrintToolBroken1, PrintToolBroken2, PrintToolBroken3, \
    PrintToolBroken4, PrintToolBroken5, PrintToolBroken6, PrintToolBroken7, PrintToolBroken8, PrintToolBroken9, \
    PrintToolBroken10, PrintToolBroken11, PrintToolBroken12
from embedia.utils.exceptions import UserDeniedError, DefinitionError


@pytest.mark.asyncio
async def test_sleep_tool():
    sleeptool = SleepTool()
    output = await sleeptool()
    assert output[0] == None
    assert output[1] == 0


@pytest.mark.asyncio
async def test_print_tool(monkeypatch):
    # monkeypatch.setattr('builtins.input', lambda _: 'y')
    printtool = PrintTool()
    output = await printtool('Hello World')
    assert output[0] == None
    assert output[1] == 0


@pytest.mark.asyncio
async def test_print_denied(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    printtool = PrintTool()
    with pytest.raises(UserDeniedError) as e:
        await printtool('Hello World')
    print(e)


@pytest.mark.asyncio
async def test_print_tool_error(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken2()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken3()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken4()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken5()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken6()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken7()
    print(e)
    with pytest.raises(DefinitionError) as e:
        PrintToolBroken8()
    print(e)
    with pytest.raises(DefinitionError) as e:
        printtool = PrintToolBroken9()
        await printtool('Hello World')
    print(e)
    with pytest.raises(DefinitionError) as e:
        printtool = PrintToolBroken10()
        await printtool('Hello World')
    print(e)
    with pytest.raises(DefinitionError) as e:
        printtool = PrintToolBroken11()
        await printtool('Hello World')
    print(e)
    with pytest.raises(DefinitionError) as e:
        printtool = PrintToolBroken12()
        await printtool('Hello World')
    print(e)
