# Static Site Generator — Boot.dev Project

Pure Python 3 stdlib static site generator. Learning project, MIT License.

## Commands

- **Run**: `bash main.sh` or `python3 src/main.py`
- **Test all**: `python3 -m unittest discover`
- **Test src only**: `bash test.sh` (equiv. `python3 -m unittest discover -s src`)
- **Single test**: `python3 -m unittest test_spitnodes.py`

## Architecture

| File | Purpose |
|------|---------|
| `src/main.py` | Entrypoint — creates sample nodes, prints their repr |
| `src/htmlnode.py` | `HTMLNode` (base), `LeafNode` (tag+value), `ParentNode` (tag+children) |
| `src/textnode.py` | `TextNode`, `TextType` enum, `text_node_to_html_node()` converter |
| `src/splitnodes.py` | `split_nodes_delimiter()` — WIP, incomplete, no return statement |
| `public/index.html` | Sample static HTML |
| `public/styles.css` | Sample CSS |

## Repo Quirks

1. **Test file outside `src/`**: `test_spitnodes.py` lives at the repo root, not in `src/`. The `test.sh` script (`discover -s src`) skips it. To run all tests use `python3 -m unittest discover` (no `-s src`).

2. **`splitnodes.py` is broken**: `split_nodes_delimiter()` has no `return` — it prints debug output and returns `None`. The test file expects a return value. This is work-in-progress.

3. **No deps, no config**: Pure Python 3 stdlib. No `requirements.txt`, `pyproject.toml`, venv, mypy, ruff, black, or CI. `opencode.json` only sets `lsp: true`.

4. **No linter/formatter/typechecker**: None configured. If the user asks for one, set it up — don't assume defaults.