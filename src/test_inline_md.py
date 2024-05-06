import unittest

from textnode import TextNode

from htmlnode import LeafNode

from inline_markdown import (
    split_nodes_delimiter,
    text_text_type,
    bold_text_type,
    link_text_type,
    image_text_type,
    italic_text_type,
    text_node_to_html_node,
    code_text_type,
    text_to_textnodes
)

class TestInlineMarkdown(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("test", "text")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode(None, "test", None))

    def test_bold(self):
        text_node = TextNode("test", "bold")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("b", "test"))
    
    def test_italic(self):
        text_node = TextNode("test", "italic")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("i", "test"))
    
    def test_code(self):
        text_node = TextNode("test", "code")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("code", "test"))

    def test_link(self):
        text_node = TextNode("test", "link", "/")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("a", "test", {"href": "/"}))

    def test_image(self):
        text_node = TextNode("test", "image", "www")
        self.assertEqual(text_node_to_html_node(text_node), LeafNode("img", "", {"src": "www", "alt": "test"}))

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_text_type)
        new_nodes = split_nodes_delimiter([node], "**", bold_text_type)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_text_type),
                TextNode("bolded", bold_text_type),
                TextNode(" word", text_text_type),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_text_type
        )
        new_nodes = split_nodes_delimiter([node], "**", bold_text_type)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_text_type),
                TextNode("bolded", bold_text_type),
                TextNode(" word and ", text_text_type),
                TextNode("another", bold_text_type),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_text_type
        )
        new_nodes = split_nodes_delimiter([node], "**", bold_text_type)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_text_type),
                TextNode("bolded word", bold_text_type),
                TextNode(" and ", text_text_type),
                TextNode("another", bold_text_type),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_text_type)
        new_nodes = split_nodes_delimiter([node], "*", italic_text_type)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_text_type),
                TextNode("italic", italic_text_type),
                TextNode(" word", text_text_type),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_text_type)
        new_nodes = split_nodes_delimiter([node], "`", code_text_type)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_text_type),
                TextNode("code block", code_text_type),
                TextNode(" word", text_text_type),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](/)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_text_type),
                TextNode("text", bold_text_type),
                TextNode(" with an ", text_text_type),
                TextNode("italic", italic_text_type),
                TextNode(" word and a ", text_text_type),
                TextNode("code block", code_text_type),
                TextNode(" and an ", text_text_type),
                TextNode("image", image_text_type, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_text_type),
                TextNode("link", link_text_type, "/"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()