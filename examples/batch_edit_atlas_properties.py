"""
Batch changes all atlases in the project

"""


import os
import deftree


def set_atlas_extrude(project_folder, value):
    for f_root, folders, files in os.walk(os.path.join(project_folder, "atlases")):
        for f in files:
            if ".atlas" in f:
                tree = deftree.parse(os.path.join(f_root, f))
                root = tree.get_root()
                extrude = root.get_attribute("extrude_borders")

                extrude.value = value
                tree.write(os.path.join(f_root, f))
