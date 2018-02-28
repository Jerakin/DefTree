Design
======
Here I would like to go over some important implementation details that can help when working with DefTree.


Defold Value vs Python Value
****************************

To simplify working with attributes I decided to split how the value looks for defold and how it looks for python.
Not only does it simply working with attributes it also enables us to do some sanity checking to ensure that we do not set a value that was an int to a float, because that would make the file corrupt for the Defold editor.

Defold always encloses a string within two quotes like "/main/defold.png", but to make it easier for us to work with it deftree reports this as /main/defold.png, without the quotes. For example let say we have a file that looks like this:

.. code:: json

  nodes {
    id: "sprite"
    blend_mode: BLEND_MODE_ALPHA
    inherit_alpha: true
  }

This makes the user able to do this

.. code:: python

    tree = root.parse(my_atlas)
    root.get_root()

    for ele in root.get_element("nodes"):
        node_id = ele.get_attribute("id")
        alpha = ele.get_attribute("inherit_alpha")
        if node_id == "sprite" and alpha:
            ...

instead of this

.. code:: python

    tree = root.parse(my_atlas)
    root.get_root()

    for ele in root.get_element("nodes"):
        node_id= ele.get_attribute("id")
        alpha = ele.get_attribute("inherit_alpha")
        if node_id== '"sprite"' and alpha == "true":
            ...

which is a lot more readable and I think not as error prone.

Attribute types
---------------
The attributes type is decided on creation, it is decided in the following order:

If the value is of type(bool) or a string equal to "true" or "false" it is bool.

If the value is only capital letters and underscore (regex'd against :code:`[A-Z_]+`) it is a enum .

If the value is of type(float) or it looks like a float (regex'd against :code:`\d+\.\d+[eE-]+\d+|\d+\.\d+`) it is a float

If the value is of type(int) or can be converted with int() it is a int

Else it is a string.

