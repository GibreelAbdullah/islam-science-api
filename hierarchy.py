import os
import json
from bs4 import BeautifulSoup

def get_directory_structure(rootdir):
    structure = {}
    files_list = []
    with open(os.path.join(rootdir, "FRONTPAGE.html"), "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
        grid_div = soup.find("div", class_="grid")
        links = grid_div.find_all("a") if grid_div else []
        for link in links:
            text = link.get_text(strip=True)
            structure[text] = []
            href = link.get("href", "")
            href = href.replace("/islam-science/", "", 1) + ".html"
            files_list.append({"href": href, "title": text})
            
    for dir_name in files_list:
        dir_path = os.path.join(rootdir, dir_name["href"])
        if dir_path.endswith(".html") and dir_name["href"] != ".html":
            text = ""
            with open(dir_path, "r", encoding="utf-8") as html_file:
                soup = BeautifulSoup(html_file, "html.parser")
                grid_div = soup.find("div", class_="grid")
                links = grid_div.find_all("a") if grid_div else []

                for link in links:
                    text = link.get_text(strip=True)
                    rel_path = link.get("href", "")
                    structure[dir_name["title"]].append({"key": text, "url": rel_path})
    return structure

if __name__ == "__main__":
    # Get the current directory or specify your root directory
    root_directory = os.getcwd()
    
    # Get the directory structure
    dir_structure = get_directory_structure(os.path.join(root_directory, "islam-science"))

    with open("hierarchy.json", "w") as json_file:
        json.dump(dir_structure, json_file, indent=4)