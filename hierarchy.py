import os
import json
from bs4 import BeautifulSoup

def generate_file_structure(path):
    def build_tree(directory, ignoreTopHTML=False):
        tree = {"name": os.path.basename(directory)}
        if os.path.isdir(directory):
            tree["children"] = []
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path):
                    tree["children"].append(build_tree(item_path))
                elif item.endswith(".html") and not (ignoreTopHTML and directory == path):
                    tree["children"].append(build_tree(item_path))
        else:
            text = ""
            with open(directory, "r", encoding="utf-8") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")
                first_p = soup.find("p")
                text = first_p.get_text(strip=True) if first_p else ""
            tree = {"name": text}
        return tree
    return build_tree(path, True)

if __name__ == "__main__":
    current_folder = os.getcwd()
    file_structure = generate_file_structure(os.path.join(current_folder, "islam-science"))
    with open("hierarchy.json", "w") as json_file:
        json.dump(file_structure, json_file, indent=None)