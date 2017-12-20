import deftree


def move_sprite_x_to(x_position):
    # Path to our file
    path = "file_path"

    # Parse our path into a DefTree object
    tree = deftree.parse(path)

    # get our root
    root = tree.get_root()

    # Recusivley find a attribut with the 'id: "sprite"
    attribute = root.get_attributes("id", '"sprite"')

    # If that attribute exists
    if attribute:

        # Get it's parent (gives us the sprite component)
        parent = attribute.get_parent()

        # Find the position element
        pos = parent.find("position")

        # Find the x attribute and set its value
        pos.find("x").value = x_position

    # Output the file to the same as the input
    tree.write(path)