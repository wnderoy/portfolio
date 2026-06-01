import urllib.request
import json
import re

# returns the direct raw web address for any given file
def get_raw_url(owner, repo, path):
    return f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}"

# downloads the raw text and mathematically patches relative image paths
def fetchrepofile(owner, repo, path):
    url = get_raw_url(owner, repo, path)
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
            # precompiles markdown images using the exact source repository
            if path.endswith('.md'):
                pattern = r'!\[(.*?)\]\((?!http)(.*?)\)'
                replacement = f'![\\1]({get_raw_url(owner, repo, "\\2")})'
                content = re.sub(pattern, replacement, content)
                
            return content
    except Exception as error:
        print(f"failed to fetch {path} error {error}")
        return None

# coordinates the downloading and creates the final json structure
def builddatabase():
    my_owner = "wnderoy"
    
    configuration = {
        "Oz Yosef Yohay": [
            {"name": "README.md", "type": "text", "repo": "portfolio", "path": "README.md"}
        ],
        "C++": [
            {"name": "README.md", "type": "text", "repo": "pinuk", "path": "README.md"},
            {"name": "News_Compare.pdf", "type": "binary", "repo": "pinuk", "path": "News_Compare.pdf"}
        ],
        "VERIFIED": [
            {"name": "index.html", "type": "text", "repo": "portfolio", "path": "index.html"}
        ]
    }
    
    finaldata = {}
    for category, filelist in configuration.items():
        finaldata[category] = {}
        for target in filelist:
            if target["type"] == "text":
                content = fetchrepofile(my_owner, target["repo"], target["path"])
                if content:
                    finaldata[category][target["name"]] = content
                else:
                    finaldata[category][target["name"]] = f"PRINT the error file missing {target['path']} from {target['repo']}"
            else:
                finaldata[category][target["name"]] = get_raw_url(my_owner, target["repo"], target["path"])
                
    with open("data.json", "w") as outfile:
        json.dump(finaldata, outfile, indent=4)
    print("synchronization complete data updated")

builddatabase()