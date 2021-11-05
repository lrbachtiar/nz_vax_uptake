#!/usr/bin/python
import main
from git import Repo
from datetime import date

today = date.today()

PATH_OF_GIT_REPO = r'./'  # make sure .git folder is properly configured
COMMIT_MESSAGE = 'Vax uptake {} update.'.format(today)

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')    

git_push()