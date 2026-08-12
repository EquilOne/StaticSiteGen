# StaticSiteGen

A static site generator written in pure Python 3 stdlib with no third-party dependencies. MIT-licensed boot.dev learning project, currently in active development — HTML node conversion, text splitting, and markdown block parsing are being built incrementally, so this is a partial implementation, not a finished product.

## Quickstart

All commands run from the repo root. `main.sh` and `test.sh` are thin wrappers.

```sh
bash main.sh   # run the generator (python3 -m src.main)
bash test.sh   # run all tests (python3 -m unittest discover)
```

Run a single test file:

```sh
python3 -m unittest discover -p test_blocks.py
```

Note: `src/main.py` uses package imports (`from src.htmlnode import ...`), so it must run as a module — `python3 src/main.py` fails with `ModuleNotFoundError`. Plain `unittest discover` works because both `src/` and `tests/` are packages; do not pass `-s src`.

## Architecture

- `src/` — package (`__init__.py`)
  - `main.py` — entrypoint
  - `htmlnode.py` — `HTMLNode`, `LeafNode`, `ParentNode`
  - `textnode.py` — `TextNode`, `TextType`, `text_node_to_html_node()`
  - `helpers.py` — `split_nodes_delimiter()`, `extract_markdown_images()`, `extract_markdown_links()`
  - `blocks.py` — `BlockType`, `markdown_to_blocks()`, `block_to_block_type()`
- `tests/` — package of unittest files (e.g. `test_blocks.py`) importing `from src...`

`pyproject.toml` is a stub (only `name = "staticsitegen"`) — no build config.