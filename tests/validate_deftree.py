import os
import timeit
import deftree

root_path = os.path.join(os.path.dirname(__file__), "data")


def validate_project(project):
    acceptable_formats = ["go", "collections", "gui", "atlas", "material", "tilemap", "spinescene", "texture_profile",
                          "render", "font", "animationset", "cubemap", "collectionfactory", "factory",
                          "collectionproxy", "collisionobject", "label", "inputbinding", "model", "particlefx", "sound",
                          "spinemodel", "sprite", "tilesource"]

    print("Starting Validation of project")
    for path_root, folders, files in os.walk(project):
        for f in files:
            if "{0}build{0}".format(os.sep) not in path_root and os.path.splitext(f)[-1][1:] in acceptable_formats:
                defold_file = os.path.join(path_root, f)
                tree = deftree.parse(defold_file)
                root = tree.get_root()
                if not deftree.validate(deftree.to_string(root), defold_file):
                    print("Error in: {}".format(defold_file))

    print("Validation of project ended")


def timing():
    times = 100
    value = timeit.timeit(
        stmt="deftree.parse('{}')".format(os.path.join(root_path, 'embedded.defold')),
        setup="import deftree; import os", number=times)

    print(value/times)

validate_project(root_path)
timing()
