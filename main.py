from git import Repo
repo = Repo('.')
print(repo) # prints the repo name and place in your system
print(repo.git.diff("--cached"))
# import sys
# print(sys.argv)
# import sys
# if len(sys.argv)<3:
#     print("pleas if you want to commit use -m flag")
# else:
#      if sys.argv[2]=='-m' and len(sys.argv)>=4:
#          message = " ".join(sys.argv[3:])
#          print("commit message is: ",message)
#      else:
#           print( "invalid flag or commit message missing")
#
# #s