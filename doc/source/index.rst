.. DefTree documentation master file, created by
   sphinx-quickstart on Sun Oct  2 12:21:40 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   api
   using


Introduction
============
DefTree is a python module modify Defold_ documents, it is inspired by the xml.ElementTree library.

.. _Defold: http://www.defold.com/

It reads any defold document into a object tree hierarchy, the module
have three main concepts

1. DefTree represents the whole Defold document as a tree and

2. Element represents a single node or block in this tree and

3. Attribute represent a name value pair


Get it
======
For now download and use deftree_ in your project as is
.. _deftree: https://github.com/Jerakin/DefTree/blob/master/deftree.py


Short comings
*************
One of the biggest short comings is that it is designed to work on any
defold file and thus is very generic, it doesn't differentiate between
different files.

If you use it on templates and similar nodes you may need to set additional
attributes, such as "overridden_fields" in GUIs.
