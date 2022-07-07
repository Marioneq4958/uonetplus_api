from fastapi import APIRouter, Depends
from git import Repo
import re
import math

router = APIRouter()

class GithubFr:
    try:
        try:
            repos = Repo(path=r"./wulkanowy-web/", search_parent_directories=True)
            print("Github1")
        except:
            repos = Repo(path=r"..", search_parent_directories=True)
            print("Github2")
    except:
        repos = Repo(path=r".", search_parent_directories=True)
        print("Github3")
    try:        
        current_commit_hash = repos.head.commit.hexsha
    except:
        current_commit_hash = "ERROR - Cannot get commit hash!"
    try:
        c_number_master = repos.git.rev_list("--count", "develop")
    except:
        c_number_master = "ERROR - Cannot get develop branch commit number!"
    try:
        commit_author = repos.head.commit.author.name
    except:
        commit_author = "ERROR - Cannot get commit author!"
    try:
        commit_date = repos.head.commit.committed_datetime.strftime("%d.%m.%Y %H:%M")
    except:
        commit_date = "ERROR - Cannot get commit date!"
    try:
        cc = repos.head.commit.message
        current_commit = cc.rstrip()
    except:
        current_commit = "ERROR - Cannot get commit message!"
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
    try:
        c_number_current_branch = repos.git.rev_list("--count", "HEAD", current_branch)
    except:
        c_number_current_branch = (
            "ERROR - Connot get " + current_branch + "branch commit number!"
        )
    if current_branch == "ERROR - Cannot get current branch!":
        current_branch_url = "null"
    else:
        try:
            current_branch_url = repo_url + "/tree/" + current_branch
        except:
            current_branch_url = "ERROR - Cannot get current branch url!"
    try:
        if int(c_number_master) - (int(c_number_current_branch) > 0):
            current_branch_commit_number = int(c_number_current_branch) - int(
                c_number_master
            )
        else:
            current_branch_commit_number = int(c_number_master) - int(
                c_number_current_branch
            )
    except:
        current_branch_commit_number = "ERROR - Cannot calculate!"


@router.get("/frontend")
def get_branch_name(repozi: str = Depends(GithubFr)):
    response = {
        "repo_name": GithubFr.repo_name[1:],
        "repo_link": GithubFr.repo_url,
        "repo_commit_number": GithubFr.repo_commit_number,
        "branch_info": [
            {
                "active_branch": GithubFr.current_branch,
                "active_branch_url": GithubFr.current_branch_url,
                "active_branch_commit_number": GithubFr.current_branch_commit_number,
            }
        ],
        "commit_info": [
            {
                "active_commit": GithubFr.current_commit,
                "active_commit_hash_long": GithubFr.current_commit_hash,
                "commit_author": GithubFr.commit_author,
                "commit_date": GithubFr.commit_date,
            }
        ],
    }
    return response


class GithubBac:
    try:
        try:
            repos = Repo(path=r"./wulkanowy-web/", search_parent_directories=True)
            print("Github1")
        except:
            repos = Repo(path=r"../..", search_parent_directories=True)
            print("Github2")
    except:
        repos = Repo(path=r".", search_parent_directories=True)
        print("Github3")
    try:        
        current_commit_hash = repos.head.commit.hexsha
    except:
        current_commit_hash = "ERROR - Cannot get commit hash!"
    try:
        c_number_master = repos.git.rev_list("--count", "develop")
    except:
        c_number_master = "ERROR - Cannot get develop branch commit number!"
    try:
        commit_author = repos.head.commit.author.name
    except:
        commit_author = "ERROR - Cannot get commit author!"
    try:
        commit_date = repos.head.commit.committed_datetime.strftime("%d.%m.%Y %H:%M")
    except:
        commit_date = "ERROR - Cannot get commit date!"
    try:
        cc = repos.head.commit.message
        current_commit = cc.rstrip()
    except:
        current_commit = "ERROR - Cannot get commit message!"
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
    try:
        c_number_current_branch = repos.git.rev_list("--count", "HEAD", current_branch)
    except:
        c_number_current_branch = (
            "ERROR - Connot get " + current_branch + "branch commit number!"
        )
    if current_branch == "ERROR - Cannot get current branch!":
        current_branch_url = "null"
    else:
        try:
            current_branch_url = repo_url + "/tree/" + current_commit_hash
        except:
            current_branch_url = "ERROR - Cannot get current branch url!"


@router.get("/backend")
def get_branch_name(repozi: str = Depends(GithubBac)):
    response = {
        "repo_name": GithubBac.repo_name[1:],
        "repo_link": GithubBac.repo_url,
        "repo_commit_number": GithubBac.repo_commit_number,
        "branch_info": [
            {
                "active_branch": GithubBac.current_branch,
                "active_branch_url": GithubBac.current_branch_url,
            }
        ],
        "commit_info": [
            {
                "active_commit": GithubBac.current_commit,
                "active_commit_hash_long": GithubBac.current_commit_hash,
                "commit_author": GithubBac.commit_author,
                "commit_date": GithubBac.commit_date,
            }
        ],
    }
    return response
