import pytest
from embedia.textdoc import TextDoc


@pytest.mark.asyncio
async def test_textdoc_split():
    with open('README.md', 'r', encoding='utf-8') as f:
        text = f.read()

    textdoc = TextDoc(
        name='README.md', description='Overview of Embedia repo, usage guide, and helpful links',
        contents=text, src='./README.md')
    parent_id = textdoc.id
    child_docs = textdoc.split_on_separator(separator='\n', strip_spaces=False)
    assert len(child_docs) > 0
    for child in child_docs:
        assert child.parent_id == parent_id


@pytest.mark.asyncio
async def test_extract_regex():
    textdoc = TextDoc.from_file('./README.md',
                                'README.md',
                                ('Overview of Embedia repo,'
                                 ' usage guide, and helpful links'),
                                './README.md')
    parent_id = textdoc.id
    child_docs = textdoc.extract_regex(pattern=r'```(.*?)```')
    assert len(child_docs) > 0
    for child in child_docs:
        assert child.parent_id == parent_id
