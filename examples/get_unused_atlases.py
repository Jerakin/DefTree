import deftree


def get_atlas_in_gui(file_path):
    tree = deftree.DefTree()
    root = tree.parse(file_path)

    # Find all texture entries
    texture_elements = root.iter_find_elements("textures")

    # Add all texture entires to a list
    atlas_used = list()
    for texture in texture_elements:
        atlas_used.append([texture.get_attribute("name").value, texture.get_attribute("texture").value])
    return atlas_used


def get_unused_atlas_in_gui(file_path):
    tree = deftree.DefTree()
    root = tree.parse(file_path)

    atlases = get_atlas_in_gui(file_path)

    # Clean up texture entries names
    atlases = [[x[0].replace('"', ""), x[1]] for x in atlases]

    # Find all Box nodes
    box_nodes = [x.get_parent() for x in root.iter_find_attributes("type", "TYPE_BOX")]

    # Add all box nodes textures to a list
    atlas_used = list()
    for box in box_nodes:
        texture = box.get_attribute("texture").value
        if texture:
            atlas_name = texture.split("/")[0].replace('"', "")
            atlas_used.append(atlas_name)

    # Compare our two lists
    for x in set(atlas_used):
        for y in atlases:
            if x == y[0]:
                atlases.remove(y)
    return atlases
