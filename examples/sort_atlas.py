"""
Sorts images in all atlases in a project
"""


import os
import deftree


def sort_atlas(atlas):
    tree = deftree.parse(atlas)
    root = tree.get_root()
    new_tree = deftree.DefTree()
    new_root = new_tree.get_root()
    _atlas = []

    for at in root.iter_elements():
        _atlas.append(at.get_attribute("image").value)

    for a in sorted(_atlas, key=lambda x: x.split("/")[-1]):
        ele = deftree.SubElement(new_root, "images")
        deftree.Attribute(ele, "image", a)

    for at in root.iter_attributes():
        if not at.name == "image":
            new_root.add(at)

    new_tree.write(atlas)


def main(project):
    for f_root, folders, files in os.walk(os.path.join(project), "atlases"):
        for f in files:
            if ".atlas" in f:
                sort_atlas(os.path.join(f_root, f))
