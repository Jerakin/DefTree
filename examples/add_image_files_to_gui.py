import os
import hashlib
import deftree

project_root = ""
gui_file = os.path.join(project_root, "main/textures.gui")
texture_folder = os.path.join(project_root, "assets/textures/heroes")


def add_image(parent, texture_path):
    # The image need a unique name, this script was written for forcing Defold to compress single images that was
    # included as resources, we are not going to refer to them again. Thus they will not increase our memory consumption
    # if we add it to a collection proxy that is never loaded.
    name = hashlib.sha1(texture_path.encode('utf-8')).hexdigest()[:5]

    # Create a new sub element
    t = deftree.SubElement(parent, "textures")

    # Add the attributes that we need for a texture entry
    deftree.Attribute(t, "name", name)
    deftree.Attribute(t, "texture", texture_path.replace(project_root, ""))


def main():
    # Create a empty tree
    tree = deftree.DefTree()

    # Get the trees root
    root = tree.get_root()

    # Iterate all images and filter out the once we want
    for folder_root, folders, files in os.walk(texture_folder):
        for image in files:
            if image.endswith("png"):
                full_path = os.path.join(folder_root, image)
                add_image(root, full_path)

    # Add the last attributes that we need for a gui file, remember that script is a string and thus needs enclosing "
    deftree.Attribute(root, "script", '""')
    deftree.Attribute(root, "adjust_reference", "ADJUST_REFERENCE_PARENT")

    # Write the tree to disk
    tree.write(gui_file)

if __name__ == '__main__':
    main()
