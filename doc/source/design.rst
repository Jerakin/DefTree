:tocdepth: 1

Design
======
Here I would like to go over some important details concerning implementation that may help when working with DefTree.

Defold Value vs Python Value
****************************

To simplify working with attributes I decided to split how the value looks for Defold and how it looks for python.
Not only does this simplify working with attributes it also enables us to do some sanity checking to ensure that we do not set a value that was an int to a float because this would make the file corrupt for the Defold editor.

Defold will always enclose a string within two quotes like "/main/defold.png". To make it easier for us to work with it DefTree reports this as /main/defold.png, i.e. without the quotes. As an example, let us assume we have a file that looks as follows:

.. code:: json

  nodes {
    id: "sprite"
    blend_mode: BLEND_MODE_ALPHA
    inherit_alpha: true
  }

This enables the user to do this:

.. code:: python

    tree = root.parse(my_atlas)
    root.get_root()

    for ele in root.get_element("nodes"):
        node_id = ele.get_attribute("id")
        alpha = ele.get_attribute("inherit_alpha")
        if node_id == "sprite" and alpha:
            ...

in contrast to:

.. code:: python

    tree = root.parse(my_atlas)
    root.get_root()

    for ele in root.get_element("nodes"):
        node_id= ele.get_attribute("id")
        alpha = ele.get_attribute("inherit_alpha")
        if node_id == "/"sprite/"" and alpha == "true":  # or '"sprite"'
            ...

The former is a lot more readable and not as error prone, as I see it.

Attribute types
---------------
The attribute's type is decided on creation and follow the logic below:

If the value is of type(bool) or a string equal to "true" or "false" it is considered a bool.

If the value consists of only capital letters and underscore (regex'd against :code:`[A-Z_]+`) it is considered an enum.

If the value is of type(float) or it looks like a float (regex'd against :code:`[-\d]+\.\d+[eE-]+\d+|[-\d]+\.\d+`) it is considered a float.

If the value is of type(int) or can be converted with int() it is considered an int.

Else it is considered a string.
