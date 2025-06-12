import os
import json
from bs4 import BeautifulSoup

def get_directory_structure(rootdir):
    structure = {}
    
    # Get all first-level directories
    for dir_name in os.listdir(rootdir):
        dir_path = os.path.join(rootdir, dir_name)
        if os.path.isdir(dir_path) and dir_name != "images":
            structure[dir_name] = []
            
            # Get all second-level subdirectories
            for subdir_name in os.listdir(dir_path):
                subdir_path = os.path.join(dir_path, subdir_name)
                if os.path.isdir(subdir_path):
                    structure[dir_name].append(subdir_name)
                elif subdir_path.endswith(".html"):
                    text = ""
                    with open(subdir_path, "r", encoding="utf-8") as html_file:
                        soup = BeautifulSoup(html_file, "html.parser")
                        first_p = soup.find("p")
                        text = first_p.get_text(strip=True) if first_p else ""
                        rel_path = os.path.relpath(subdir_path, rootdir)
                        structure[dir_name].append({"key": text, "url": rel_path})
    return structure

if __name__ == "__main__":
    # Get the current directory or specify your root directory
    root_directory = os.getcwd()
    
    # Get the directory structure
    dir_structure = get_directory_structure(os.path.join(root_directory, "islam-science"))

    with open("hierarchy.json", "w") as json_file:
        json.dump(dir_structure, json_file, indent=4)