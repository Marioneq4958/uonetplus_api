from tests.checks.status_code import status_check
from tests.routes.login import client
from git import Repo
import re


def github_info_backend_test(fg):
    try:
        try:
            repos = Repo(path=r"./wulkanowy-web/", search_parent_directories=True)
        except:
            repos = Repo(path=r"../..", search_parent_directories=True)
    except:
        repos = Repo(path=r".", search_parent_directories=True)
    try:        
        current_commit_hash = repos.head.commit.hexsha
    except:
        current_commit_hash = "ERROR - Cannot get commit hash!"
    try:
        commit_author = repos.head.commit.author.name
    except:
        commit_author = "ERROR - Cannot get commit author!"
    try:
        commit_date = repos.head.commit.committed_datetime.strftime("%d.%m.%Y %H:%M")
    except:
        commit_date = "ERROR - Cannot get commit date!"
    try:
        repo_url = repos.remote("origin").url
    except:
        repo_url = "ERROR - Cannot get repo url!"
    try:
        repo_name = re.search(r"\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+.*", str(repo_url)).group(0)
    except:
        repo_name = "ERROR - Cannot get repo name!"
    try:
        repo_commit_number = repos.git.rev_list("--count", "develop")
    except:
        repo_commit_number = "ERROR - Cannot get repo commit number!"
    try:
        #current_branch = repos.active_branch.name
        current_branch = current_commit_hash
    except:
        current_branch = "ERROR - Cannot get current branch!"
    if current_branch == "ERROR - Cannot get current branch!":
        current_branch_url = "null"
    else:
        try:
            current_branch_url = repo_url + "/tree/" + current_commit_hash
        except:
            current_branch_url = "ERROR - Cannot get current branch url!"
    response = client.get("/api/v1/github/backend")
    status_check(response.status_code, response.json(), fg)
    assert response.json()["repo_name"] == repo_name[1:]
    assert response.json()["repo_link"] == repo_url
    assert response.json()["repo_commit_number"] == repo_commit_number
    assert response.json()["branch_info"][0]["active_branch_url"] == current_branch_url
    assert (
        response.json()["commit_info"][0]["active_commit_hash_long"]
        == current_commit_hash
    )
    assert response.json()["commit_info"][0]["commit_date"] == commit_date
    assert response.json()["commit_info"][0]["commit_author"] == commit_author


def github_info_frontend_test(fg):
    try:
        try:
            repos = Repo(path=r"./wulkanowy-web/", search_parent_directories=True)
        except:
            repos = Repo(path=r"..", search_parent_directories=True)
    except:
        repos = Repo(path=r".", search_parent_directories=True)
    try:        
        current_commit_hash = repos.head.commit.hexsha
    except:
        current_commit_hash = "ERROR - Cannot get commit hash!"
    try:
        commit_author = repos.head.commit.author.name
    except:
        commit_author = "ERROR - Cannot get commit author!"
    try:
        commit_date = repos.head.commit.committed_datetime.strftime("%d.%m.%Y %H:%M")
    except:
        commit_date = "ERROR - Cannot get commit date!"
    try:
        repo_url = repos.remote("origin").url
    except:
        repo_url = "ERROR - Cannot get repo url!"
    try:
        repo_name = re.search(r"\/[a-zA-Z0-9]+\/[a-zA-Z0-9]+.*", str(repo_url)).group(0)
    except:
        repo_name = "ERROR - Cannot get repo name!"
    try:
        repo_commit_number = repos.git.rev_list("--count", "develop")
    except:
        repo_commit_number = "ERROR - Cannot get repo commit number!"
    try:
        current_branch = repos.active_branch.name
    except:
        current_branch = "ERROR - Cannot get current branch!"
    if current_branch == "ERROR - Cannot get current branch!":
        current_branch_url = "null"
    else:
        try:
            current_branch_url = repo_url + "/tree/" + current_branch
        except:
            current_branch_url = "ERROR - Cannot get current branch url!"
    response = client.get("/api/v1/github/frontend")
    status_check(response.status_code, response.json(), fg)
    assert response.json()["repo_name"] == repo_name[1:]
    assert response.json()["repo_link"] == repo_url
    assert response.json()["repo_commit_number"] == repo_commit_number
    assert response.json()["branch_info"][0]["active_branch_url"] == current_branch_url
    assert (
        response.json()["commit_info"][0]["active_commit_hash_long"]
        == current_commit_hash
    )
    assert response.json()["commit_info"][0]["commit_date"] == commit_date
    assert response.json()["commit_info"][0]["commit_author"] == commit_author