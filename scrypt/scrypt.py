import os
import re
import shutil
import pathlib
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
            print('This branch exists')
            return True
        else:
            return False

    def switch_branch(self, branch, s_or_d, id, repo_dir):
        if branch(branch):
            os.chdir(f'repos/{repo_dir}')
            os.system(f'git checkout --track {s_or_d}{id}/{branch}')
            os.chdir(settings.BASE_DIR)
            print(f'Branch swiched to {branch}')

    def clone_repo(self, id, qwery, repo_dir, source_repo, source_branch, destination_repo, destination_branch):
        try:
            # if cloned before, just update branch
            if source_repo in qwery:
                return self.update_repo(source_repo, qwery, id, repo_dir,
                                        source_branch, destination_repo, destination_branch)

            # if new repo check folders name
            pathlib.Path(f'{repo_dir}').mkdir(parents=True, exist_ok=True)
            # clone repo
            os.chdir(repo_dir)
            os.popen(f'git clone {source_repo}')
            os.system(f'git remote add s{id} {source_repo}')
            print('You repository is cloned')
            # send to socket

            os.chdir(settings.BASE_DIR)
            self.clone_info = 'Your repository has been cloned'
        except Exception:
            self.clone_info = f"""You have some mistake\n Check repository info\n 
                                    If repository exists check branch name in {self.branches}\n
                                    If everything is ok contact system administrator to check
                                    access level"""
        os.chdir(settings.BASE_DIR)

    def push_repo(self, source_repo, qwery, id, repo_dir, source_branch, destination_repo, destination_branch):
        try:
            branches = os.popen('pwd')
            current_folder = branches.readlines()[0]
            print(f'Your current folder is {current_folder}')

            print(f'repos/{repo_dir}')
            if os.path.isdir(f'repos/{repo_dir}'):
                # if branch exists, if no switch branch
                if self.if_branch(source_branch):
                    # if everything is ok push repo
                    os.chdir(f'repos/{repo_dir}')
                    os.system(f'git checkout {source_branch}')
                    os.system(f'git remote add d{id} {destination_repo}')
                    os.system(f'git fetch d{id}')
                    os.system(f'git branch -M {destination_branch}')
                    os.system(f'git push d{id} {destination_branch}')
                else:
                    self.switch_branch(source_branch, 's', id, repo_dir)
            # if no clone repo
            elif not os.path.isdir(repo_dir):
                self.clone_repo(id, qwery, repo_dir, source_repo, source_branch, destination_repo, destination_branch)
                # self.push_repo(source_repo, qwery, id, repo_dir, source_branch, destination_repo, destination_branch)
            print('Customer repository has been updated')

            self.push_info = 'Repository has been pushed'
        except:
            self.push_info = f"""You have some mistake\n Check repository info\n 
                                If repository exists check branch name in {self.branches}\n
                                If everything is ok contact system administrator to check
                                access level"""
        os.chdir(settings.BASE_DIR)

    def update_repo(self, source_repo, qwery, id, repo_dir, source_branch, destination_repo_adress, destination_branch):
        try:
            os.chdir('repos/')
            if os.path.isdir(repo_dir):
                # if branch exists, if no switch branch
                if self.if_branch():
                    # if everything is ok push repo
                    os.chdir(repo_dir)
                    os.system(f'git pull s{id} {source_branch}')
                    os.system(f'git fetch s{id}')
                    os.system(f'git remote add d{id} {destination_repo_adress}')
                    os.system(f'git checkout --track s{id}/{source_branch}')
                    os.system(
                        f'git push d{id} refs/remotes/s{id}/{source_branch}:refs/remotes/d{id}/{destination_branch}')
                else:
                    print('Change branch and send data again')
            # if no clone repo
            elif not os.path.isdir(repo_dir):
                self.clone_repo(source_repo, qwery, id, repo_dir)
                self.update_repo(source_repo, qwery, id, repo_dir, source_branch, destination_repo_adress, destination_branch)

            self.update_info = 'Repository has been updated'
        except:
            self.update_info = f"""You have some mistake\n Check repository info\n 
                                If repository exists check branch name in {self.branches}\n
                                If everything is ok contact system administrator to check
                                access level"""
        os.chdir(settings.BASE_DIR)

    def delete_repo(self, source_repo):
        split = re.split('/', source_repo)
        project_folder = split[-1][:-4]
        # getting the folder path from the user
        folder_path = f'repos/{project_folder}'

        # checking whether folder exists or not
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print('Project and folder deleted')
        else:
            # file not found message
            print("File not found in the directory")

        os.chdir(settings.BASE_DIR)

