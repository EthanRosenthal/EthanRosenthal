import os 

from github import Github

def leftpad(s, pad, total_width):
    size = len(s)
    to_pad = total_width - size 
    return pad * to_pad + s 


token = os.environ["PERSONAL_ACCESS_TOKEN"]
gh = Github(token)
repos = [
    repo for repo in gh.get_user().get_repos(visibility="public", affiliation="owner")
    if not repo.fork
]
repos = sorted(repos, key=lambda x: -x.stargazers_count)
repo_infos = []
for repo in repos:
    repo_infos.append(
        f"{repo.stargazers_count} ⭐ [{repo.name}]({repo.html_url}): "
        f"{repo.description if repo.description else ''} ({repo.created_at.year})"
    )

with open("README.md", "r") as f:
    readme = f.read()

start_pattern = "<!-- BEGIN LIST -->"
end_pattern = "<!-- END LIST -->"
start_index = readme.find(start_pattern) + len(start_pattern)
end_index = readme.find("<!-- END LIST -->")
readme = (
    readme[:start_index] + "\n- " + "\n- ".join(repo_infos) + "\n" + readme[end_index:]
)

this_repo = repo = [r for r in repos if r.name == "EthanRosenthal"][0]
contents = repo.get_contents("README.md", ref="main")
repo.update_file(
    contents.path, 
    "Automatic Update From GitHub Actions", 
    readme, 
    contents.sha, 
    branch="main"
)
