.. DefTree documentation master file, created by
   sphinx-quickstart on Sun Oct  2 12:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   api
   using
   design
   contributing
   changelog_link

DefTree |version|
=================
DefTree is a python module for modifying Defold_ documents. The first implementation was inspired by the xml.ElementTree library.

.. _Defold: http://www.defold.com/

DefTree reads any Defold document into an object tree hierarchy and follow the these three main concepts

1. DefTree represents the complete Defold document as a tree.

2. Element represents a single node or block in this tree.

3. Attribute represent a name value pair.


Installation
************

.. note::  DefTree is only supported by python >= 3.3.0

DefTree is a native python implementation and thus should work under the most common platforms that supports python.
The package is distributed in the wheel format and is easily installed with pip.

.. code:: bash

    pip install deftree


You need to install the backport of the standard library typing module if you are running Python versions older than 3.5

.. code::  bash

    pip install typing

Old Versions
************
Old distributions may be accessed via PyPI_.

.. _PyPi: https://pypi.python.org/pypi/deftree
