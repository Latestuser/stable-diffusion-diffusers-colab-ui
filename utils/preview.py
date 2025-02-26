import os
import shutil
from ipywidgets import Image, HBox, VBox, Button, Layout
from IPython.display import display, FileLink
from typing import List

def get_image_previews(paths: List[str], width: int, height: int,
                       favourite_dir: str = "outputs/favourite") -> HBox:
    """Creates a widget preview for every image in paths"""
    wgts = []
    for filepath in paths:
        preview = Image(
            value=open(filepath, "rb").read(),
            width=width,
            height=height,
        )
        btn = _add_favourite_button(filepath, favourite_dir)
        download_btn = _add_download_button(filepath)  # 新增下载按钮
        wgt = VBox([preview, btn, download_btn])
        wgts.append(wgt)

    return HBox(wgts)

def copy_file(file_path: str, to_path: str):
    """Copy file at `file_path` to `to_path` directory"""
    try_create_dir(to_path)
    filename = os.path.basename(file_path)
    shutil.copyfile(file_path, os.path.join(to_path, filename))

def try_create_dir(path: str):
    """Create folder at `path` if it doesn't already exist"""
    try:
        os.makedirs(path)
    except FileExistsError: pass

def _add_favourite_button(filepath: str, to_dir:str) -> Button:
    btn = Button(description="Favourite", tooltip=filepath, layout=Layout(width="99%"))
    def btn_handler(b):
        copy_file(filepath, to_dir)
    btn.on_click(btn_handler)
    return btn

def _add_download_button(filepath: str) -> Button:
    btn = Button(description="Download", tooltip=filepath, layout=Layout(width="99%"))
    def btn_handler(b):
        # 使用 FileLink 创建下载链接并显示
        link = FileLink(filepath, result_html_prefix="Click to download: ")
        display(link)
    btn.on_click(btn_handler)
    return btn
