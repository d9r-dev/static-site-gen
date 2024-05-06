import os
import shutil
from textnode import TextNode
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
tempalte_path = "./template.html"

def copy_tree(path):
    fragment = path.split("/")[2:]
    fragment = "/".join(fragment)
    new_path = "./public/"+fragment
    if os.path.isfile(path):
        print(f"copying file {path}")
        shutil.copy(path, new_path)
    else:
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        dirs = os.listdir(path)
        for dir in dirs:
            copy_tree(path + "/" + dir)

def copy_static():
    if not os.path.exists("./static/"):
        raise Exception("Static path does not exist")
    if os.path.exists("./public/"):
        shutil.rmtree("./public/")
    os.mkdir("./public/")
    copy_tree("./static")
    
def main():
   copy_static()
   print("Generatring page...")
   generate_pages_recursive(dir_path_content, tempalte_path, dir_path_public)

if __name__ == "__main__":
    main()

