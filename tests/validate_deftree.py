import os
import timeit
import deftree

root_path = os.path.join(os.path.dirname(__file__), "data")


def validate_project(project):
    acceptable_formats = ["go", "collections", "gui", "atlas", "material", "tilemap", "spinescene", "texture_profile",
                          "render", "font", "animationset", "cubemap", "collectionfactory", "factory",
                          "collectionproxy", "collisionobject", "label", "inputbinding", "model", "particlefx", "sound",
                          "spinemodel", "sprite", "tilesource"]

    acceptable_formats.extend(["defold"])
    print("Starting Validation of project")
    for path_root, folders, files in os.walk(project):
        for f in files:
            if "{0}build{0}".format(os.sep) not in path_root and os.path.splitext(f)[-1][1:] in acceptable_formats:
                print("Validating", f)
                defold_file = os.path.join(path_root, f)
                try:
                    tree = deftree.parse(defold_file)
                    root = tree.get_root()
                except deftree.ParseError:
                    print("  Couldn't parse: ", f)
                    continue
                if not deftree.validate(deftree.to_string(root), defold_file):
                    print("  Error in: {}".format(defold_file))

    print("Validation of project ended")


validate_project(root_path)

