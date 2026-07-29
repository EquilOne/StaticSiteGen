# Static Site Generator — Boot.dev Project

Pure Python 3 stdlib static site generator. Learning project, MIT License.

## Commands

- **Run**: `bash main.sh` or `python3 src/main.py`
- **Test all**: `bash test.sh` (equiv. `python3 -m unittest discover -s src`)
- **Single test**: `python3 -m unittest discover -s src -p test_splitnodes.py`

## Architecture

| File | Purpose |
|------|---------|
| `src/main.py` | Entrypoint — creates sample nodes, prints their repr |
| `src/htmlnode.py` | `HTMLNode` (base), `LeafNode` (tag+value), `ParentNode` (tag+children) |
| `src/textnode.py` | `TextNode`, `TextType` enum, `text_node_to_html_node()` converter |
| `src/splitnodes.py` | `split_nodes_delimiter()` — splits text nodes by delimiter markers |
| `public/index.html` | Sample static HTML |
| `public/styles.css` | Sample CSS |

## Repo Quirks

1. **Test discovery requires `-s src`**: `python3 -m unittest discover` (no `-s src`) runs 0 tests. Always use `bash test.sh` or `python3 -m unittest discover -s src`. No `__init__.py` files exist — `src/` is not a package.

2. **`splitnodes.py` has a script-level invocation**: Lines 27-33 run `split_nodes_delimiter` on test cases at import time. This executes on module import but does not affect unit tests.

3. **No deps, no config**: Pure Python 3 stdlib. No `requirements.txt`, `pyproject.toml`, venv, mypy, ruff, black, or CI. `opencode.json` only sets `lsp: true`.

4. **No linter/formatter/typechecker**: None configured. If the user asks for one, set it up — don't assume defaults.