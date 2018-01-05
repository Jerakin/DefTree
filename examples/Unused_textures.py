# This example assumes that you are not using resource.set_texture()
# Warning, this example assumes that all your images are in gui, this example should not be ran on your project.

import os
import deftree


def is_image(path):
    if path.endswith(".png") and "{0}build{0}".format(os.sep) not in path:
        return True


def get_images_in_projects(project):
    for root, folders, files in os.walk(project):
        for f in files:
            path = os.path.join(root, f)
            if is_image(path):
                yield path


def get_atlas_files(project_folder):
    """Get all atlas files in a given project"""
    return [os.path.join(root, x) for root, folders, files in os.walk(project_folder) for x in files if ".atlas" in x]


def get_images_in_atlas(path):
    """get all images paths in a given path"""
    tree = deftree.DefTree()
    root = tree.parse(path)
    for x in root.iter_find_attributes("image"):
        yield x.value.replace('"', "")


def clean_up_atlas(project_root, atlas):
    """Remove all missing image in entries in the atlas"""
    for missing in missing_images_in_atlas(project_root, atlas):
        tree = deftree.DefTree()
        root = tree.parse(atlas)
        for attribute in root.iter_find_attributes("image", '"{}"'.format(missing)):
            print("Removed: {}".format(missing))
            root.remove(attribute.get_parent())
        tree.write(atlas)


def missing_images_in_atlas(project_root, atlas):
    """get images in an atlas that does not exist on disk"""
    tree = deftree.DefTree()
    root = tree.parse(atlas)
    for image in get_images_in_atlas(root):
        if not os.path.exists(os.path.join(project_root, image[1:])):
            yield image


def run_on_project(project):

    # Find all images in all atlases
    images_in_atlases = []
    for atlas in get_atlas_files(project):
        for img in get_images_in_atlas(atlas):
            images_in_atlases.append(os.path.join(project, img[1:]))

    # Find all images in the project and compare them to what are in the atlases
    for project_image in get_images_in_projects(project):
        if project_image not in images_in_atlases:
            # Do something to the images
            print(project_image)

run_on_project("/Users/mattias.hedberg/Documents/repo/defold_projects/gui_scene")
