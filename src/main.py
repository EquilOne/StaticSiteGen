import os
import shutil
import sys

from src.constant import DST_DIR, SRC_DIR


def _copy_files(
    src_path: str | os.PathLike[str], dst_path: str | os.PathLike[str]
) -> None:
    """Recursively copy the contents of src_path into dst_path.

    dst_path must not exist; the caller validates src and cleans dst first.
    Skips symlinks."""

    print(f"Creating directory '{os.path.basename(dst_path)}' in '{dst_path}'")
    os.mkdir(dst_path)

    src_dir_contents = os.listdir(src_path)
    for item in src_dir_contents:
        item_path = os.path.join(src_path, item)
        if os.path.islink(item_path):
            continue
        if os.path.isdir(item_path):
            _copy_files(item_path, os.path.join(dst_path, item))
        else:
            print(f"Copying {item} to {dst_path}")
            shutil.copy2(item_path, dst_path)


def main() -> None:

    try:
        if not os.path.exists(SRC_DIR):
            raise FileNotFoundError(f"Source directory {SRC_DIR.name} does not exist")
        if not os.path.isdir(SRC_DIR):
            raise NotADirectoryError(f"Source directory {SRC_DIR.name} is not a directory")
        if os.path.isdir(DST_DIR):
            print(f"Directory '{DST_DIR.name}' already exists, performing cleanup.")
            shutil.rmtree(DST_DIR)
            print("Cleanup complete")
        _copy_files(SRC_DIR, DST_DIR)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
