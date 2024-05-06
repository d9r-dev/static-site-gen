
import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "test", None, {"href": "www.test.de"})
        node2 = HTMLNode("p", "test", None, {"href": "www.test.de"})
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)

    def test_not_eq(self):
        node = HTMLNode("p", "test", None, {"href": "www.test.de"})
        node2 = HTMLNode("p", "test2", None, {"href": "www.test.de"})
        self.assertEqual(node.tag, node2.tag)
        self.assertNotEqual(node.value, node2.value)
        self.assertEqual(node.children, node2.children)
        self.assertEqual(node.props, node2.props)
    
    def test_props(self):
        node = HTMLNode("p", "test", None, {"href": "www.test.de"})
        expected_html = " href=\"www.test.de\""
        self.assertEqual(node.props_to_html(), expected_html)
        
    def test_props_parsing_multi(self):
        node = HTMLNode("p", "test", None, {"href": "www.test.de", "target": "_blank"})
        expected_html = " href=\"www.test.de\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected_html)

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        self.assertRaises(ValueError, LeafNode, None, None, None)
    
    def test_raw_text(self):
        node = LeafNode(None, "test", {"href": "test"})
        expected_html = "test"
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html(self):
        node = LeafNode("p", "test", {"href": "test", "target": "_blank"})
        expected_html = "<p href=\"test\" target=\"_blank\">test</p>"
        self.assertEqual(node.to_html(), expected_html)

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold test"),
                LeafNode (None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

if __name__ == "__main__":
    unittest.main()
