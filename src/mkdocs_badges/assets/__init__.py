import os
import shutil

def get_resource_path(name: str) -> str:
    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, name)


BADGE_CSS = get_resource_path("badge.css")
BADGE_JS = get_resource_path("badge.js")
INSTALL_BADGE_DATA = get_resource_path("install_badge_data.json")


def copy_asset_if_target_file_does_not_exist(output_dir: str, target_path_in_output_folder: str, asset_name: str):
    if not target_path_in_output_folder:
        raise ValueError("Empty value for 'target_path_in_output_folder' given")

    target_path = os.path.join(output_dir, target_path_in_output_folder)
    if os.path.exists(target_path):
        # The file exists. This probably means, that the user wanted to override the default file
        # So we just do nothing
        pass
    else:
        # Make sure that the folder exists
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        # Copy the file
        asset_path = get_resource_path(asset_name)
        shutil.copyfile(asset_path, target_path)
