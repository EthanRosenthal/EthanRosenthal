import os 

from github import Github
import pandas as pd

# A unicode star emoji
STAR = u"\u2606"


token = os.environ["PERSONAL_ACCESS_TOKEN"]
gh = Github(token)

# Find all repos that I made that are not a fork.
repos = [
    repo for repo in gh.get_user().get_repos(visibility="public", affiliation="owner")
    if not repo.fork
]

# Convert to a DataFrame
repo_df = pd.DataFrame(
    [
        {
            # The name is a markdown link.
            "name":  f"[{repo.name}]({repo.html_url})", 
            "description": repo.description if repo.description else "", 
            STAR: repo.stargazers_count,
            "created": repo.created_at.year
        }
        for repo in repos

    ]
)
# Sort rows and order the columns.
repo_df = repo_df.sort_values(STAR, ascending=False)
repo_df = repo_df[[STAR, "name", "description", "created"]]

repo_markdown = repo_df.to_markdown(index=False)


with open("README.md", "r") as f:
    readme = f.read()

# Replace the table in the README by finding this hacky start and end template.
start_pattern = "<!-- BEGIN LIST -->"
end_pattern = "<!-- END LIST -->"
start_index = readme.find(start_pattern) + len(start_pattern)
end_index = readme.find("<!-- END LIST -->")

readme = (
    readme[:start_index] + "\n" + repo_markdown + "\n" + readme[end_index:]
)

# Commit the results.
this_repo = [r for r in repos if r.name == "EthanRosenthal"][0]
contents = this_repo.get_contents("README.md", ref="main")
this_repo.update_file(
    contents.path, 
    "Automatic Update From GitHub Actions", 
    readme, 
    contents.sha, 
    branch="main"
)
