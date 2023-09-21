import pytest
from embedia import TextDoc


@pytest.mark.asyncio
async def test_textdoc():
    doc = TextDoc.from_file(
        "./README.md", meta={"description": "Readme file of Embedia"}
    )
    parent_id = doc.id
    linedocs = doc.split_on_separator()
    assert len(linedocs) > 0
    for line in linedocs:
        assert line.meta["parent_id"] == parent_id
        assert line.id != parent_id

    codeblocks = doc.extract_regex(pattern=r"```(.*?)```")
    assert len(codeblocks) > 0
    for codeblock in codeblocks:
        assert codeblock.meta["parent_id"] == parent_id
        assert codeblock.id != parent_id
