import os
import deftree


def get_particles(folder):
    for root, folders, files in os.walk(folder):
        if "/build/" not in root:
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path) and ".particlefx" in file:
                    yield file_path


def scale_effect(scale, tree):
    scale_properties(scale, tree)
    for position in tree.iter_find_elements("position"):
        position.get_attribute("x").value = float(position.get_attribute("x").value) * scale
        position.get_attribute("y").value = float(position.get_attribute("y").value) * scale


def scale_properties(scale, tree):
    keys = ["EMITTER_KEY_PARTICLE_SIZE", "EMITTER_KEY_SIZE_X", "EMITTER_KEY_SIZE_Y", "EMITTER_KEY_SIZE_Z",
            "EMITTER_KEY_PARTICLE_SPEED", "MODIFIER_KEY_MAGNITUDE", "MODIFIER_KEY_MAX_DISTANCE"]
    for k in keys:
        for attribute in tree.iter_find_attributes("key", k):
            properties = attribute.get_parent()
            points = properties.get_element("points")
            points.get_attribute("x").value = float(points.get_attribute("x").value) * scale
            points.get_attribute("y").value = float(points.get_attribute("y").value) * scale
            spread = properties.get_attribute("spread")
            if spread:
                spread.value = float(spread.value) * scale


def resize(scale, path):
    root = deftree.parse(path)
    tree = root.get_root()
    scale_effect(scale, tree)
    root.write(path)


def resize_all(scale, file_path):
    for image_file in get_particles(file_path):
        resize(scale, image_file)
