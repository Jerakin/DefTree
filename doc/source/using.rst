Using DefTree
=============
If you are not familiar with Defold files this is how the syntax looks, it is in a `Google Protobuf`_ format.

.. code:: javascript

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


Parsing Defold Documents
************************

Parsing from a file is done by calling the parse method

.. code:: python

    import deftree
    tree = deftree.parse(path)  # parse the document into a DefTree
    root = tree.get_root()      # returns the root from the tree

Or alternatively we can first create a DefTree instance

.. code:: python

    tree = deftree.Deftree()
    root = tree.parse(path)

We can also parse a document from a string

.. code:: python

    tree = deftree.from_string(document_as_string)  # parse the document into a DefTree
    root = tree.get_root()      # returns the root from the tree

Finding interesting elements
****************************

Element has some useful methods that help iterate recursively over all
the sub-tree below it (its children, their children, and so on). For
example, Element.iter():

.. code:: python

    for child in root.iter():
        print(child.name)

We can also iterate only elements by calling Element.iter_elements()

.. code:: python

    for child in root.iter_elements():
        print(child.name)

    for child in root.iter_elements("nodes"):  # iter_elements also supports filtering on name
        print(child.name)

Element.get_attribute() finds the first attributes with the given name
in that element.

.. code:: python

    attribute = element.get_attribute("id")


Modifying existing scenes
*************************

DefTree provides a simple way to edit Defold documents and write them
to files. The DefTree.write() method serves this purpose. Once created,
an Element object may be manipulated by directly changing its fields,
as well as adding new children (for example with Element.insert()).

Let's say we want to find all box nodes in a gui and change its layers.

.. code:: python

    for element in root.iter_elements("nodes")
        if element.get_attribute("type") == "TYPE_BOX":
            element.set_attribute("layer", 'new_layer')

We can also add new attributes and elements all together.

.. code:: python

    new_element = root.add_element("layers")
    new_element.add_attribute("name", 'new_layer')

DefTree Attribute of number types supports basic math functions directly

.. code:: python

    new_element = root.get_element("position")
    attribute = new_element.get_attribute("x")
    attribute += 10

We will probably then overwrite the file

.. code:: python

    tree.write(tree.get_document_path())

.. _Google Protobuf: https://developers.google.com/protocol-buffers/