import os
import shutil
import unittest

# hack the import
import sys
if os.path.dirname(os.path.dirname(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import deftree


def is_valid(path):
    tree = deftree.parse(path)
    root = tree.get_root()
    return deftree.validate(deftree.to_string(root), path)


class TestDefTreeParsing(unittest.TestCase):
    root_path = os.path.join(os.path.dirname(__file__), "data")

    @classmethod
    def setUpClass(cls):
        os.makedirs(os.path.join(cls.root_path, "_copy"), exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(cls.root_path, "_copy"))

    def test_parsing_embedded_data(self):
        path = os.path.join(self.root_path, "embedded.defold")
        self.assertTrue(is_valid(path), "Failed validating - embedded.defold")

    def test_parsing_nested_embedded_data(self):
        path = os.path.join(self.root_path, "nested.defold")
        self.assertTrue(is_valid(path), "Failed validating - nested.defold")

    def test_parsing_with_special_characters(self):
        path = os.path.join(self.root_path, "special_character.defold")
        self.assertTrue(is_valid(path), "Failed validating - special_character.defold")

    def test_parsing_invalid_document(self):
        with self.assertRaises(deftree.ParseError):
            is_valid(os.path.join(self.root_path, "not_a_valid.defold"))
        with self.assertRaises(deftree.ParseError):
            is_valid(os.path.join(self.root_path, "not_a_valid_text.defold"))


class TestDefTree(unittest.TestCase):
    root_path = os.path.join(os.path.dirname(__file__), "data")

    @classmethod
    def setUpClass(cls):
        os.makedirs(os.path.join(cls.root_path, "_copy"), exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(cls.root_path, "_copy"))

    def test_writing_empty_file(self):
        output_path = os.path.join(self.root_path, "_copy", "empty.defold")
        tree = deftree.DefTree()
        tree.write(output_path)
        self.assertTrue(os.path.exists(output_path), "Failed writing file")

    def test_adding_attributes_to_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        root.add_attribute("my_attribute", "my_value")
        self.assertTrue((root.get_attribute("my_attribute") == "my_value"), "Failed adding attribute")

    def test_adding_sub_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        element = root.add_element("my_element")
        self.assertTrue((root.get_element("my_element") == element), "Failed adding element")

    def test_getting_invalid_element_return_none(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        self.assertIsNone(root.get_element("Nothing"), "Failed adding element")

    def test_editing_attribute_value(self):
        path = os.path.join(self.root_path, "simple.defold")
        output_path = os.path.join(self.root_path, "_copy", "edit.defold")
        tree = deftree.parse(path)
        root = tree.get_root()
        root.set_attribute("extrude_borders", 99)
        tree.write(output_path)
        self.assertTrue(deftree.validate(deftree.to_string(root), output_path))

    def test_rewrite_file(self):
        path = os.path.join(self.root_path, "simple.defold")
        output_path = os.path.join(self.root_path, "_copy", "rewrite.defold")
        shutil.copy(path, output_path)

        tree = deftree.parse(output_path)
        tree.write(output_path)
        self.assertTrue(is_valid(output_path), "Failed rewriting file")

    def test_writing_to_unknown_location_raises_FileNotFoundError(self):
        output_path = os.path.join(self.root_path, "_copy", "unknown", "rewrite.defold")
        tree = deftree.DefTree()
        with self.assertRaises(FileNotFoundError):
            tree.write(output_path)

    def test_getting_missing_attribute(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        self.assertIsNone(root.get_attribute("missing_attribute"), "Failed when returning missing attribute")

    def test_element_is_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        self.assertTrue(isinstance(root, deftree.Element), "Failed asserting Element")

    def test_attribute_is_attribute(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        attribute = root.add_attribute("name", "value")
        self.assertTrue(isinstance(attribute, deftree.Attribute), "Failed asserting Element")

    def test_comparing_attribute_value(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        root.add_attribute("name", "value")
        self.assertTrue(root.get_attribute("name") == "value", "Failed asserting Element")

    def test_removing_children(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = root.add_element("parent")
        child1 = parent.add_element("child1")
        child2 = parent.add_element("child2")
        parent.remove(child2)
        self.assertIn(child1, parent, "child1 is not found")
        self.assertNotIn(child2, root, "Failed deleting child")

    def test_clear_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = root.add_element("parent")
        parent.add_attribute("id", "true")
        parent.add_attribute("name", "element")
        parent.clear()
        self.assertIsNone(parent.get_attribute("id"), "Failed clearing element")

    def test_length_of_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        self.assertTrue(len(root) == 0, "Fail checking length of Element, more than one child")
        root.add_element("parent")
        self.assertTrue(len(root) == 1, "Failed checking length of Element, too many children")

    def test_iterating_elements(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = root.add_element("parent")
        child = parent.add_attribute("id", True)
        self.assertIn(parent, root.iter_elements())
        self.assertNotIn(child, root.iter_elements())

    def test_iterating_direct_attributes(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent_element = root.add_element("parent")
        child_attribute = parent_element.add_attribute("id", True)
        self.assertIn(child_attribute, parent_element.attributes())
        self.assertNotIn(parent_element, root.attributes())

    def test_iterating_attributes(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent_element = root.add_element("parent")
        child_element = parent_element.add_element("child")
        child_attribute = child_element.add_attribute("id", True)
        self.assertIn(child_attribute, parent_element.iter_attributes("id"))

    def test_iter_element_with_filter(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = root.add_element("parent")
        child = parent.add_element("child")
        self.assertIn(child, root.iter_elements("child"))

    def test_reading_from_string(self):
        string_doc = """profiles {\n  name: "Landscape"\n  qualifiers {\n    width: 1280\n    height: 720\n  }\n}"""
        string_tree = deftree.from_string(string_doc)
        string_root = string_tree.get_root()

        tree = deftree.DefTree()
        root = tree.get_root()
        profiles = root.add_element("profiles")
        profiles.add_attribute("name", '"Landscape"')
        qualifiers = profiles.add_element("qualifiers")
        qualifiers.add_attribute("width", "1280")
        qualifiers.add_attribute("height", "720")
        self.assertTrue(deftree.validate(deftree.to_string(string_root), deftree.to_string(root)))

    def test_getting_the_next_child(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        check_against = ["first", "second", "third", "forth", "fifth"]
        root.add_attribute("first", "bah")
        root.add_attribute("second", "true")
        root.add_attribute("third", "atr")
        root.add_attribute("forth", "atr")
        root.add_attribute("fifth", "atr")
        for name in check_against:
            self.assertTrue(next(root).name == name)

    def test_getting_stop_iteration_on_next(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        check_against = ["first", "second", "missing"]
        root.add_attribute("first", "bah")
        root.add_attribute("second", "true")
        with self.assertRaises(StopIteration):
            for _ in check_against:
                next(root)

    def test_asserts(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        attribute = root.add_attribute("attr", 1)
        element = root.add_element("element")
        try:
            deftree.assert_is_element_or_attribute(element)
            deftree.assert_is_element_or_attribute(attribute)
        except TypeError:
            self.fail()

        try:
            deftree.assert_is_element(element)
        except TypeError:
            self.fail()

        try:
            deftree.assert_is_attribute(attribute)
        except TypeError:
            self.fail()


class TestDefTreeAttributes(unittest.TestCase):
    def test_deftree_attribute_numbers_assignment(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        number = root.add_attribute("number", 0)
        self.assertTrue(number == 0, "Comparing number to int")
        number += 1
        self.assertTrue(number == 1, "Number after adding not correct")
        number -= 1
        self.assertTrue(number == 0, "Comparing number to int")
        self.assertTrue(isinstance(number, deftree.DefTreeNumber),
                        "DefTreeNumber after arithmetics are not DefTreeNumber")

    def test_deftree_attribute_numbers_comparision(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        number = root.add_attribute("number", 0.0)
        science = root.add_attribute("science", "4.1751063E-15")
        science2 = root.add_attribute("science2", "4.6049512E-4")
        self.assertTrue(science == 4.1751063e-15, "Comparing number to int")
        self.assertTrue(science2 == 4.6049512E-4, "Comparing number to int")
        self.assertTrue(number == 0, "Comparing number to int")
        self.assertTrue(number == 0.0, "Comparing number to float")
        self.assertTrue(number < 1.0, "Less than comparision")
        self.assertTrue(number > -1.0, "More than comparision")
        self.assertTrue(number >= 0, "More or equal to comparision")
        self.assertTrue(number <= 0, "More or equal to comparision")

    def test_deftree_attribute_number_types(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        number_float_float = root.add_attribute("number_float_float", 0.0)
        number_float_string = root.add_attribute("number_float_string", "0.0")
        number_float_science_long = root.add_attribute("number_float_science_long", "4.1751063E-15")
        number_float_science_short = root.add_attribute("number_float_science_short", "4.6049512E-1")
        number_int_int = root.add_attribute("number_int_int", 4)
        number_int_string = root.add_attribute("number_int_string", "4")
        self.assertTrue(isinstance(number_float_float, deftree.DefTreeFloat))
        self.assertTrue(isinstance(number_float_string, deftree.DefTreeFloat))
        self.assertTrue(isinstance(number_float_science_long, deftree.DefTreeFloat))
        self.assertTrue(isinstance(number_float_science_short, deftree.DefTreeFloat))
        self.assertTrue(isinstance(number_int_int, deftree.DefTreeInt))
        self.assertTrue(isinstance(number_int_string, deftree.DefTreeInt))

    def test_deftree_attribute_string_comparision(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        the_string = "my_string"
        fake_parsed_string = root.add_attribute("Attribute", '"{}"'.format(the_string))
        self.assertTrue(fake_parsed_string == the_string, "Comparing strings, fake parsed")
        my_string_attribute = root.add_attribute("Attribute2", the_string)
        self.assertTrue(my_string_attribute == the_string, "Comparing strings, normally added")
        self.assertTrue(isinstance(fake_parsed_string, deftree.DefTreeString))
        self.assertTrue(isinstance(my_string_attribute, deftree.DefTreeString))

    def test_deftree_attribute_enum_comparision(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        the_enum = "MY_FAKE_ENUM"
        not_an_enum = "nOT_AN_ENUM"
        my_enum = root.add_attribute("Attribute", the_enum)
        self.assertTrue(my_enum == the_enum, "Comparing enums")
        not_enum = root.add_attribute("Attribute2", not_an_enum)
        self.assertTrue(isinstance(my_enum, deftree.DefTreeEnum))
        self.assertFalse(isinstance(not_enum, deftree.DefTreeEnum))

    def test_deftree_attribute_bool_comparision(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        my_string_true = root.add_attribute("Attribute1", "true")
        my_string_false = root.add_attribute("Attribute2", "false")
        my_bool_true = root.add_attribute("Attribute3", True)
        my_bool_false = root.add_attribute("Attribute4", False)
        self.assertTrue(my_string_true == True)
        self.assertTrue(my_bool_true == True)
        self.assertTrue(my_string_false == False)
        self.assertTrue(my_bool_false == False)
        self.assertFalse(isinstance(my_string_true.__class__, deftree.DefTreeBool))

    def test_attribute_set_number(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        number = root.add_attribute("number", 0.0)
        self.assertTrue(number == 0, "Comparing number to int")
        self.assertTrue(number == 0.0, "Comparing number to float")

        root.set_attribute("number", 0.0)
        self.assertTrue(number == 0, "Comparing number to int")
        self.assertTrue(number == 0.0, "Comparing number to float")

        root.set_attribute("number", "1.0")
        self.assertTrue(number == 1, "Comparing number to int")
        self.assertTrue(number == 1.0, "Comparing number to float")

        root.set_attribute("number", 2)
        self.assertTrue(number == 2, "Comparing number to int")
        self.assertTrue(number == 2.0, "Comparing number to float")

        with self.assertRaises(ValueError):
            root.set_attribute("number", "")

    def test_attribute_set_string(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        the_string = "my_string"
        root.add_attribute("Attribute", '"{}"'.format(the_string))
        root.set_attribute("Attribute", "str")
        self.assertTrue(root.get_attribute("Attribute") == "str")

        root.set_attribute("Attribute", '"str"')
        self.assertTrue(root.get_attribute("Attribute") == "str")

        root.set_attribute("Attribute", 1)
        self.assertTrue(root.get_attribute("Attribute") == "1")

        root.set_attribute("Attribute", True)
        self.assertTrue(root.get_attribute("Attribute") == "True")

    def test_attribute_set_enum(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        the_enum = "MY_FAKE_ENUM"
        not_an_enum = "nOT_AN_ENUM"
        my_enum = root.add_attribute("Attribute", the_enum)
        self.assertTrue(my_enum == the_enum, "Comparing enums")

        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", not_an_enum)
        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", 1.0)
        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", False)

    def test_attribute_set_bool(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        root.add_attribute("Attribute", "true")
        self.assertTrue(root.get_attribute("Attribute") == True)
        root.set_attribute("Attribute", True)
        self.assertTrue(root.get_attribute("Attribute") == True)
        root.set_attribute("Attribute", 1)
        self.assertTrue(root.get_attribute("Attribute") == True)
        root.set_attribute("Attribute", "false")
        self.assertTrue(root.get_attribute("Attribute") == False)
        root.set_attribute("Attribute", False)
        self.assertTrue(root.get_attribute("Attribute") == False)
        root.set_attribute("Attribute", 0)
        self.assertTrue(root.get_attribute("Attribute") == False)
        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", "str")
        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", "")
        with self.assertRaises(ValueError):
            root.set_attribute("Attribute", None)

    def test_attribute_number_representation(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        d_number = root.add_attribute("number", 10)
        self.assertTrue(d_number == 10)
        self.assertTrue(d_number.value == 10)
        self.assertTrue(d_number.string == "10")

    def test_attribute_enum_representation(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        d_enum = root.add_attribute("enum", "ENUM")
        self.assertTrue(d_enum == "ENUM")
        self.assertTrue(d_enum.value == "ENUM")
        self.assertTrue(d_enum.string == "ENUM")

    def test_attribute_string_representation(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        d_string = root.add_attribute("string", "deftree")
        self.assertTrue(d_string == "deftree")
        self.assertTrue(d_string.value == "deftree")
        self.assertTrue(d_string.string == '"deftree"')

    def test_attribute_bool_representation(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        d_bool = root.add_attribute("bool", True)
        self.assertTrue(d_bool == True)
        self.assertTrue(d_bool.value is True)
        self.assertTrue(d_bool.string == "true")


class PublicAPITests(unittest.TestCase):
    """Ensures that the correct values are exposed in the public API."""

    def test_module_all_attribute(self):
        self.assertTrue(hasattr(deftree, '__all__'))
        target_api = ["DefTree", "to_string", "parse", "dump", "validate"]
        self.assertEqual(set(deftree.__all__), set(target_api))


def run():   # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDefTree)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':   # pragma: no cover
    run()
