import logging
import os
import shutil

from src.constant import CONTENT_DIR, DST_DIR, PROJECT_ROOT, PUBLIC_DIR, SRC_DIR
from src.files import _copy_files
from src.page import generate_pages_recursive

logger = logging.getLogger(__name__)


def main() -> None:

    logging.basicConfig(
        level=logging.INFO,
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

    # generate_page(
    #     os.path.join(PROJECT_ROOT, "content/index.md"),
    #     os.path.join(PROJECT_ROOT, "template.html"),
    #     os.path.join(PROJECT_ROOT, "public"),
    # )

    generate_pages_recursive(
        CONTENT_DIR,
        os.path.join(PROJECT_ROOT, "template.html"),
        PUBLIC_DIR,
    )


if __name__ == "__main__":
    main()
