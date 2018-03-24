Written for the authors bad memory

Docs
****

Install sphinx and the read the docs theme

.. code:: bash

    pip install Sphinx

    pip install sphinx_rtd_theme


Build and verify documentation

.. code:: bash

    cd doc
    make html


    
Run unittests
*************

Install coverage

.. code:: bash

    pip install coverage


Run unittests with coverage

.. code:: bash

    coverage run --omit=tests/test_deftree.py -m unittest discover -s tests/
    coverage report

    

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
    
    
Git
***

* Tag the release with "release/x.x.x"
* Update the __version__ in deftree.py
* Update CHANGELOG.rst
* Push to repository
* Build documentation on deftree.readthedocs.io

Step by step
************

* Update version in deftree.py
* Update CHANGELOG.rst
* Do a commit
* Tag the release with "release/x.x.x"
* Push commit
* Push tag
* Build wheel
* Upload wheel
* Build documentation
* Create a git release