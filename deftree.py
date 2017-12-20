"""
 Defold files are a inherently hierarchical data format, and the most natural way to
 represent it is with a tree.  This module has three classes for this purpose:

    1. DefTree represents the whole D as a tree and

    2. Element represents a single node in this tree and

    3. Attribute represent a name value pair
"""
import re
from sys import stdout
__version__ = "0.1.0"


class BaseDefParser:
    _pattern = ''
    _regex = re.compile(_pattern)

    def __init__(self, root_element):
        self.root = root_element
        self._element_chain = [self.root]

    def parse(self, source):
        """Loads an external Defold section into this DefTree

        :param source: path to the file.
        :returns Element: root Element"""

        document = self._open(source)
        return self._parse(document)

    def from_string(self, source):
        """Parses an Defold section from a string constant

        :param source: string to parse.
        :returns Element: root Element"""

        return self._parse(source)

    def _parse(self, input_doc):
        document = input_doc
        last_index = True
        while last_index:
            last_index = self._tree_builder(document)
            if last_index:
                document = document[last_index:]
        return self.root

    def _tree_builder(self, document):
        """searches the document for a match, and builds the tree"""
        return False

    @staticmethod
    def _open(_path):
        """Return the documents data as a string"""

        with open(_path, "r") as document:
            current_document = document.read()
        return current_document

    @staticmethod
    def _to_python_objects(_input):
        def is_bool(__input):
            if __input == "false":
                return False
            elif __input == "true":
                return True
            else:
                return __input

        return is_bool(_input)

    @staticmethod
    def serialize(element):
        """Returns a string of the element"""
        return ""


class NaiveDefParser(BaseDefParser):
    _pattern = '(?:^|\s)(\w+):\s+(.+(?:\s+".*)*)|(\w*)\s{|(})'
    _regex = re.compile(_pattern)

    def __init__(self, root_element):
        super().__init__(root_element)

    def _tree_builder(self, document):
        """searches the document for a match, and builds the tree"""
        regex_match = re.search(self._pattern, document)
        if regex_match:
            element_name = regex_match.group(3)
            attribute_name, attribute_value = regex_match.group(1, 2)
            element_exit = regex_match.group(4)

            if element_name:
                last_element = self._element_chain[-1]
                name = element_name
                element = SubElement(last_element, name)
                self._element_chain.append(element)
            elif attribute_name and attribute_value:
                last_element = self._element_chain[-1]
                name = attribute_name
                value = self._to_python_objects(attribute_value)
                Attribute(last_element, name, value)
            elif element_exit:
                self._element_chain.pop()

            return regex_match.end()
        return False

    @staticmethod
    def serialize(element):
        """Returns a string of the element"""
        _assert_is_element(element)

        def __from_python_object(_input):
            def is_bool(__input):
                if __input is False:
                    return "false"
                elif __input is True:
                    return "true"
                else:
                    return __input

            return is_bool(_input)

        def construct_string(node):
            """Recursive function that formats the text"""
            nonlocal output_string
            nonlocal level
            for child in node:
                if isinstance(child, Element):
                    level += 1
                    output_string += "{}{} {{\n".format("  " * child._level, child.name)
                    construct_string(child)
                elif isinstance(child, Attribute):
                    output_string += "{}{}: {}\n".format("  " * child._level, child.name,
                                                         __from_python_object(child.value))
                if level > child._level:
                    level -= 1
                    output_string += "{}{}".format("  " * level, "}\n")

        level = 0
        output_string = ""
        construct_string(element)
        return output_string


class DefParser(BaseDefParser):
    _pattern = r'(?:data:)|(?:^|\s)(\w+):\s+(.+(?:\s+".*)*)|(\w*)\W{|(})'
    _regex = re.compile(_pattern)

    def __init__(self, root_element):
        super().__init__(root_element)

    def _tree_builder(self, document):
        """searches the document for a match, and builds the tree"""
        regex_match = re.search(self._pattern, document)
        if regex_match:
            element_name = regex_match.group(3)
            attribute_name, attribute_value = regex_match.group(1, 2)
            element_exit = regex_match.group(4)

            if element_name:
                last_element = self._element_chain[-1]
                element = SubElement(last_element, element_name)
                self._element_chain.append(element)
            elif attribute_name and attribute_value:
                if attribute_name == "data":
                    attribute_value = bytes(attribute_value, "utf-8").decode("unicode_escape").replace('\n"\n  "',
                                                                                                       "\n")[1:-1]
                    last_element = self._element_chain[-1]
                    element = SubElement(last_element, "data")
                    self._element_chain.append(element)
                    self._parse(attribute_value)
                    self._element_chain.pop()
                else:
                    last_element = self._element_chain[-1]
                    name = attribute_name
                    value = self._to_python_objects(attribute_value)
                    Attribute(last_element, name, value)
            elif element_exit:
                self._element_chain.pop()

            return regex_match.end()
        return False

    @staticmethod
    def serialize(element):
        """Returns a string of the element"""
        _assert_is_element(element)

        def __from_python_object(_input):
            def is_bool(__input):
                if __input is False:
                    return "false"
                elif __input is True:
                    return "true"
                else:
                    return __input

            return is_bool(_input)

        def construct_string(node):
            """Recursive function that formats the text"""
            nonlocal output_string
            nonlocal level
            for child in node:
                if isinstance(child, Element):
                    if child.name == "data":
                        value = escape_element(child)
                        output_string += "{}{}: {}\n".format("  " * (child.get_parent()._level + 1), child.name, value)
                    else:
                        level += 1
                        output_string += "{}{} {{\n".format("  " * child._level, child.name)
                        construct_string(child)
                elif isinstance(child, Attribute):
                    output_string += "{}{}: {}\n".format("  " * child._level, child.name,
                                                         __from_python_object(child.value))
                if level > child._level and not child.name == "data":
                    level -= 1
                    output_string += "{}{}".format("  " * level, "}\n")

        level = 0
        output_string = ""
        construct_string(element)
        return output_string


def escape_element(ele):
    element = ele.copy()
    embedded = {}
    _root = DefTree().get_root()
    for x in element.iter_all():
        if isinstance(x, Element) and x.name == "data":
            if x._level not in embedded:
                embedded[x._level] = []
            embedded[x._level].append(x)

    while embedded:
        for d in embedded[max(embedded)]:
            d_copy = d.copy()
            value = '"{}"'.format(DefParser.serialize(d_copy).replace('\"', '\\\\"').replace('\n', "\\\n"))
            attr = Attribute(_root, "data", value)
            parent = d.get_parent()
            index = parent._children.index(d)
            parent.remove(d)
            parent.insert(index, attr)
        del embedded[max(embedded)]

    for x in element.iter_all():
        if isinstance(x, Attribute) and isinstance(x.value, str) and x.value.startswith('"') and x.value.endswith('"'):
            x.value = x.value.replace('"', '\\"')

    return '"{}"'.format(DefParser.serialize(element).replace("\n", '\\n\"\n  \"'))


class Element:
    """ Element class.  This class defines the Element interface """

    def __init__(self, name):
        self.name = name
        self._parent = None
        self._level = -1  # Holds how 'deep' the node are in the hierarchy
        self.__index = -1
        self._children = list()

    def __iter__(self):
        self.__index = -1
        for child in self._children:
            yield child

    def __next__(self):
        try:
            result = self._children[self.__index]
        except IndexError:
            raise StopIteration
        self.__index += 1
        return result

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, item):
        self._children[index] = item

    def __delitem__(self, index):
        del self._children[index]

    def __len__(self):
        return len(self._children)

    def _makeelement(self, name):
        """Create a new element with the same type.
        Do not call this method, use the SubElement factory function instead.

        :param name: *name* of the element
        :returns Element"""

        return self.__class__(name)

    def _reset_level(self):
        """Reset the levels of the object, needed when copying"""
        self._level = -1
        for x in self.iter_all():
            x._level = x.get_parent()._level + 1

    def insert(self, index, item):
        _assert_is_element_or_attribute(item)
        item._parent = self
        item._level = self._level + 1
        self._children.insert(index, item)

    def append(self, item):
        _assert_is_element_or_attribute(item)
        item._parent = self
        item._level = self._level + 1
        self._children.append(item)

    def add(self, item, index=-1):
        """Adds an item to the element.

        :param item: *reference* of the element or attribute
        :param index: *index* of where the item should be added"""
        if index == -1:
            self.append(item)
        else:
            self.insert(index, item)

    def iter_all(self):
        """Generator function for all child objects

        :returns generator: child Element and Attribute"""
        def yield_all(element):
            for child in element:
                if isinstance(child, Element):
                    yield child
                    yield from yield_all(child)
                else:
                    yield child

        return yield_all(self)

    def iter_elements(self):
        """Generator function for all child elements

        :returns generator: all child Elements"""
        def yield_elements(element):
            for child in element:
                if isinstance(child, Element):
                    yield child
                    yield from yield_elements(child)

        return yield_elements(self)

    def iter_attributes(self):
        """Generator function for all child attributes

        :returns generator: all child Attribute"""
        def yield_attributes(element):
            for child in element:
                if isinstance(child, Element):
                    yield from yield_attributes(child)
                else:
                    yield child
        return yield_attributes(self)

    def items(self):
        """Returns the elements attributes as a sequence of (name, value) pairs.

        :returns List: of all elements attributes name value pair"""

        _values = list()
        for x in self:
            if isinstance(x, Attribute):
                _values.append((x.name, x.value))
        return _values

    def iter_find_attributes(self, name, value=None):
        """Generator yields attribute found that have the name and value given,
        if value is none then it only searches on name

        :param name: *name* to search for.
        :param value: *value* to search for.
        :returns generator: matching attributes"""

        for child in self.iter_attributes():
            if child.name == name and (value is None or child.value == value):
                yield child

    def iter_find_elements(self, name):
        """Generator yields elements found that have the name

        :param name: *name* to search for.
        :returns generator: matching elements"""

        for child in self.iter_elements():
            if child.name == name:
                yield child

    def get_attribute(self, name, value=None):
        """Returns the first attribute found that have the name and value given,
        if value is none then it only searches on name

        :param name: *name* to search for.
        :param value: *value* to search for.
        :returns Attribute: First Attribute matching *name*. If no exists returns None"""
        for child in self:
            if isinstance(child, Attribute) and child.name == name and (value is None or child.value == value):
                return child
        return None

    def get_element(self, name):
        """Returns a list of attribute found that have the name and value given

        :param name: *name* to search for.
        :returns Element: First Element matching *name*. If no exists returns None"""

        for child in self:
            if isinstance(child, Element) and child.name == name:
                return child
        return None

    def clear(self):
        """Resets an element. This function removes all children, clears all attributes"""
        self.name = None
        self._parent = None
        self._level = -1
        self._children = list()

    def remove(self, child):
        """Removes a child from the element. Compares on instance identity.

        :param child: the *child* element to remove"""

        for index, _child in enumerate(self):
            if child is _child:
                del self._children[index]

    def copy(self):
        """Creates a deep copy of the current element

        :returns: Copy of the element"""

        elem = self._makeelement(self.name)
        elem[:] = self
        self._reset_level()
        return elem

    def get_parent(self):
        """Returns the parent of the current Element

        :returns: parent"""
        return self._parent


class Attribute:
    """Attribute class.  This class defines the Attribute interface"""

    def __init__(self, parent, name, value):
        self.name = name
        self.value = value
        self._parent = None
        self._level = -1
        parent.append(self)

    def __eq__(self, other):
        return self.value == other

    def get_parent(self):
        """Returns the parent of the attribute

        :returns Element: Parent of the Attribute"""

        return self._parent


class DefTree:
    """DefTree class. This class represents an entire element hierarchy,
    and adds some extra support for serialization to and from standard XML."""

    def __init__(self):
        self.root = Element("root")
        self.parser = DefParser

    def get_root(self):
        """:returns Element: the root"""
        return self.root

    def write(self, file_path):
        """Writes the element tree to a file.

        :param file_path:"""

        with open(file_path, "w") as document:
            document.write(self.parser.serialize(self.root))

    def dump(self):
        """Write element tree or element structure to sys.stdout.

        This function should be used for debugging only.
        *elem* is either an DefTree, or a single Element."""
        stdout.write(self.parser.serialize(self.root))

    def parse(self, source, parser=DefParser):
        """Loads an external Defold section into this DefTree

        :param source: path to the file.
        :param parser: parser, default DefParser
        :returns Element: the root"""
        self.parser = parser
        parser = self.parser(self.root)
        return parser.parse(source)

    def from_string(self, source, parser=DefParser):
        """Parses an Defold section from a string constant

        :param source: string to parse.
        :param parser: parser, default DefParser
        :returns Element: the root"""

        self.parser = parser
        parser = self.parser(self.root)
        return parser.from_string(source)


def SubElement(parent, name):
    """SubElement factory which creates an element instance, and appends it
    to an existing parent.

    :param parent: the parent element that this will be appended to.
    :param name: the name of the new element.
    :returns Element: new Element"""
    element = parent._makeelement(name)

    parent.append(element)
    return element


def to_string(element, parser=DefParser):
    """Generates a string representation of an DefTree element, including all children

    :param element: Element - to cast to string
    :param parser: parser, default DefParser
    :returns string: string representation of the Element"""

    _assert_is_element(element)
    return parser.serialize(element)


def parse(source):
    """Parse Defold document into DefTree.

    :param source: path to the file.
    :returns : DefTree instance"""

    tree = DefTree()
    tree.parse(source)
    return tree


def to_json(element):
    # Todo: Implement tojson
    raise NotImplementedError("Not implemented, sorry")


def dump(elem, parser=DefParser):
    """Write element tree or element structure to sys.stdout.

    This function should be used for debugging only.
    *elem* is either an DefTree, or a single Element."""
    if isinstance(elem, DefTree):
        elem = elem.get_root()
    stdout.write(parser.serialize(elem))


def validate(string, path, verbose=False):
    """Checks if the string is the same as the file at path
    This function should be used for debugging only."""

    from hashlib import md5
    from os import path as os_path
    is_valid = False

    def _generate_hash(input_string):
        m = md5()
        m.update(input_string)
        my_hash = m.hexdigest()
        return my_hash

    if os_path.isfile(path):
        with open(path, 'r') as read_file:
            buf = read_file.read()
            source_hash = _generate_hash(buf.encode('utf-8'))
    else:
        source_hash = _generate_hash(path.encode('utf-8'))

    string_hash = _generate_hash(string.encode('utf-8'))
    if string_hash == source_hash:
        is_valid = True
    if verbose:
        stdout.write("Is the input the same as the output: %s" % is_valid)
    return is_valid


def _assert_is_element_or_attribute(item):
    if not isinstance(item, Element) and not isinstance(item, Attribute):
        raise TypeError('expected an Element or Attribute, not %s' % type(item).__name__)


def _assert_is_element(item):
    if not isinstance(item, Element):
        raise TypeError('expected an Element, not %s' % type(item).__name__)


def _assert_is_attribute(item):
    if not isinstance(item, Attribute):
        raise TypeError('expected an Attribute, not %s' % type(item).__name__)
