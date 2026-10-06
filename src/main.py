import logging
import os
import shutil

from src.constant import DST_DIR, PROJECT_ROOT, SRC_DIR

logger = logging.getLogger(__name__)


def extract_title(markdown: str) -> str:
    lines: list[str] = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip()

    raise ValueError("No title found in markdown")


def _copy_files(
    src_path: str | os.PathLike[str], dst_path: str | os.PathLike[str]
) -> None:
    """Recursively copy the contents of src_path into dst_path.

    dst_path must not exist; the caller validates src and cleans dst first.
    Skips symlinks; warns and skips entries that are neither regular
    files nor directories."""

    logger.debug(
        "Creating directory '%s' in '%s'",
        os.path.basename(dst_path),
        os.path.dirname(os.path.normpath(dst_path)),
    )
    os.mkdir(dst_path)

    src_dir_contents = sorted(os.listdir(src_path))
    for item in src_dir_contents:
        item_path = os.path.join(src_path, item)
        if os.path.islink(item_path):
            continue
        elif os.path.isdir(item_path):
            _copy_files(item_path, os.path.join(dst_path, item))
        elif os.path.isfile(item_path):
            logger.debug("Copying '%s' --> '%s'", item, dst_path)
            shutil.copy2(item_path, dst_path)
        else:
            logger.warning("Unsupported file %s, skipping", item_path)


def main() -> None:

    with open(os.path.join(PROJECT_ROOT, "tests/test.md"), "r", encoding="utf-8") as f:
        content = f.read()
    print(extract_title(content))

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        if not os.path.exists(SRC_DIR):
            raise FileNotFoundError(f"Source directory '{SRC_DIR}' does not exist")
        if not os.path.isdir(SRC_DIR):
            raise NotADirectoryError(f"Source directory '{SRC_DIR}' is not a directory")
        if SRC_DIR.resolve().is_relative_to(
            DST_DIR.resolve()
        ) or DST_DIR.resolve().is_relative_to(SRC_DIR.resolve()):
            raise ValueError(
                "Source and destination directories must not be the same or a subdirectory of each other"
            )
        if os.path.lexists(DST_DIR):
            if os.path.islink(DST_DIR):
                logger.debug("%s is a symlink, performing cleanup", DST_DIR)
                os.unlink(DST_DIR)
            elif os.path.isdir(DST_DIR):
                logger.info(
                    "Directory '%s' already exists, performing cleanup.", DST_DIR
                )
                shutil.rmtree(DST_DIR)
                logger.info("Cleanup complete, '%s' removed.", DST_DIR)
            else:
                logger.debug("%s is not a directory, performing cleanup", DST_DIR)
                os.unlink(DST_DIR)
        logger.info("Copying files from '%s' --> '%s'", SRC_DIR, DST_DIR)
        _copy_files(SRC_DIR, DST_DIR)
        logger.info("Successfully copied files from '%s' --> '%s'", SRC_DIR, DST_DIR)

    except OSError as e:
        logger.error("Static site generation failed: %s", e)
        raise SystemExit(1)
    except ValueError as e:
        logger.error("Static site generation failed: %s", e)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
