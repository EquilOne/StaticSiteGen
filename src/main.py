import logging
import os
import shutil

from src.constant import DST_DIR, SRC_DIR

logger = logging.getLogger(__name__)


def _copy_files(
    src_path: str | os.PathLike[str], dst_path: str | os.PathLike[str]
) -> None:
    """Recursively copy the contents of src_path into dst_path.

    dst_path must not exist; the caller validates src and cleans dst first.
    Skips symlinks."""

    logger.debug(
        "Creating directory '%s' in '%s'",
        os.path.basename(dst_path),
        os.path.dirname(os.path.normpath(dst_path)),
    )
    os.mkdir(dst_path)

    src_dir_contents = os.listdir(src_path)
    for item in src_dir_contents:
        item_path = os.path.join(src_path, item)
        if os.path.islink(item_path):
            continue
        if os.path.isdir(item_path):
            _copy_files(item_path, os.path.join(dst_path, item))
        else:
            logger.debug("Copying '%s' to '%s'", item, dst_path)
            shutil.copy2(item_path, dst_path)


def main() -> None:

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        if not os.path.exists(SRC_DIR):
            raise FileNotFoundError(f"Source directory '{SRC_DIR.name}' does not exist")
        if not os.path.isdir(SRC_DIR):
            raise NotADirectoryError(
                f"Source directory '{SRC_DIR.name}' is not a directory"
            )
        if os.path.isdir(DST_DIR):
            logger.info(
                "Directory '%s' already exists, performing cleanup.", DST_DIR.name
            )
            shutil.rmtree(DST_DIR)
            logger.info("Cleanup complete, '%s' removed.", DST_DIR.name)
        _copy_files(SRC_DIR, DST_DIR)
    except OSError:
        logger.exception("Static site generation failed")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
