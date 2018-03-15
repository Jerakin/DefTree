#!/usr/bin/env bash
cd ..
python -m coverage run --omit=tests/test_deftree.py -m unittest discover -s tests/
python -m coverage report
python -m coverage html

open htmlcov/index.html


cd doc
make html
open build/html/index.html
