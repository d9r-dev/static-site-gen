import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    text_text_type,
    image_text_type,
    link_text_type,
    split_nodes_image,
    split_nodes_link
)

from textnode import TextNode

class TestExtractMD(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])

    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_text_type,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_text_type),
                TextNode("image", image_text_type, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_text_type,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", image_text_type, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_text_type,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_text_type),
                TextNode("image", image_text_type, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_text_type),
                TextNode(
                    "second image", image_text_type, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_text_type,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_text_type),
                TextNode("link", link_text_type, "https://boot.dev"),
                TextNode(" and ", text_text_type),
                TextNode("another link", link_text_type, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_text_type),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()