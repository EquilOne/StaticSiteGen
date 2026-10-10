import logging
import os
import shutil

logger = logging.getLogger(__name__)


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
