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
        tree = deftree.parse(gui)
        root = tree.get_root()
        rem = False
        for layout in root.iter_find_elements("layouts"):
            errors.append("{}".format(gui))
            rem = True
            root.remove(layout)

        if rem:
            tree.write(gui)

    if errors:
        [print(x) for x in errors]
