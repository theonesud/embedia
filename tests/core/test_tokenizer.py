import pytest
from tests.core.definitions import OpenAITokenizer, OpenAITokenizerBroken1, OpenAITokenizerBroken2
from embedia.utils.exceptions import DefinitionError


text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eu arcu risus. Proin sed fringilla tellus. Donec scelerisque elit sed sapien bibendum rutrum. Morbi blandit justo in urna semper volutpat. Nunc consectetur ex vitae consequat blandit. Duis sit amet metus quis mi molestie bibendum rutrum et ante. Nam aliquam metus magna, eget porta lacus dictum sit amet. Morbi dictum tellus a semper tristique. Duis ipsum ex, pharetra non rhoncus in, gravida quis magna. Nam pretium enim non lectus efficitur, sit amet sagittis elit finibus. Vivamus varius ligula turpis, sit amet vehicula mi eleifend eget. Cras dignissim mauris eu feugiat euismod. Integer dapibus dolor eu nulla euismod finibus."""


@pytest.mark.asyncio
async def test_tokenizer():
    tokenizer = OpenAITokenizer()
    tokens = await tokenizer(text)
    assert len(text.split()) == 107
    assert len(tokens) == 192


@pytest.mark.asyncio
async def test_tokenizer_error():
    tokenizer = OpenAITokenizer()
    with pytest.raises(DefinitionError) as e:
        await tokenizer('')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await tokenizer(4)
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAITokenizerBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        tokenizer = OpenAITokenizerBroken2()
        await tokenizer(text)
    print(e)
