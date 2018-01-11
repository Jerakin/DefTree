------------------------------------------------------------------------------------------
`0.2.0 <https://github.com/Jerakin/DefTree/compare/release/0.1.1...release/0.2.0>`_
------------------------------------------------------------------------------------------

Added
=====
- Raises ParseError when reading invalid documents

Changed
=======
- Updated docstrings to be easier to read.
- Refactored internal usage of a level variable to track how deep the item were in the tree

Removed
=======
- Removed Element.add(), use Element.append() Element.insert()
- Removed Element.items(), use Element.iter_all()

....

------------------------------------------------------------------------------------------
`0.1.1 <https://github.com/Jerakin/DefTree/compare/release/0.1.0...release/0.1.1>`_
------------------------------------------------------------------------------------------

Added
=====
- Licence to github repository
- Setup files for PyPi to github repository
- Example usage
- Unittesting with `unittest <https://docs.python.org/3/library/unittest.html>`_
- Coverage exclusion for usage with `Coverage.py <http://coverage.readthedocs.io/en/latest/>`_
- Using __all__ to define public api, in case of wild import

Changed
=======
- Elements __setitem__ raises exception on invalid types
- Elements __next__ implementation was broken
- serialize() is now a class method

....


-------------------------------------------------------------------------------------------------------------------
`0.1.0 <https://github.com/Jerakin/DefTree/compare/52db00b03bb3990c06843f3a58f24fce13b8fe74...release/0.1.0>`_
-------------------------------------------------------------------------------------------------------------------

Added
=====
- First release of DefTree