#------------------------GitPython------------------------
#Task 1 in GitPython:
"""
from git import Repo
repo = Repo(".")
branch = repo.active_branch
print(branch)
"""
#################################################
#Task 2 in GitPython:
"""
from git import Repo
repo = Repo(".")
staged_files =repo.git.diff("--staged" , "--name-only")
print("Staged files :\n",staged_files)
"""
#################################################
#Task 3 in GitPython:
"""
from git import Repo
repo = Repo(".")
staged_diffs =repo.git.diff("--staged")
print("Staged files :\n",staged_diffs)
"""
#################################################
#Task 4 in GitPython:
"""
from git import Repo
repo = Repo(".")
file_names = repo.git.diff("--staged" , "--name-only")
for f in file_names.split("\n"):
    print(f"------------------------------- {f}-----------------------------------\n")
    staged_diffs =repo.git.diff("--staged", f)
    print(staged_diffs)
"""
#####################################################
#Task 5 in GitPython:
"""
from git import Repo

def get_staged_diffs(repo_path="."):
    repo = Repo(repo_path)

    # Get staged files (list of names)
    file_names = repo.git.diff("--cached", "--name-only").splitlines()

    diffs = {}  # our dict

    for f in file_names:
        diff_text = repo.git.diff("--cached", f)
        diffs[f] = diff_text   # store filename → diff text

    return diffs

staged_diffs = get_staged_diffs()

if not staged_diffs:
    print("No staged files found.")
else:
    print("Files captured:", list(staged_diffs.keys()))  # print just the filenames
    print("\n--- Preview of diffs ---\n")
    for file, diff in staged_diffs.items():
        print(f"{file}: {diff[:200]}...\n")  # only first 200 chars
"""
#####################################################
#------------------------CLI Args "sys.argv"------------------------
#Task 1 in sys.argv:
# import sys
# length = len(sys.argv)
# arr = list(sys.argv)
# for i in range(length):
#     print(f"Arg {i}: {arr[i]}")
######################################################
#Task 2 & 3 & 4 in sys.argv:
import sys
length = len(sys.argv)
print(f"Length of sys.argv: {length}")
if length <2 :
    print("Please provide an valid command.""")
elif length >=4 and sys.argv[1] == "gen" and sys.argv[2] == "-m" :
        commit_message = sys.argv[3:]
        print(f"Commit message: {commit_message}")
    # filename gen -m "commit message"
elif length ==2 and sys.argv[1] == "diff":
    print("showing diff of staged files...")
else:
    print("Invalid command. Usage: filename gen -m \"commit message\"")

