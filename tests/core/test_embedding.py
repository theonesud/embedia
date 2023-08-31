import json

import pytest

from embedia import TextDoc
from embedia.utils.exceptions import DefinitionError
from tests.core.definitions import (OpenAIEmbedding, OpenAIEmbeddingBroken1,
                                    OpenAIEmbeddingBroken2)

lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis eu arcu risus. Proin sed fringilla tellus. Donec scelerisque elit sed sapien bibendum rutrum. Morbi blandit justo in urna semper volutpat. Nunc consectetur ex vitae consequat blandit. Duis sit amet metus quis mi molestie bibendum rutrum et ante. Nam aliquam metus magna, eget porta lacus dictum sit amet. Morbi dictum tellus a semper tristique. Duis ipsum ex, pharetra non rhoncus in, gravida quis magna. Nam pretium enim non lectus efficitur, sit amet sagittis elit finibus. Vivamus varius ligula turpis, sit amet vehicula mi eleifend eget. Cras dignissim mauris eu feugiat euismod. Integer dapibus dolor eu nulla euismod finibus."""


@pytest.mark.asyncio
async def test_emb_model():
    embmodel = OpenAIEmbedding()

    emb = await embmodel(lorem)
    assert len(emb) == 1536

    doc = TextDoc.from_file('./README.md')
    text = doc.contents
    if doc.meta:
        meta_str = json.dumps(doc.meta)
        text = 'metadata:' + meta_str + '\n' + 'content:' + text
    emb = await embmodel(text)
    assert len(emb) == 1536


@pytest.mark.asyncio
async def test_emb_model_error():
    embmodel = OpenAIEmbedding()
    with pytest.raises(DefinitionError) as e:
        await embmodel(5)
    print(e)
    with pytest.raises(DefinitionError) as e:
        await embmodel('')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await embmodel([])
    print(e)
    with pytest.raises(DefinitionError) as e:
        OpenAIEmbeddingBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        embmodel = OpenAIEmbeddingBroken2()
        await embmodel(lorem)
    print(e)
