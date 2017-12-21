Releasing
=========
Written for the authors bad memory

Run unittests
*************

.. code:: bash

    python -m unittest discover tests


Docs
****
Install dependencies

.. code:: bash

    pip install Sphinx

Build and verify documentation

.. code:: bash

    doc/make hml


PyPi
****

Install dependencies

.. code:: bash

    pip install twine
    pip install wheel

Build the wheel

.. code:: bash

    python setup.py bdist_wheel

Upload to PyPi

.. code:: bash

    twine upload dist/*