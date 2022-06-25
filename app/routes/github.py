from fastapi import APIRouter, Depends
from git import Repo
import re
import math

router = APIRouter()


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class Github:
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
        commit_size = convert_size(repos.head.commit.size)
    except:
        commit_size = "ERROR - Cannot get commit size!"
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
        repo_size = repos.git.count_objects("-H")
    except:
        repo_size = "ERROR - Cannot get repo size!"
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


@router.get("/")
def get_branch_name(repozi: str = Depends(Github)):
    response = {
        "repo_name": Github.repo_name[1:],
        "repo_link": Github.repo_url,
        "repo_commit_number": Github.repo_commit_number,
        "repo_size": Github.repo_size[12:],
        "branch_info": [
            {
                "active_branch": Github.current_branch,
                "active_branch_url": Github.current_branch_url,
                "active_branch_commit_number": Github.current_branch_commit_number,
            }
        ],
        "commit_info": [
            {
                "active_commit": Github.current_commit,
                "active_commit_hash_long": Github.current_commit_hash,
                "commit_author": Github.commit_author,
                "commit_date": Github.commit_date,
                "commit_size": Github.commit_size,
            }
        ],
    }
    return response
