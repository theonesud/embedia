import json
import os
import pytest
import shutil

from embedia import TextDoc, VectorDBInsert, VectorDBGetSimilar
from tests.core.definitions import (WeaviateDB, OpenAIEmbedding)


@pytest.mark.asyncio
async def test_vectordb():
    embmodel = OpenAIEmbedding()
    shutil.rmtree('temp', ignore_errors=True)
    os.makedirs('temp')
    db = WeaviateDB()
    doc = TextDoc.from_file('./README.md', meta={'description': 'Readme file of Embedia'})

    linedocs = doc.split_on_separator()
    for line in linedocs:
        text = line.contents
        if line.meta:
            meta_str = json.dumps(line.meta)
            text = 'metadata:' + meta_str + '\n' + 'content:' + text
        emb = await embmodel(text)
        await db.insert(VectorDBInsert(id=line.id, text=line.contents, meta=line.meta, embedding=emb))

    query = "Advantages of Embedia"
    query_emb = await embmodel(query)
    results = await db.get_similar(VectorDBGetSimilar(
        embedding=query_emb, n_results=5))
    assert len(results) == 5
    for r in results:
        assert r[0] > 0.7

    shutil.rmtree('temp')
