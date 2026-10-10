# StaticSiteGen

A static site generator written in pure Python 3 stdlib with no third-party dependencies. MIT-licensed boot.dev learning project. It converts the markdown under `content/` into HTML pages, applies a shared template, and writes the finished site (plus copied static assets) to `docs/`. The live site is served via GitHub Pages from `/docs` on branch `main` (repo: `EquilOne/StaticSiteGen`).

## Quickstart

All commands run from the repo root. `main.sh`, `build.sh`, and `test.sh` are thin wrappers.

```sh
bash build.sh  # build the site with the /StaticSiteGen/ basepath (GitHub Pages)
bash main.sh   # build the site, then serve it on :8888
bash test.sh   # run all tests (python3 -m unittest discover, 164 tests)
```

- `build.sh` runs `python3 -m src.main "/StaticSiteGen/"` — the basepath argument makes all `href="/...` and `src="/...` attributes point under `/StaticSiteGen/` so the site works from a GitHub Pages project URL.
- `main.sh` runs `python3 -m src.main` (basepath defaults to `/`), then serves the build from `docs/` on `http://localhost:8888`.

Run a single test file:

```sh
python3 -m unittest discover -p test_blocks.py
```

Note: `src/main.py` uses package imports (`from src.htmlnode import ...`), so it must run as a module — `python3 src/main.py` fails with `ModuleNotFoundError`. Plain `unittest discover` works because both `src/` and `tests/` are packages; do not pass `-s src`.

## Architecture

- `src/` — package (`__init__.py`)
  - `main.py` — entrypoint; reads `basepath` from `sys.argv[1]` (defaults to `/`), validates and cleans `docs/`, copies `static/` assets, then generates all pages
  - `page.py` — `generate_page()`, `generate_pages_recursive()`; renders markdown pages through the template and rewrites `href="/` / `src="/` prefixes to the given `basepath`
  - `files.py` — `_copy_files()`; recursive static-asset copy (skips symlinks)
  - `convert.py` — `markdown_to_html_node()`; markdown string → HTML node tree
  - `blocks.py` — `BlockType`, `markdown_to_blocks()`, `block_to_block_type()`, `extract_title()`
  - `helpers.py` — `text_to_textnodes()`, `split_nodes_delimiter()`, `extract_markdown_images()`, `extract_markdown_links()`
  - `htmlnode.py` — `HTMLNode`, `LeafNode`, `ParentNode`
  - `textnode.py` — `TextNode`, `TextType`, `text_node_to_html_node()`
  - `constant.py` — path constants: `SRC_DIR` (`static/`), `DST_DIR` (`docs/`), `CONTENT_DIR` (`content/`)
- `content/` — site markdown (`index.md`, `blog/`, `contact/`)
- `static/` — copied assets (`images/`, `index.css`)
- `template.html` — shared page template (`{{ Title }}`, `{{ Content }}`)
- `docs/` — generated site output (GitHub Pages serves from here)
- `tests/` — package of unittest files (`test_blocks.py`, `test_convert.py`, `test_helpers.py`, `test_htmlnode.py`, `test_textnode.py`) importing `from src...`

Each markdown file `foo.md` renders to `<dst>/foo/index.html` (`index.md` renders in place as `index.html`), mirroring the `content/` directory structure.

`pyproject.toml` is a stub (only `name = "staticsitegen"`) — no build config.