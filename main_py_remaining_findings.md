# Code Review — Remaining Findings for `src/main.py`

**Status:** 2 of 5 findings resolved; 3 remain unfixed (as of Oct 2026).

## Resolved

The two critical findings were fixed in commit `87f98ac` (`fix(main): fix generate_page template replacement and add file validation`):

1. Discarded `str.replace` results — the template replacement chain did not assign its result, so `{{ Title }}` / `{{ Content }}` were never substituted.
2. Missing file-existence checks for the source markdown and template files before `open()`.

## Remaining Findings

### 1. Medium — Off-by-one slice in `extract_title` (`main.py:15`)

```python
if line.startswith("# "):
    return line[1:].strip()
```

**What's wrong:** The guard matches `"# "` (two characters) but the slice strips only one (`line[1:]`), keeping the `#` character in the returned title.

**Why it still works:** The leading space left by the slice is removed by `.strip()`, masking the bug. Any change to the whitespace handling would surface `#` in generated titles.

**Suggested fix:** Slice off both characters — `line[2:].strip()` — or, more robustly, use `line.removeprefix("# ").strip()`.

### 2. Critical — Unreachable/dead destination-directory logic in `generate_page` (`main.py:23-29`)

```python
if not os.path.lexists(dst_path):
    os.makedirs(dst_path)
```

**What's wrong:** The validation branches for `dst_path` are nested inside a check that the path does *not* exist. A non-existent path can never be a directory, so the "is a directory" error branch is dead code. A missing `dst_path` always falls through to `SystemExit(1)` with a misleading "is not a directory" error. Conversely, an existing regular file at `dst_path` bypasses validation entirely and crashes later at `open(...)` with `NotADirectoryError`.

**Suggested fix:** Un-nest the logic:

- `if not os.path.exists(dst_path): os.makedirs(dst_path, exist_ok=True)`
- `elif not os.path.isdir(dst_path):` → log the error and exit.

### 3. Low — Debug leftovers

- `main()` reads `tests/test.md` and `print()`s the extracted title (`main.py:82-84`) before `logging.basicConfig()` is configured; it fails with `FileNotFoundError` if the test asset is absent.
- `print(src_html_str)` inside `generate_page` (`main.py:34`) pollutes stdout.

**Context:** These were deliberately left in when committing (commit-as-is decision). They are development/debug artifacts, not production logic.

**Suggested fix:** Remove both debug blocks (or gate them behind a debug flag / move the title check after logging setup).

## Cosmetic (not counted)

- The template-existence error messages inside `generate_page` (`main.py:37, 39`) are mislabeled "Source file" where they refer to `tmpl_file`. Cosmetic; reword to "Template file".
