import re
from htmlnode import LeafNode
from textnode import TextNode

TextNodeTypes = ["text", "bold", "italic", "code", "link", "image"]
text_text_type = "text"
bold_text_type = "bold"
italic_text_type = "italic"
code_text_type = "code"
link_text_type = "link"
image_text_type = "image"

def text_to_textnodes(text):
    nodes = [TextNode(text, text_text_type)]
    nodes = split_nodes_delimiter(nodes, "**", bold_text_type)
    nodes = split_nodes_delimiter(nodes, "*", italic_text_type)
    nodes = split_nodes_delimiter(nodes, "`", code_text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

    
def text_node_to_html_node(text_node):
    if not (text_node.text_type in TextNodeTypes):
        raise Exception("Node type not supported")
    if text_node.text_type == text_text_type:
        return LeafNode(None, text_node.text)
    if text_node.text_type == bold_text_type:
        return LeafNode("b", text_node.text)
    if text_node.text_type == italic_text_type:
        return LeafNode("i", text_node.text)
    if text_node.text_type == code_text_type:
        return LeafNode("code", text_node.text)
    if text_node.text_type == link_text_type:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == image_text_type:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != text_text_type:
            new_list.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted sections must be closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_text_type))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_list.extend(split_nodes)
    return new_list

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links 

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_text_type:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdow, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_text_type))
            new_nodes.append(
                TextNode(
                    image[0],
                    image_text_type,
                    image[1]
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_text_type))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_text_type:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_text_type))
            new_nodes.append(TextNode(link[0], link_text_type, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_text_type))
    return new_nodes