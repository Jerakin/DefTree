#######
DefTree
#######

.. image:: https://travis-ci.org/Jerakin/DefTree.svg?branch=master
    :target: https://travis-ci.org/Jerakin/DefTree

.. image:: https://img.shields.io/github/release/jerakin/deftree.svg
    :target: https://github.com/jerakin/deftree/releases

DefTree is a python module for modifying `Defold <https://www.defold.com>`_ documents.


Install
=======

.. code:: bash

    pip install deftree

Dependencies
============

You need to install the backport of the standard library typing module if you are running Python versions older than 3.5

.. code::  bash

    pip install typing

Example Usage
=============

Changing an atlas extrude border setting

.. code:: python

    import deftree
    tree = deftree.parse(path)                  # parse the document into a DefTree
    root = tree.get_root()                      # returns the root from the tree
    root.set_attribute("extrude_borders", 2)    # sets the attribute "extrude_boarders" to 2
    tree.write()                                # writes the file to the parsed files path

API
===

You can find the `API <https://deftree.readthedocs.io/en/latest/api.html#>`_ on `readthedocs <https://deftree.readthedocs.io/>`_.


Contributing
============

Please take a look at the `contributing <https://deftree.readthedocs.io/en/latest/contributing.html>`_ guidelines if you're interested in helping!


More information
================

Around the web, the initial post on `forum.defold.com <https://forum.defold.com/t/python-module-for-creating-pipeline-workflow-scripts/15210>`_, the package on `PyPi <https://pypi.python.org/pypi/deftree>`_ and of course the repo on
`github <https://github.com/Jerakin/DefTree>`_.
