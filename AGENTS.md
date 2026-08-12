# Static Site Generator — Boot.dev Project

Pure Python 3 stdlib static site generator. Learning project, MIT License.

## Commands

Run from repo root. `main.sh` and `test.sh` are thin wrappers.

- **Run**: `bash main.sh` — executes `python3 -m src.main` (module form, NOT `python3 src/main.py`)
- **Test all**: `bash test.sh` — executes `python3 -m unittest discover` (no args)
- **Single test file**: `python3 -m unittest discover -p test_blocks.py` (from repo root)

## Architecture

- `src/main.py` — entrypoint; imports `from src.htmlnode import ...`
- `src/htmlnode.py` — `HTMLNode`, `LeafNode`, `ParentNode`
- `src/textnode.py` — `TextNode`, `TextType`, `text_node_to_html_node()`
- `src/blocks.py` — `BlockType`, `markdown_to_blocks()`, `block_to_block_type()`
- `src/helpers.py` — `split_nodes_delimiter()`, `extract_markdown_images()` / `extract_markdown_links()`
- `tests/` — `test_blocks.py`, `test_helpers.py`, `test_htmlnode.py`, `test_textnode.py`
- `public/` — `index.html`, `styles.css` sample static assets

## Gotchas

1. **Use plain discovery — no `-s src`**: `src/__init__.py` and `tests/__init__.py` exist; tests import `from src.blocks import ...`. Bare `python3 -m unittest discover` recurses into `tests/` and finds them. `-s src` points discovery into `src/` and misses the `tests/` tree — 0 tests run.

2. **Always run as a module**: every src module uses package imports (`from src.textnode import ...`), so `python3 src/main.py` fails with `ModuleNotFoundError`. Use `python3 -m src.main`.

3. **`pyproject.toml` is a stub**: only declares `name = "staticsitegen"`. No build config, no `requirements.txt`, no venv — stdlib only.

4. **No linter/formatter/typechecker configured**: `opencode.json` only sets `"lsp": true`, and there is no CI. If the user asks for tooling, set it up — don't assume defaults.