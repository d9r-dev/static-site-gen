import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", "bold", "test")
        self.assertEqual(node.url, "test")

    def test_no_url(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.url, None)



if __name__ == "__main__":
    unittest.main()
