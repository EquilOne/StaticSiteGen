def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        if not raw_block:
            continue
        blocks.append(raw_block.strip())
    return blocks
