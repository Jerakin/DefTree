import deftree


def example_in_md():
    path = ""

    tree = deftree.parse(path)
    root = tree.get_root()

    for child in root:
        print(child.name)

    for child in root.iter_all():
        print(child.name)

    for child in root.iter_elements():
        if child.name == "position":
            child.get("x").value += 10.0


def create_fish_document():
    tree = deftree.DefTree()
    root = tree.get_root()
    fish = deftree.SubElement(root, "fish")
    tuna = deftree.SubElement(fish, "tuna")
    scales = deftree.Attribute(fish, "scales", True)
    fish_copy = fish.copy()
    root.append(fish_copy)
    deftree.dump(tree)

