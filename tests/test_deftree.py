import os
import shutil
import unittest

# hack the import
import sys
if os.path.dirname(os.path.dirname(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import deftree


class TestDeftree(unittest.TestCase):
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

    def test_special_characters(self):
        path = os.path.join(self.root_path, "special_character.defold")
        self.assertTrue(is_valid(path), "Failed validating - special character")

    def test_writing_empty_file(self):
        output_path = os.path.join(self.root_path, "_copy", "empty.defold")
        tree = deftree.DefTree()
        tree.write(output_path)
        self.assertTrue(os.path.exists(output_path), "Failed writing file")

    def test_adding_attributes(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        deftree.Attribute(root, "my_attribute", "my_value")
        self.assertTrue((root.get_attribute("my_attribute").value == "my_value"), "Failed adding attribute")

    def test_adding_element(self):
        tree = deftree.DefTree()
        root = tree.get_root()
        element = deftree.SubElement(root, "my_element")
        self.assertTrue((root.get_element("my_element") == element), "Failed adding element")

    def test_editing_value(self):
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


def is_valid(path, parser=deftree.DefParser):
    tree = deftree.DefTree()
    root = tree.parse(path, parser)
    return deftree.validate(deftree.to_string(root, parser), path)


def run():   # pragma: no cover
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDeftree)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':   # pragma: no cover
    run()
