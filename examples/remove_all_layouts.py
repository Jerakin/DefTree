"""
Example of how to remove all layers in a project
"""

import deftree
import os


def is_gui(f):
    if f.endswith(".gui"):
        return True


def get_gui_scenes(p_root):
    for root, folders, files in os.walk(p_root):
        for f in files:
            path = os.path.join(root, f)
            if is_gui(path):
                yield path


def main(project):
    errors = list()
    for gui in get_gui_scenes(project):
        # Create our tree
        tree = deftree.parse(gui)
        root = tree.get_root()
        rem = False

        # Find all layouts
        for layout in root.iter_find_elements("layouts"):
            # For error reporting
            errors.append("{}".format(gui))

            rem = True

            # Remove the child layout from the root
            root.remove(layout)

        # If we removed a layout rewrite the file
        if rem:
            tree.write(gui)

    # Report our errors
    if errors:
        [print(x) for x in errors]
