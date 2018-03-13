"""
 Defold files are an inherently hierarchical data format and the most natural way to
 represent this is through a tree. This module uses three classes for this purpose:

    1. DefTree represents the whole document as a tree

    2. Element represents a single node in this tree

    3. Attribute represent a name value pair
"""
from re import compile as re_compile
from sys import stdout
__version__ = "1.1.1"
__all__ = ["DefTree", "to_string", "parse", "dump", "validate", "is_attribute", "is_element"]


class ParseError(SyntaxError):
    pass


class BaseDefParser:  # pragma: no cover
    _pattern = ''
    _regex = re_compile(_pattern)
    file_path = None

    def __init__(self, root_element):
        self.root = root_element
        self._element_chain = [self.root]

    def _raise_parse_error(self):
        if self.file_path:
            raise ParseError("Error when parsing file: {}".format(self.file_path))
        raise ParseError("Error when parsing supplied document")

    def parse(self, source):
        """Loads an external Defold section into this DefTree

        :param source: path to the file.
        :returns Element: root Element"""
        self.file_path = source
        document = self._open(self.file_path)
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
        """Searches the document for a match and builds the tree"""
        return False

    @staticmethod
    def _get_level(child):
        element_level = -1

        def _count_up(_child, count):
            parent = _child.get_parent()
            if not parent:
                return count

            return _count_up(parent, count+1)
        return _count_up(child, element_level)

    @staticmethod
    def _open(_path):
        """Returns the documents data as a string"""

        with open(_path, "r") as document:
            current_document = document.read()
        return current_document

    @classmethod
    def serialize(cls, element):
        """Returns a string of the element"""
        return ""


class DefParser(BaseDefParser):
    _pattern = r'(?:data:)|(?:^|\s)(\w+):\s+(.+(?:\s+".*)*)|(\w*)\W{|(})'
    _regex = re_compile(_pattern)

    def __init__(self, root_element):
        super().__init__(root_element)

    def _tree_builder(self, document):
        """Searches the document for a match and builds the tree"""
        regex_match = self._regex.search(document)
        if not regex_match and len(document) > 25:
            self._raise_parse_error()
        if regex_match:
            element_name = regex_match.group(3)
            attribute_name, attribute_value = regex_match.group(1, 2)
            element_exit = regex_match.group(4)

            if element_name:
                if self._element_chain:
                    last_element = self._element_chain[-1]
                else:
                    self._raise_parse_error()  # pragma: no cover
                element = last_element.add_element(element_name)
                self._element_chain.append(element)
            elif attribute_name and attribute_value:
                if attribute_name == "data":
                    attribute_value = bytes(attribute_value, "utf-8").decode("unicode_escape").replace('\n"\n  "',
                                                                                                       "\n")[1:-1]
                    last_element = self._element_chain[-1]
                    element = last_element.add_element("data")
                    self._element_chain.append(element)
                    self._parse(attribute_value)
                    self._element_chain.pop()
                else:
                    if self._element_chain:
                        last_element = self._element_chain[-1]
                    else:
                        self._raise_parse_error()  # pragma: no cover
                    last_element.add_attribute(attribute_name, attribute_value)

            elif element_exit:
                if self._element_chain:
                    self._element_chain.pop()
                else:
                    self._raise_parse_error()  # pragma: no cover

            return regex_match.end()
        return False

    @classmethod
    def serialize(cls, element, internal=False):
        """Returns a string of the element"""
        assert_is_element(element)

        def construct_string(node):
            """Recursive function that formats the text"""
            nonlocal output_string
            nonlocal level
            for child in node:
                element_level = cls._get_level(child)
                if is_element(child):
                    if child.name == "data" and not internal:
                        value = cls._escape_element(child)
                        output_string += "{}{}: {}\n".format("  " * element_level, child.name, value)
                    else:
                        level += 1
                        output_string += "{}{} {{\n".format("  " * element_level, child.name)
                        construct_string(child)
                elif is_attribute(child):
                    output_string += "{}{}: {}\n".format("  " * element_level, child.name,
                                                         child.string)
                if level > element_level and not child.name == "data":
                    level -= 1
                    output_string += "{}{}".format("  " * level, "}\n")

        level = 0
        output_string = ""
        construct_string(element)
        return output_string

    @classmethod
    def _escape_element(cls, ele):
        def yield_attributes(element_parent):
            for child in element_parent:
                if is_attribute(child):
                    yield child
                else:
                    yield from yield_attributes(child)
        data_elements = dict()
        data_elements[cls._get_level(ele)] = [ele]

        for x in ele.iter_elements():
            if is_element(x) and x.name == "data":
                lvl = cls._get_level(x)
                if lvl not in data_elements:
                    data_elements[lvl] = []
                data_elements[lvl].append(x)

        while data_elements:
            for x in data_elements[max(data_elements)]:
                for a in yield_attributes(x):
                    if isinstance(a, DefTreeString) and a.string.startswith('"') and a.string.endswith('"'):
                        a._value = a.string.replace('"', '\\"')
                _root = DefTree().get_root()
                attr = _root.add_attribute("data", "")
                parent = x.get_parent()
                index = parent.index(x)
                parent.remove(x)
                parent.insert(index, attr)
                x._parent = None
                text = cls.serialize(x, True)
                _root.set_attribute("data", '"{}"'.format(text.replace('\"', '\\\"').replace('\n', "\\\n")))
                del data_elements[max(data_elements)]

        return '"{}"'.format(cls.serialize(ele).replace("\n", '\\n\"\n  \"'))


class Element:
    """ Element class. This class defines the Element interface"""
    __float_regex = re_compile("[-\d]+\.\d+[eE-]+\d+|[-\d]+\.\d+")
    __enum_regex = re_compile('[A-Z_]+')

    def __init__(self, name):
        self.name = name
        self._parent = None
        self.__index = -1
        self._children = list()

    def __iter__(self):
        self.__index = -1
        for child in self._children:
            yield child

    def __next__(self):
        try:
            result = self._children[self.__index + 1]
        except IndexError:
            raise StopIteration
        self.__index += 1
        return result

    def __getitem__(self, index):
        return self._children[index]

    def __setitem__(self, index, item):
        assert_is_element_or_attribute(item)
        self._children[index] = item

    def __delitem__(self, index):  # pragma: no cover
        del self._children[index]

    def __len__(self):
        return len(self._children)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.name)

    def __get_type(self, x):

        num_match = self.__float_regex.match(str(x))
        if num_match:
            if isinstance(x, float) or len(num_match.group(0)) == len(x):
                return float
            else:
                return str
        try:
            int(x)
        except ValueError:
            return str
        else:
            return int

    def _makeelement(self, name):
        """Returns a new element.
        Do not call this method, use the add_element factory function instead."""
        return self.__class__(name)

    def add_element(self, name):
        """Creates an :class:`.Element` instance with name as a child to self."""
        element = self._makeelement(name)
        self.append(element)
        return element

    def _make_attribute(self, name, v):
        enum_match = self.__enum_regex.match(str(v))
        if isinstance(v, bool) or v == "true" or v == "false":
            return DefTreeBool(self, name, v)
        elif enum_match and len(enum_match.group(0)) == len(v):
            return DefTreeEnum(self, name, v)

        a_type = self.__get_type(v)
        if a_type is int:
            return DefTreeInt(self, name, v)
        elif a_type is float:
            return DefTreeFloat(self, name, v)
        return DefTreeString(self, name, v)

    def add_attribute(self, name, value):
        """Creates an :class:`.Attribute` instance with name and value as a child to self."""

        attr = self._make_attribute(name, value)
        return attr

    def index(self, item):
        """Returns the index of the item in this element, raises `ValueError` if not found."""
        for i, child in enumerate(self._children):
            if child is item:
                return i
        raise ValueError("{} is not in children".format(item))

    def insert(self, index, item):
        """Inserts the item at the given position in this element.
        Raises `TypeError` if item is not a :class:`.Element` or :class:`.Attribute`"""
        assert_is_element_or_attribute(item)
        item._parent = self
        self._children.insert(index, item)

    def append(self, item):
        """Inserts the item at the end of this element's internal list of children.
               Raises `TypeError` if item is not a :class:`.Element` or :class:`.Attribute`"""
        assert_is_element_or_attribute(item)
        item._parent = self
        self._children.append(item)

    def iter(self):
        """Creates a tree iterator with the current element as the root. The iterator iterates over this
        element and all elements below it in document (depth first) order.
        Both :class:`.Element` and :class:`.Attribute` are returned from the iterator."""

        def yield_all(element):
            for child in element:
                if is_element(child):
                    yield child
                    yield from yield_all(child)
                else:
                    yield child

        return yield_all(self)

    def iter_elements(self, name=None):
        """iter_elements([name])
        Creates a tree iterator with the current element as the root. The iterator iterates over this
        element and all elements below it, in document (depth first) order. If the optional argument name is not None only
        :class:`.Element` with a name equal to name is returned."""

        def yield_elements(element):
            for child in element:
                if is_element(child):
                    if name is None or child.name == name:
                        yield child
                        yield from yield_elements(child)
                    else:
                        yield from yield_elements(child)

        return yield_elements(self)

    def iter_attributes(self, name=None):
        """iter_attributes([name])
        Creates a tree iterator with the current element as the root. The iterator iterates over this
        element and all elements below it, in document (depth first) order. If the optional argument name is not None
        only :class:`.Attribute` with a name equal to name is returned."""

        def yield_attributes(element):
            for child in element:
                if is_element(child):
                    yield from yield_attributes(child)
                else:
                    if name is None or child.name == name:
                        yield child

        return yield_attributes(self)

    def attributes(self, name=None, value=None):
        """attributes([name, value])
        Iterates over the current element and returns all attributes.
        Only :class:`.Attributes`. Name and value are optional and used for filters."""

        for child in self:
            if is_attribute(child):
                if (name is None or child.name == name) and (value is None or child == value):
                    yield child

    def elements(self, name=None):
        """elements([name])
        Iterates over the current element and returns all elements. If the optional argument name is not None only
        :class:`.Element` with a name equal to name is returned."""

        for child in self:
            if is_element(child) and (name is None or child.name == name):
                yield child

    def get_attribute(self, name, value=None):
        """get_attribute(name, [value])
        Returns the first :class:`Attribute` instance whose name matches name and if value is not None whose value equal
        value. If no matching attribute is found it returns None."""

        for child in self:
            if is_attribute(child) and child.name == name and (value is None or child == value):
                return child
        return None

    def get_element(self, name):
        """Returns the first :class:`Element` whose name matches name, if none is found returns None."""

        for child in self:
            if is_element(child) and child.name == name:
                return child
        return None

    def set_attribute(self, name, value):
        """Sets the first :class:`Attribute` with name to value."""

        element = self.get_attribute(name)
        element.value = value

    def clear(self):
        """Resets an element. This function removes all children, clears all attributes"""

        self.name = None
        self._parent = None
        self._children = list()

    def remove(self, child):
        """Removes child from the element. Compares on instance identity not name.
        Raises `TypeError` if child is not a :class:`.Element` or :class:`.Attribute`"""

        assert_is_element_or_attribute(child)
        for index, _child in enumerate(self):
            if child is _child:
                del self._children[index]

    def copy(self):
        """Returns a deep copy of the current :class:`.Element`."""

        from copy import deepcopy
        return deepcopy(self)

    def get_parent(self):
        """Returns the parent of the current :class:`.Element`"""

        return self._parent


class Attribute:
    """Attribute class. This class defines the Attribute interface."""

    def __init__(self, parent, name, value):
        self.name = name
        self._value = ""
        self.value = value  # To trigger the setter
        self._parent = None
        parent.append(self)

    @property
    def string(self):
        return str(self._value)

    @property
    def value(self):
        """A property of the attribute, used to set and get the attributes value"""

        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    def __repr__(self):
        return '{0}({1!r}, {2!r})'.format(self.__class__.__name__, self.name, self.value)

    def __eq__(self, other):
        return self.value == other

    def __len__(self):
        return len(self.value)

    def get_parent(self):
        """Returns the parent element of the attribute."""

        return self._parent


class DefTreeNumber(Attribute):
    def __init__(self, parent, name, value):
        super(DefTreeNumber, self).__init__(parent, name, value)

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __sub__(self, other):
        self.value -= other
        return self

    def __add__(self, other):
        self.value += other
        return self

    def __mul__(self, other):
        self.value *= other
        return self

    def __truediv__(self, other):
        return NotImplemented

    def __floordiv__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __divmod__(self, other):
        return NotImplemented

    def __pow__(self, other, modulo):
        return NotImplemented

    def __lshift__(self, other):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented


class DefTreeFloat(DefTreeNumber):
    def __init__(self, parent, name, value):
        super(DefTreeFloat, self).__init__(parent, name, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = float(v)

    @property
    def string(self):
        return str(self._value).upper()


class DefTreeInt(DefTreeNumber):
    def __init__(self, parent, name, value):
        super(DefTreeInt, self).__init__(parent, name, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = int(v)


class DefTreeString(Attribute):
    def __init__(self, parent, name, value):
        super(DefTreeString, self).__init__(parent, name, value)

    @property
    def value(self):
        return self._value[1:-1]

    @value.setter
    def value(self, v):
        if not isinstance(v, str):
            raise ValueError("Expected string got {}".format(type(v)))
        if v.endswith('"') and v.startswith('"'):
            self._value = v
        else:
            self._value = '"{}"'.format(v)

    def endswith(self, suffix, start=None, end=None):
        return self.value.startswith(suffix, start, end)

    def startswith(self, prefix, start=None, end=None):
        return self.value.startswith(prefix, start, end)

    def strip(self, chars=None):
        return self.value.strip(chars)

    def rstrip(self, chars=None):
        return self.value.strip(chars)

    def count(self, sub, start=None, end=None):
        return self.value.count(sub, start, end)

    def index(self, sub, start=None, end=None):
        return self.value.index(sub, start, end)

    def rindex(self, sub, start=None, end=None):
        return self.value.rindex(sub, start, end)

    def replace(self, old, new, count=-1):
        return self.value.replace(old, new, count)


class DefTreeEnum(Attribute):
    __enum_regex = re_compile('[A-Z_]+')

    def __init__(self, parent, name, value):
        super(DefTreeEnum, self).__init__(parent, name, value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        enum_match = self.__enum_regex.match(str(v))
        if not (isinstance(v, str) and enum_match and len(enum_match.group(0)) == len(v)):
            raise ValueError("Unsupported value, enum expected to be an all upper case string.")
        self._value = v


class DefTreeBool(Attribute):
    def __init__(self, parent, name, value):
        super(DefTreeBool, self).__init__(parent, name, value)

    @property
    def string(self):
        return "true" if self._value == True else "false"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if v in ["true", True]:
            self._value = True
        elif v in ["false", False]:
            self._value = False
        else:
            raise ValueError("Unsupported boolean value.")


class DefTree:
    """DefTree class. This class represents an entire element hierarchy."""

    def __init__(self):
        self.root = Element("root")
        self._parser = DefParser

    def get_document_path(self):
        """Returns the path to the parsed document."""
        return self._parser.file_path

    def get_root(self):
        """Returns the root :class:`.Element`"""

        return self.root

    def write(self, file_path):
        """Writes the element tree to a file, as plain text. `file_path` needs to be a path."""

        with open(file_path, "w") as document:
            document.write(self._parser.serialize(self.root))

    def dump(self):  # pragma: no cover
        """Writes the the DefTree structure to sys.stdout. This function should be used for debugging only."""

        stdout.write(self._parser.serialize(self.root))

    def parse(self, source, parser=DefParser):
        """parse(source, [parser])
        Parses a Defold document into a :class:`.DefTree` which it returns. `source` is a file_path.
        `parser` is an optional parser instance. If not given the standard parser is used."""

        self._parser = parser
        self._parser.file_path = source
        parser = self._parser(self.root)
        return parser.parse(source)

    def from_string(self, text, parser=DefParser):
        """from_string(text, [parser])
        Parses a Defold document section from a string constant which it returns.
        `parser` is an optional parser instance. If not given the standard parser is used.
        Returns the root of :class:`.DefTree`."""

        self._parser = parser
        parser = self._parser(self.root)
        return parser.from_string(text)


def is_element(item):
    """Returns True if the item is an :class:`.Element` else returns False"""
    if isinstance(item, Element):
        return True
    return False


def is_attribute(item):
    """Returns True if the item is an :class:`.Attribute` else returns False"""
    if issubclass(item.__class__, Attribute):
        return True
    return False


def to_string(element, parser=DefParser):
    """to_string(element, [parser])
    Generates a string representation of the Element, including all children.
    `element` is a :class:`.Element` instance."""

    assert_is_element(element)
    return parser.serialize(element)


def parse(source):
    """Parses a Defold document into a DefTree which it returns. `source` is a file_path.
    `parser` is an optional parser instance. If not given the standard parser is used."""

    tree = DefTree()
    tree.parse(source)
    return tree


def from_string(text):
    """from_string(text, [parser])
    Parses a Defold document section from a string constant which it returns. `parser` is an optional parser instance.
        If not given the standard parser is used. Returns the root of :class:`.DefTree`."""

    tree = DefTree()
    tree.from_string(text)
    return tree


def dump(element, parser=DefParser):  # pragma: no cover
    """dump(element, [parser])
    Writes the element tree or element structure to sys.stdout. This function should be used for debugging only.
    *element* is either an :class:`.DefTree`, or :class:`.Element`."""

    if isinstance(element, DefTree):
        element = element.get_root()
    stdout.write(parser.serialize(element))


def validate(string, path_or_string, verbose=False):
    """validate(string, path_or_string, [verbose])
    Verifies that a document in string format equals a document in path_or_string.
    If Verbose is True it echoes the result. This function should be used for debugging only.
    Returns a bool representing the result"""

    from hashlib import md5
    from os import path as os_path
    is_valid = False

    def _generate_hash(input_string):
        m = md5()
        m.update(input_string)
        my_hash = m.hexdigest()
        return my_hash

    if os_path.isfile(path_or_string):
        with open(path_or_string, 'r') as read_file:
            buf = read_file.read()
            source_hash = _generate_hash(buf.encode('utf-8'))
    else:
        source_hash = _generate_hash(path_or_string.encode('utf-8'))

    string_hash = _generate_hash(string.encode('utf-8'))
    if string_hash == source_hash:
        is_valid = True
    if verbose:  # pragma: no cover
        stdout.write("Is the input the same as the output: %s" % is_valid)
    return is_valid


def assert_is_element_or_attribute(item):
    if not (is_attribute(item) or is_element(item)):
        raise TypeError('expected an Element or Attribute, not %s' % type(item).__name__)


def assert_is_element(item):
    if not is_element(item):
        raise TypeError('expected an Element, not %s' % type(item).__name__)


def assert_is_attribute(item):
    if not is_attribute(item):
        raise TypeError('expected an Attribute, not %s' % type(item).__name__)
