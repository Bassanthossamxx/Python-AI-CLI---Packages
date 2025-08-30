# GitPython Review Notes

## 🔹 1. Setup & Repo Access
First, install GitPython if you haven't:

```bash
pip install GitPython
```

Then, in Python:

```python
from git import Repo

repo = Repo('.')   # '.' means current directory (must be inside a Git repo)
print(repo)        # prints repo info (like path, branch)
```

---
- we will use it to get diffs of staged files for commit message generation.
- `Repo` object → represents the Git repository.
- now let's explore how to get staged files and their diffs.
---
## 🔹 2. Staged vs Unstaged

* **Staged changes** → `git add file.py` (ready to commit).
* **Unstaged changes** → modified, but not added.
* We only care about **staged** changes for commit message generation.

---

## 🔹 3. Get Staged Files

CLI equivalent:

```bash
git diff --name-only --cached
```

GitPython:

```python
staged_files = repo.git.diff("--cached", "--name-only").splitlines() #splitlines() to get list
print(staged_files)
# ['app.py', 'utils/helpers.py']
```

---

## 🔹 4. Get Diff of All Staged Files

CLI equivalent:

```bash
git diff --cached
```

GitPython:

```python
print(repo.git.diff("--cached")) # prints full diff text
```

This prints full diff for all staged files.

---

## 🔹 5. Get Diff for a Specific File

CLI equivalent:

```bash
git diff --cached app.py
```

GitPython:

```python
diff_text = repo.git.diff("--cached", "app.py")
print(diff_text)
```

---

## 🔹 6. Collect File → Diff Mapping (Dict)

This is the **most useful format for AI later**.

```python
def get_staged_diffs(repo_path="."):
    repo = Repo(repo_path)
    staged_files = repo.git.diff("--cached", "--name-only").splitlines()

    diffs = {}
    for f in staged_files:
        diffs[f] = repo.git.diff("--cached", f)

    return diffs

# Example usage:
diffs = get_staged_diffs()
for file, diff in diffs.items():
    print(f"\n--- {file} ---\n{diff}")
```

Output:

```
--- app.py ---
diff --git a/app.py b/app.py
...

--- utils/helpers.py ---
diff --git a/utils/helpers.py b/utils/helpers.py
...
```
### 🔹 What the function returned

When we wrote:

```python
diffs = get_staged_diffs()
```

`diffs` is a **Python dictionary**.
Example structure:

```python
{
    "app.py": "diff --git a/app.py b/app.py\n ...",
    "utils/helpers.py": "diff --git a/utils/helpers.py b/utils/helpers.py\n ..."
}
```

So:

* Keys = filenames (`"app.py"`, `"utils/helpers.py"`)
* Values = diff text (the string with the actual changes)

---

### 🔹 Looping over a dict in Python

By default:

```python
for file in diffs:
    print(file)
```

This loops over **keys only** (so `file` = `"app.py"`, then `"utils/helpers.py"`).
That’s why you don’t get the diff text unless you look it up:

```python
for file in diffs:
    print(file, diffs[file])  # filename + diff
```

---

### 🔹 Cleaner way (looping over keys + values directly)

Python gives us `.items()` for dicts:

```python
for file, diff in diffs.items():
    print("---", file, "---")
    print(diff)
```

Now `file` is the key (filename) and `diff` is the value (diff text) — no need to do `diffs[file]`.

---

## 🔹 7. Why We Need This

* These diffs → will be the **input to AI** to generate commit messages.
* The dict format (`{file: diff}`) makes it easy to package and send in API calls.

---

That’s everything we covered in GitPython.
Think of it as:

* Step 1: **Find which files are staged**
* Step 2: **Get the diff for each file**
* Step 3: **Store results in a dict → ready for AI**

---
