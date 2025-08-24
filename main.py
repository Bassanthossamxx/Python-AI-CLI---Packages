# from git import Repo
#  #To check repo name
# repo = Repo('.')
# print(repo) # prints the repo name and place in your system
# print(repo.git.status()) # prints the status of the repo and details
# print(repo.git.branch()) # prints all branches name
# print(repo.active_branch.name) # prints the active branch name
# # list 2 commits in the active branch
# commits = list(repo.iter_commits(repo.active_branch.name))
# for commit in commits:
#     print(commit.message + "  "+ commit.author.name)
# print(repo.git.diff("--cached"))
# import sys
# print(sys.argv)
import sys
if len(sys.argv)<3:
    print("pleas if you want to commit use -m flag")
else:
     if sys.argv[2]=='-m' and len(sys.argv)>=4:
         message = " ".join(sys.argv[3:])
         print("commit message is: ",message)
     else:
          print( "invalid flag or commit message missing")

