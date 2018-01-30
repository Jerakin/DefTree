"""
This (crude) example checks which atlases, layers and fonts are in use in all gui files. If they are not used it removes them.
This works on the project I am working on because we don't use gui.set_texture

"""

import os
import deftree


def gui_clean_up(project_folder):
    def resource_used_in_scene(root, resource):
        used_resource = list()
        for x in root.iter_find_elements("nodes"):
            if not x:
                continue
            texture = x.get_attribute(resource)
            if texture:
                atlas = texture.value.replace('"', "").split("/")[0]
                if atlas and atlas not in used_resource:
                    used_resource.append(atlas)
        return used_resource

    file_list = list()
    for root, folders, files in os.walk(project_folder):
        [file_list.append(os.path.join(root, x)) for x in files if ".gui" in x[-4:]]

    for f in file_list:
        tree = deftree.DefTree()
        root = tree.parse(f)

        atlas_in_use = resource_used_in_scene(root, "texture")
        layers_in_use = resource_used_in_scene(root, "layer")
        fonts_in_use = resource_used_in_scene(root, "font")

        # CLEAN UP TEXTURES
        for x in root.iter_find_elements("textures"):
            if not x:
                continue

            name_attr = x.get_attribute("name")

            if name_attr:
                name = name_attr.value.replace('"', "")
                if name not in atlas_in_use:
                    root.remove(x)
                    print("Removed atlas {} in {}".format(name, f))
                    tree.write(f)

        # CLEAN UP LAYERS
        for x in root.iter_find_elements("layers"):
            if not x:
                continue

            layers_attr = x.get_attribute("name")
            if layers_attr:
                name = layers_attr.value.replace('"', "")
                if name not in layers_in_use:
                    root.remove(x)
                    print("Removed layer {} in {}".format(name, f))
                    tree.write(f)

        # CLEAN UP FONTS
        for x in root.iter_find_elements("fonts"):
            if not x:
                continue

            layers_attr = x.get_attribute("name")
            if layers_attr:
                name = layers_attr.value.replace('"', "")
                if name not in fonts_in_use:
                    root.remove(x)
                    print("Removed font {} in {}".format(name, f))
                    tree.write(f)
