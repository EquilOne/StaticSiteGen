import os
import shutil


def copy_files(
    src_dir: str, dst_dir: str, create_dst: bool = False, root_dir: str | None = None
):
    if root_dir is None:
        root_dir = os.getcwd()
        print(f"Root directory not specified, using {root_dir}")
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Root directory {root_dir} does not exist")
    if not os.path.isdir(root_dir):
        raise NotADirectoryError(f"Root directory {root_dir} is not a directory")

    src_dir_path = os.path.join(root_dir, src_dir)
    if not os.path.exists(src_dir_path):
        raise FileNotFoundError(f"Source directory {src_dir} does not exist")
    if not os.path.isdir(src_dir_path):
        raise NotADirectoryError(f"Source directory {src_dir} is not a directory")

    dst_dir_path = os.path.join(root_dir, dst_dir)
    if os.path.exists(dst_dir_path):
        print(
            f"Destination directory {dst_dir_path} already exists, performing cleanup."
        )
        shutil.rmtree(dst_dir_path)
        print(f"Cleanup complete, {dst_dir_path} removed.")
        print(f"Creating directory '{dst_dir}' in {root_dir}")
    os.mkdir(dst_dir_path)

    src_dir_contents = os.listdir(src_dir_path)
    for item in src_dir_contents:
        item_path = os.path.join(src_dir_path, item)
        if os.path.isdir(item_path):
            print(f"Creating directory '{item}' in {dst_dir_path}")
            copy_files(item_path, os.path.join(dst_dir_path, item), True, item_path)
        else:
            print(f"Copying {item} to {dst_dir_path}")
            shutil.copy(item_path, dst_dir_path)


def main():
    # text_node = TextNode("Test text", TextType.BOLD, "https://www.google.com")
    # leaf_node = LeafNode("a", "link", {"href": "afakelink.com"})
    # html_node = HTMLNode("p", "HTML node", [leaf_node])
    # html_code_node = markdown_to_html_node(
    #     "```\nPretend this is actually a code block.```"
    # )
    # print(text_node.__repr__())
    # print(leaf_node.__repr__())
    # print(html_node.__repr__())
    # print(html_code_node.__repr__())

    try:
        copy_files("static", "public", True)
    except FileNotFoundError as e:
        print(e)
    except NotADirectoryError as e:
        print(e)


main()
