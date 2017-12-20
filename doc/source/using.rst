Using DefTree
=============
If you are not familiar with Defold files this is how the syntax looks,
it is the Protobuf_ format.

::

    elementname {
      attributename: attributevalue
      position {
        x: 0.0
        y: 0.0
        z: 0.0
      }
      type: TYPE_BOX
      blend_mode: BLEND_MODE_ALPHA
      texture: "atlas/logo"
      id: "logo"
    }


Example 1: Parsing Defold Documents
***********************************

We can import this data by reading from a file:

.. code:: python

    import deftree
    tree = deftree.parse(path)  # parse the document into a DefTree
    root = tree.get_root()      # returns the root from the tree


Example 2: Finding interesting elements
***************************************

Element has some useful methods that help iterate recursively over all
the sub-tree below it (its children, their children, and so on). For
example, Element.iter_all():

.. code:: python

    for child in root.iter_all():
        print(child.name)

Element.get_attribute() finds the first attributes with the given name
in that element. This will return the attribute, which you can then get the
parent from thus finding a particular node. For example:

.. code:: python

    attribute = element.get_attribute("id", '"logo"')
    logo_node = attribute.get_parent()

Example 3: Modifying existing scenes
************************************

DefTree provides a simple way to build Defold documents and write them
to files. The DefTree.write() method serves this purpose. Once created,
an Element object may be manipulated by directly changing its fields
(such as Attribute.value), as well as adding new children (for example
with Element.append()).

Let’s say we want to add 10 to all x value in a scene

.. code:: python

    for child in root.iter_find_attributes("x"):
        child.value =+ 10.0

The SubElement() function also provides a convenient way to create new
sub-elements for a given element, adding new attributes to that is easy.

.. code:: python

    new_parent = deftree.SubElement(root, "layers")
    deftree.Attribute(new_parent, "name", '"new_layer"')

More Examples
*************

There are a lot more in depth examples in the folder examples_ of
the repository

.. _examples: https://github.com/Jerakin/DefTree/tree/master/examples
.. _Protobuf: https://developers.google.com/protocol-buffers/