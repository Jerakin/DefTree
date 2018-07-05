------------------------------------------------------------------------------------------
`2.1.3 <https://github.com/Jerakin/DefTree/compare/release/2.1.1...release/2.1.3>`_
------------------------------------------------------------------------------------------

Changed
=====
- `#6 <https://github.com/Jerakin/DefTree/issues/6>`_ Science annotation are now serialized properly

------------------------------------------------------------------------------------------
`2.1.1 <https://github.com/Jerakin/DefTree/compare/release/2.1.0...release/2.1.1>`_
------------------------------------------------------------------------------------------

Added
=====
- Added split and rsplit for DefTreeString
- Added \_\_contains__ for DefTreeString
- `#5 <https://github.com/Jerakin/DefTree/issues/5>`_ Added type hints for arguments

------------------------------------------------------------------------------------------
`2.1.0 <https://github.com/Jerakin/DefTree/compare/release/2.0.0...release/2.1.0>`_
------------------------------------------------------------------------------------------

Added
=====
- Added type hints for return types, helps IDEs with autocomplete

Changed
=======
- DefTree.write() argument file_path is now optional, uses the parsers file path as default

------------------------------------------------------------------------------------------
`2.0.0 <https://github.com/Jerakin/DefTree/compare/release/1.1.1...release/2.0.0>`_
------------------------------------------------------------------------------------------

Added
=====
- Added the following functions for the DefTreeString implementation: endswith, startswith, strip, rstrip, count, index, rindex, replace
- Added Attribute implementation for len()

Changed
=======
- repr() for Elements and Attributes now returns a proper formatted representations of the object
- \_\_str\_\_ on Attributes removed, now defaults back to repr()
- uses python standard library copy for getting a copy of a elements

Removed
=======
- Removed Element._set_attribute_name(), name of attributes should be changed with Attribute.name

....

------------------------------------------------------------------------------------------
`1.1.1 <https://github.com/Jerakin/DefTree/compare/release/1.1.0...release/1.1.1>`_
------------------------------------------------------------------------------------------

Changed
=======
- Fixed a bug where a negative number would be evaluated as a string

....

------------------------------------------------------------------------------------------
`1.1.0 <https://github.com/Jerakin/DefTree/compare/release/1.0.2...release/1.1.0>`_
------------------------------------------------------------------------------------------
Added
=====
- Added Element.iter_attributes to iterate over the elements and its children's elements attributes

Changed
=======
- Only imports re.compile from re instead of the whole of re
- The string value of an attribute can now be get with Attribute.string
- The Attribute.value and the value Attribute() returns should be the same
- Now reports the python value when calling the __str__ method instead of the defold value
- is_element and is_attribute are no longer flagged as internal
- improved type checking when setting attribute values

....

------------------------------------------------------------------------------------------
`1.0.2 <https://github.com/Jerakin/DefTree/compare/release/1.0.1...release/1.0.2>`_
------------------------------------------------------------------------------------------
Changed
=======
- How DefTree determines if a string is a string, int or float. Fix for bigger numbers with science annotation

....

------------------------------------------------------------------------------------------
`1.0.1 <https://github.com/Jerakin/DefTree/compare/release/0.2.0...release/1.0.1>`_
------------------------------------------------------------------------------------------
Added
=====
- Added Element.add_element(name)
- Added Element.add_attribute(name, value)
- Added Element.set_attribute(name, value)
- Added Element.elements() - for getting top level elements of Element
- Added Element.attribute() - for getting top level attribute of Element
- Exposed deftree.dump and deftree.validate in the documentation
- Added DefTree.get_document_path() to get the path of the document that was parsed
- Attribute are now sub classed into different types this to make it easier when editing values as Defold is picky

Changed
=======
- Element.iter_all() is now Element.iter()
- Element.iter_find_elements(name) is now Element.iter_elements(name)
- Changed how attributes reports their value. They should now be easier to work with, without any need add quotationmarks and such.

Removed
=======
- Removed SubElement() factory, now use element.add_element()
- Removed Element.iter_attributes()
- Removed Element.iter_find_attributes()
- Removed NaiveDefParser as it was obsolete and inferior
- Removed Example folder

....

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
- Elements \_\_setitem__ raises exception on invalid types
- Elements \_\_next__ implementation was broken
- serialize() is now a class method

....


-------------------------------------------------------------------------------------------------------------------
`0.1.0 <https://github.com/Jerakin/DefTree/compare/52db00b03bb3990c06843f3a58f24fce13b8fe74...release/0.1.0>`_
-------------------------------------------------------------------------------------------------------------------

Added
=====
- First release of DefTree