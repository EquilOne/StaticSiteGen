import logging
import os
from pathlib import Path

from src.blocks import extract_title
from src.convert import markdown_to_html_node

logger = logging.getLogger(__name__)


def generate_page(src_file, tmpl_file, dst_path, basepath="/"):
    logger.info("Generating page in %s from %s with %s", dst_path, src_file, tmpl_file)

    if not os.path.exists(src_file):
        logger.error("Source file '%s' does not exist", os.path.abspath(src_file))
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
            contents = (
                tmpl_contents.replace("{{ Title }}", page_title)
                .replace("{{ Content }}", src_html_str)
                .replace('href="/', f'href="{basepath}')
                .replace('src="/', f'src="{basepath}')
            )
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

            stem = Path(src_file).stem
            out_dir = dst_path if stem == "index" else os.path.join(dst_path, stem)
            os.makedirs(out_dir, exist_ok=True)
            with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(contents)


def generate_pages_recursive(src_dir, tmpl_file, dst_dir, basepath="/"):
    src_dir_contents = sorted(os.listdir(src_dir))
    for item in src_dir_contents:
        item_path = os.path.abspath(os.path.join(src_dir, item))
        if os.path.isfile(item_path) and Path(item).suffix.lower() == ".md":
            generate_page(item_path, tmpl_file, dst_dir, basepath)

        elif os.path.isdir(item_path):
            generate_pages_recursive(
                item_path, tmpl_file, os.path.join(dst_dir, item), basepath
            )
        else:
            logger.debug("%s is not a directory or markdown file", item_path)
