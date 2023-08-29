import pytest
from embedia import TextDoc
from tests.core.definitions import OpenAIEmbedding, ChromaDB, ChromaDBBroken1, ChromaDBBroken2, ChromaDBBroken3

from embedia.utils.exceptions import DefinitionError
import json


@pytest.mark.asyncio
async def test_vectordb():
    embmodel = OpenAIEmbedding()
    db = ChromaDB()
    doc = TextDoc.from_file('./README.md', meta={'description': 'Readme file of Embedia'})

    linedocs = doc.split_on_separator()
    for line in linedocs:
        text = line.contents
        if line.meta:
            meta_str = json.dumps(line.meta)
            text = 'metadata:' + meta_str + '\n' + 'content:' + text
        emb = await embmodel(text)
        await db.insert(line.id, line.contents, line.meta, emb)

    query = "Advantages of Embedia"
    query_emb = await embmodel(query)
    results = await db.get_similar(embedding=query_emb, n_results=5)
    assert len(results) == 5
    for r in results:
        assert r[0] > 0.7


@pytest.mark.asyncio
async def test_vectordb_error():
    db = ChromaDB()
    with pytest.raises(DefinitionError) as e:
        await db.insert(id=3, text='test', meta={}, embedding=[1, 2, 3])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='', text='test', meta={}, embedding=[1, 2, 3])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='123-123-12', text=4, meta={}, embedding=[1, 2, 3])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='123-123-12', text='', meta={}, embedding=[1, 2, 3])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='123-123-12', text='asdasd', meta=None, embedding=[1, 2, 3])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='123-123-12', text='asdasd', meta={}, embedding={})
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.insert(id='123-123-12', text='asdasd', meta={}, embedding=[])
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.get_similar(embedding=None, n_results=5)
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.get_similar(embedding=[], n_results=5)
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.get_similar(embedding=[1, 2, 3], n_results='5')
    print(e)
    with pytest.raises(DefinitionError) as e:
        await db.get_similar(embedding=[1, 2, 3], n_results=0)
    print(e)
    with pytest.raises(DefinitionError) as e:
        ChromaDBBroken1()
    print(e)
    with pytest.raises(DefinitionError) as e:
        ChromaDBBroken2()
    print(e)
    with pytest.raises(DefinitionError) as e:
        db = ChromaDBBroken3()
        await db.get_similar(embedding=[1, 2, 3], n_results=5)
    print(e)
