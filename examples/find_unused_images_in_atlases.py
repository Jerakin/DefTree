"""
"""

import os
import deftree


def get_atlas_files(project_folder):
    """Get all atlas files in a given project"""
    return [os.path.join(root, x) for root, folders, files in os.walk(project_folder) for x in files if ".atlas" in x]


def get_images(df_object):
    """get all images paths in a given DefTree Element instance"""
    for x in df_object.iter_find_attributes("image"):
        yield x.value.replace('"', "")


def missing_images_in_atlas(project_root, atlas):
    """get images in an atlas that does not exist on disk"""
    tree = deftree.DefTree()
    root = tree.parse(atlas)
    for image in get_images(root):
        if not os.path.exists(os.path.join(project_root, image[1:])):
            yield image


def clean_up_atlas(project_root, atlas):
    """Remove all missing image in entries in the atlas"""
    for missing in missing_images_in_atlas(project_root, atlas):
        tree = deftree.DefTree()
        root = tree.parse(atlas)
        for attribute in root.iter_find_attributes("image", '"{}"'.format(missing)):
            root.remove(attribute.get_parent())
        tree.write(atlas)


def verify(project_folder):
    """Print images that are missing on disk"""
    for atlas in get_atlas_files(project_folder):
        for missing in missing_images_in_atlas(project_folder, atlas):
            print("{}{}{}".format(atlas.replace(project_folder, ""),
                                  (50 - len(atlas.replace(project_folder, ""))) * " ",
                                  missing))


def clean_up_all_atlases(project_folder):
    """Remove all missing image in entries in the project"""
    for atlas in get_atlas_files(project_folder):
        clean_up_atlas(project_folder, atlas)
