import os
import re
import requests

from django.conf import settings


class GitCloner:
    github_api_url = github_url = "https://api.github.com"

    def __init__(self, *args):
        self.repo_url = None

    def _get_reppo_url(self, repo_url):
        self.repo_url = repo_url

    @property
    def branches(self) -> list:
        owner_repo = self.repo_url.replace("https://github.com/", "").replace(".git", "")
        endpoint = f"/repos/{owner_repo}/branches"
        r = requests.get(f"{self.github_api_url}{endpoint}")
        rj = r.json()
        return [r['name'] for r in rj]

    def if_branch(self, branch):
        if branch in self.branches:
            return True
        else:
            return False

    def switch_branch(self, branch, s_or_d, id, repo_dir):
        if branch(branch):
            os.chdir(repo_dir)
            os.system(f'git checkout --track {s_or_d}{id}/{branch}')
            os.chdir(settings.BASE_DIR)

    def clone_repo(self, source_repo, qwery, id, repo_dir):
        os.chdir('/repos')
        # if cloned before, just update branch
        cloned = [project.source_url for project in qwery]
        if source_repo in qwery:
            return self.update_repo()
        dirs = [name for name in os.listdir(".") if os.path.isdir(name)]
        # if new repo check folders name
        # if we have same name add _new
        os.makedirs(repo_dir)
        # clone repo
        os.chdir(repo_dir)
        os.popen(f'git clone {source_repo}')
        os.system(f'git remote add s{id} {source_repo}')

        os.chdir(settings.BASE_DIR)

    def push_repo(self, source_repo, qwery, id, repo_dir, source_branch, destination_repo_adress, destination_branch):
        if os.path.isdir(repo_dir):
            # if branch exists, if no switch branch
            if self.if_branch():
                # if everything is ok push repo
                os.chdir(repo_dir)
                os.system(f'git checkout {source_branch}')
                os.system(f'git remote add d{id} {destination_repo_adress}')
                os.system(f'git fetch d{id}')
                os.system(f'git branch -M {destination_branch}')
                os.system(f'git push d{id} {destination_branch}')
            else:
                self.switch_branch()
        # if no clone repo
        elif not os.path.isdir(repo_dir):
            self.clone_repo(source_repo, qwery, id, repo_dir)
        os.chdir(settings.BASE_DIR)

    def update_repo(self, source_repo, qwery, id, repo_dir, source_branch, destination_repo_adress, destination_branch):
        if os.path.isdir(repo_dir):
            # if branch exists, if no switch branch
            if self.if_branch():
                # if everything is ok push repo
                os.chdir(repo_dir)
                os.system(f'git pull s{id} {source_branch}')
                os.system(f'git fetch s{id}')
                os.system(f'git checkout --track s{id}/{source_branch}')
                os.system(
                    f'git push d{id} refs/remotes/s{id}/{source_branch}:refs/remotes/d{id}/{destination_branch}')
            else:
                self.switch_branch()
        # if no clone repo
        elif not os.path.isdir(repo_dir):
            self.clone_repo(source_repo, qwery, id, repo_dir)
        os.chdir(settings.BASE_DIR)
        os.chdir(settings.BASE_DIR)

