from deftree import *
import os

# Name of layer is resource basename
# Add Text layers last

# TYPE_BOX
# TYPE_TEXT
# TYPE_TEMPLATE
# TYPE_PIE
# TYPE_SPINE


def add_box_layer(node, empty="empty"):
    layer_name = node.get_attribute("texture").value.strip('"').split("/")[0]
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '"{}"'.format(layer_name)
    return layer_name


def add_text_layer(node, empty="empty"):
    layer_name = node.get_attribute("font").value
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '{}'.format(layer_name)
    return layer_name.strip('"')


def add_template_layer(node, empty="empty"):
    layer_name = node.get_attribute()
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '"{}"'.format(layer_name)
    return ""


def add_pie_layer(node, empty="empty"):
    layer_name = node.get_attribute("texture").value.strip('"').split("/")[0]
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '"{}"'.format(layer_name)
    return layer_name


def add_spine_layer(node, empty="empty"):
    layer_name = node.get_attribute("spine_scene").value
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '{}'.format(layer_name)
    return layer_name.strip('"')


def add_particle_layer(node, empty="empty"):
    layer_name = node.get_attribute("particlefx").value
    if not layer_name:
        layer_name = empty
    node.get_attribute("layer").value = '{}'.format(layer_name)
    return layer_name.strip('"')


def _add_layer(scene_root, layer):
    if not layer:
        return
    for l in scene_root.iter_find_elements("layers"):
        if layer in l.get_attribute("name").value:
            return
    ele = SubElement(scene_root, "layers")
    Attribute(ele, "name", '"{}"'.format(layer))


def add_layers_to_gui(scene_root, layers):
    for layer in set(layers["TYPE_BOX"]):
        _add_layer(scene_root, layer)
    
    for layer in set(layers["TYPE_SPINE"]):
        _add_layer(scene_root, layer)
    
    for layer in set(layers["TYPE_TEMPLATE"]):
        _add_layer(scene_root, layer)
    
    for layer in set(layers["TYPE_PIE"]):
        _add_layer(scene_root, layer)

    for layer in set(layers["TYPE_PARTICLEFX"]):
        _add_layer(scene_root, layer)

    for layer in set(layers["TYPE_TEXT"]):
        _add_layer(scene_root, layer)

    
def iter_nodes(element):
    for i in element.iter_find_elements("nodes"):
        node_type = i.get_attribute("type")
        yield i, node_type.value


def add_layers_in_scene(scene):
    layer_names = {"TYPE_BOX": [], "TYPE_TEXT": [], "TYPE_TEMPLATE": [], "TYPE_PIE": [], "TYPE_SPINE": [],
                   "TYPE_PARTICLEFX": []}
    layer_name = "UNRECOGNIZED TYPE"
    tree = parse(scene)
    root = tree.get_root()

    for node, n_type in iter_nodes(root):
        if n_type == "TYPE_BOX":
            layer_name = add_box_layer(node, (layer_names[n_type] and layer_names[n_type][0]) or "empty")

        elif n_type == "TYPE_TEXT":
            layer_name = add_text_layer(node, (layer_names[n_type] and layer_names[n_type][0]) or "empty")

        elif n_type == "TYPE_TEMPLATE":
            # layer_name = add_template_layer(node)
            pass

        elif n_type == "TYPE_PIE":
            layer_name = add_box_layer(node, (layer_names[n_type] and layer_names[n_type][0]) or "empty")

        elif n_type == "TYPE_SPINE":
            layer_name = add_spine_layer(node, (layer_names[n_type] and layer_names[n_type][0]) or "empty")

        elif n_type == "TYPE_PARTICLEFX":
            layer_name = add_particle_layer(node, (layer_names[n_type] and layer_names[n_type][0]) or "empty")

        layer_names[n_type].append(layer_name)
    
    add_layers_to_gui(root, layer_names)
    tree.write(tree.parser.file_path)


def is_gui(scene):
    if scene.endswith(".gui") and os.path.exists(scene):
        return scene


def create_layers_in_project(project):
    for root, folders, files in os.walk(project):
        for f in files:
            file_path = os.path.join(root, f)
            if is_gui(file_path):
                add_layers_in_scene(file_path)
