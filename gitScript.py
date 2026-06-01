import urllib.request
import json
import base64

# fetches file data from a specific github directory path and decodes it
def fetch_repo_file(owner, repo, path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    request = urllib.request.Request(url)
    
    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
    except Exception as error:
        print(f"failed to fetch {path}")
        return ""

# main routine to build the dictionary and output the text
def build_data_object():
    owner = "wnderoy"
    repo = "yourrepository"
    
    portfolio_data = {
        "VERIFIED": {
            "proof.dfy": fetch_repo_file(owner, repo, "src/proofs/main.dfy")
        },
        "C++": {
            "main.cpp": fetch_repo_file(owner, repo, "systems/core/main.cpp")
        }
    }
    
    print(json.dumps(portfolio_data, indent=4))

build_data_object()