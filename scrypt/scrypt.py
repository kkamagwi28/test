from django.conf import settings
import os, re, time, json


"""
ssh-keygen -t rsa
'git config --system http.sslCAInfo /home/javl/git-certs/cert.pem'   

"""


class GitCloner:
    def __init__(self, *args):
        pass

    def clone_project(self, source_url, source_id):
        # get repo name
        split = re.split('/', source_url)
        project_folder = split[-1][:-4]

        # change directory to repos
        print(f'Your project folder is {project_folder}')
        os.chdir('repos/')
        branches = os.popen('pwd')
        current_folder = branches.readlines()[0]
        print(f'Your current folder is {current_folder}')

        # making project folder and change location to it
        try:
            os.makedirs(f'{project_folder}')
            os.chdir(f'{project_folder}/')
            branches = os.popen('pwd')
            current_folder = branches.readlines()[0]
            print(f'Your current folder for project is {current_folder}')

            os.popen(f'git clone {source_url}')
            self.clone = 'Repository is cloning, you can press push button'

            # go into folder with .git file of repo
            try:
                os.chdir(f'{project_folder}/')
                branches = os.popen('pwd')
                self.current_folder_git = os.path.abspath(os.getcwd())
                current_folder_git = branches.readlines()
                print(f'Your current folder for project with previous .git  {current_folder_git}')

                os.system(f'git remote add s{source_id} {source_url}')
                # change directory to BASE django dir to help django find its own info
                os.chdir(settings.BASE_DIR)
            except Exception as e:

                self.clone_exeption = str(e)
                os.chdir(settings.BASE_DIR)
        except OSError:
            self.update = 'Press push button to update repository'
            os.chdir(settings.BASE_DIR)

    def updating_branch(self, source_url, source_branch, source_id, destination_branch):
        split = re.split('/', source_url)
        project_folder = split[-1][:-4]
        os.chdir(f'repos/{project_folder}/{project_folder}/')
        branches = os.popen('pwd')
        current_folder_git = branches.readlines()[0]
        print(f'Your current folder for project with previous .git  {current_folder_git}')
        os.system(f'git pull s{source_id} {source_branch}')
        os.system(f'git fetch s{source_id}')
        os.system(f'git checkout --track s{source_id}/{source_branch}')
        os.system(
            f'git push d{source_id} refs/remotes/s{source_id}/{source_branch}:refs/remotes/d{source_id}/{destination_branch}')
        self.updated = "Your repository has been updated"
        os.chdir(settings.BASE_DIR)


    def creating_branch(self, source_url, source_branch, destination_repo_adress, destination_branch,
                        destination_id):
        # getting back to project folder
        split = re.split('/', source_url)
        project_folder = split[-1][:-4]
        os.chdir(f'repos/{project_folder}/{project_folder}/')
        r = os.popen('pwd')
        current_folder_git = r.readlines()
        print(f'You are working in  {current_folder_git}')

        r = os.popen(f'git checkout {source_branch}')
        self.current_branch = r.readlines()
        print(self.current_branch)

        os.system(f'git remote add d{destination_id} {destination_repo_adress}')
        # no output if everything is ok
        os.system(f'git fetch d{destination_id}')

        os.system(f'git branch -M {destination_branch}')
        # no output if everything is ok

        r = os.popen('git status')
        self.status = r.readlines()
        r = os.popen(f'git push d{destination_id} {destination_branch}')
        self.done = r.readlines()

        os.chdir(settings.BASE_DIR)



