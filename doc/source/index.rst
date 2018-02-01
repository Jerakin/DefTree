.. DefTree documentation master file, created by
   sphinx-quickstart on Sun Oct  2 12:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   api
   using
   changelog_link
   contributing

DefTree
=======
DefTree is a python module modify Defold_ documents, it is inspired by the xml.ElementTree library.

.. _Defold: http://www.defold.com/

It reads any defold document into a object tree hierarchy, the module
have three main concepts

1. DefTree represents the whole Defold document as a tree and

2. Element represents a single node or block in this tree and

3. Attribute represent a name value pair


Installation
************

.. note::  DefTree is only supported by python >= 3.3.0

DefTree is a native python implementation and thus should work under the most common platforms that supports python.
The package is distributed in the wheel format

.. code:: bash

    pip install deftree


Old Versions
************
You can download old distributions from PyPI_.

.. _PyPi: https://pypi.python.org/pypi/deftree