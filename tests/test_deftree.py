import os
import shutil
import unittest

# hack the import
import sys
if os.path.dirname(os.path.dirname(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import deftree


def is_valid(path, parser=deftree.DefParser):
    tree = deftree.DefTree()
    root = tree.parse(path, parser)
    return deftree.validate(deftree.to_string(root, parser), path)


class TestDefTree(unittest.TestCase):
    root_path = os.path.join(os.path.dirname(__file__), "data")

    @classmethod
    def setUpClass(cls):
        os.makedirs(os.path.join(cls.root_path, "_copy"), exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(os.path.join(cls.root_path, "_copy"))

    def test_parsing_embedded_data(self):
        path = os.path.join(self.root_path, "embedded.defold")
        self.assertTrue(is_valid(path), "Failed validating - embedded data")

    def test_parsing_nested_embedded_data(self):
        path = os.path.join(self.root_path, "nested.defold")
        self.assertTrue(is_valid(path), "Failed validating - nested embedded data")

    def test_parsing_with_special_characters(self):
        path = os.path.join(self.root_path, "special_character.defold")
        self.assertTrue(is_valid(path), "Failed validating - special character")

    def test_parsing_invalid_document(self):
        with self.assertRaises(deftree.ParseError):
            is_valid(os.path.join(self.root_path, "not_a_valid.defold"))
        with self.assertRaises(deftree.ParseError):
            is_valid(os.path.join(self.root_path, "not_a_valid_text.defold"))

    def test_writing_empty_file(self):
        output_path = os.path.join(self.root_path, "_copy", "empty.defold")
        tree = deftree.DefTree()
        tree.write(output_path)
        self.assertTrue(os.path.exists(output_path), "Failed writing file")

    def test_adding_attributes_to_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        deftree.Attribute(root, "my_attribute", "my_value")
        self.assertTrue((root.get_attribute("my_attribute").value == "my_value"), "Failed adding attribute")

    def test_adding_sub_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        element = deftree.SubElement(root, "my_element")
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
        atr = root.get_attribute("extrude_borders")
        atr.value = 99
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
        attribute = deftree.Attribute(root, "name", "value")
        self.assertTrue(isinstance(attribute, deftree.Attribute), "Failed asserting Element")

    def test_comparing_attribute_value(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        attribute = deftree.Attribute(root, "name", "value")
        self.assertTrue(attribute == "value", "Failed asserting Element")
        self.assertTrue(attribute.value == "value", "Failed asserting Element")

    def test_removing_children(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        child1 = deftree.SubElement(parent, "child1")
        child2 = deftree.SubElement(parent, "child2")
        parent.remove(child2)
        self.assertIn(child1, parent, "child1 is not found")
        self.assertNotIn(child2, root, "Failed deleting child")

    def test_clear_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        deftree.Attribute(parent, "id", True)
        deftree.Attribute(parent, "name", "element")
        parent.clear()
        self.assertIsNone(parent.get_attribute("id"), "Failed clearing element")

    def test_length_of_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        self.assertTrue(len(root) == 0, "Fail checking length of Element, more than one child")
        deftree.SubElement(root, "parent")
        self.assertTrue(len(root) == 1, "Failed checking length of Element, to many children")

    def test_iterating_elements(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        child = deftree.Attribute(parent, "id", True)
        self.assertIn(parent, root.iter_elements())
        self.assertNotIn(child, root.iter_elements())

    def test_iterating_attributes(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        child = deftree.Attribute(parent, "id", True)
        self.assertIn(child, root.iter_attributes())
        self.assertNotIn(parent, root.iter_attributes())

    def test_iter_find_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        child = deftree.SubElement(parent, "child")
        self.assertIn(child, root.iter_find_elements("child"))

    def test_iter_find_attribute(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        parent = deftree.SubElement(root, "parent")
        child = deftree.SubElement(parent, "child")
        atr = deftree.Attribute(child, "id", True)
        self.assertIn(atr, root.iter_find_attributes("id"))

    def test_reading_from_string(self):
        string_doc = """profiles {\n  name: "Landscape"\n  qualifiers {\n    width: 1280\n    height: 720\n  }\n}"""
        string_tree = deftree.from_string(string_doc)
        string_root = string_tree.get_root()

        tree = deftree.DefTree()
        root = tree.get_root()
        profiles = deftree.SubElement(root, "profiles")
        deftree.Attribute(profiles, "name", '"Landscape"')
        qualifiers = deftree.SubElement(profiles, "qualifiers")
        deftree.Attribute(qualifiers, "width", 1280)
        deftree.Attribute(qualifiers, "height", 720)

        self.assertTrue(deftree.validate(deftree.to_string(string_root), deftree.to_string(root)))

    def test_getting_the_next_child(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        check_against = ["first", "second", "third", "forth", "fifth"]
        deftree.Attribute(root, "first", "bah")
        deftree.Attribute(root, "second", True)
        deftree.Attribute(root, "third", "atr")
        deftree.Attribute(root, "forth", "atr")
        deftree.Attribute(root, "fifth", "atr")
        for name in check_against:
            self.assertTrue(next(root).name == name)

    def test_getting_stop_iteration_on_next(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        check_against = ["first", "second", "missing"]
        deftree.Attribute(root, "first", "bah")
        deftree.Attribute(root, "second", True)
        with self.assertRaises(StopIteration):
            for _ in check_against:
                next(root)


class PublicAPITests(unittest.TestCase):
    """Ensures that the correct values are exposed in the public API."""

    def test_module_all_attribute(self):
        self.assertTrue(hasattr(deftree, '__all__'))
        target_api = ["DefTree", "DefParser", "Element", "Attribute", "SubElement",
                      "to_string", "parse", "dump", "validate", "ParseError"]
        self.assertEqual(set(deftree.__all__), set(target_api))


def run():   # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDefTree)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':   # pragma: no cover
    run()