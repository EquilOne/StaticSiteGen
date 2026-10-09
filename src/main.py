import logging
import os
import shutil

from src.blocks import BlockType, block_to_block_type, markdown_to_blocks
from src.constant import DST_DIR, PROJECT_ROOT, SRC_DIR
from src.convert import markdown_to_html_node

logger = logging.getLogger(__name__)


def extract_title(markdown: str) -> str:
    blocks: list[str] = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) != BlockType.HEADING:
            continue
        lines: list[str] = block.splitlines()
        for line in lines:
            if line.startswith("# "):
                return line[2:].strip()

        raise ValueError("No title found in markdown")


def generate_page(src_file, tmpl_file, dst_path):
    logger.info("Generating page in %s from %s with %s", dst_path, src_file, tmpl_file)

    if os.path.lexists(dst_path):
        logger.debug("Destination path '%s' exists", dst_path)
        if os.path.islink(dst_path):
            logger.error("Destination path '%s' is a symlink", dst_path)
            raise SystemExit(1)
        elif os.path.isfile(dst_path):
            logger.error("Destination path '%s' is a file", dst_path)
            raise SystemExit(1)
        elif os.path.isdir(dst_path):
            logger.debug("Destination path '%s' is a directory", dst_path)
        else:
            logger.error("Destination path '%s' is of unknown type", dst_path)
            raise SystemExit(1)

    else:
        os.makedirs(dst_path)

    if not os.path.exists(src_file):
        logger.error("Source file '%s' does not exist", src_file)
        raise SystemExit(1)
    if os.path.isdir(src_file):
        logger.error("Source file '%s' is a directory", src_file)
        raise SystemExit(1)
    else:
        with open(src_file, "r", encoding="utf-8") as f:
            src_md_contents = f.read()
        src_html_str = markdown_to_html_node(src_md_contents).to_html()
        page_title = extract_title(src_md_contents)
        if not os.path.exists(tmpl_file):
            logger.error("Template file '%s' does not exist", tmpl_file)
            raise SystemExit(1)
        if os.path.isdir(tmpl_file):
            logger.error("Template file '%s' is a directory", tmpl_file)
            raise SystemExit(1)
        else:
            with open(tmpl_file, "r", encoding="utf-8") as f:
                tmpl_contents = f.read()
            contents = tmpl_contents.replace("{{ Title }}", page_title).replace(
                "{{ Content }}", src_html_str
            )
            with open(os.path.join(dst_path, "index.html"), "w", encoding="utf-8") as f:
                f.write(contents)


def _copy_files(
    src_path: str | os.PathLike[str], dst_path: str | os.PathLike[str]
) -> None:
    """Recursively copy the contents of src_file into dst_path.

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

    generate_page(
        os.path.join(PROJECT_ROOT, "content/index.md"),
        os.path.join(PROJECT_ROOT, "template.html"),
        os.path.join(PROJECT_ROOT, "public"),
    )


if __name__ == "__main__":
    main()
