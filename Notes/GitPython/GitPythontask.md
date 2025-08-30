
# GitPython Practice Tasks

### ✅ Task 1 – Open a Repo

* Write a function `open_repo(path=".")` that returns a Repo object.
* Print the **active branch name**.

  ```python
  repo.active_branch.name
  ```
#### DONE
---

### ✅ Task 2 – List Staged Files

* Get all staged files (like `git diff --name-only --cached`).
* Print them one by one.
* Example output:

  ```
  Staged files:
  - app.py
  - utils/helpers.py
  ```
#### DONE
---

### ✅ Task 3 – Print Full Diff (All Files)

* Get the diff of all staged changes in one string (`repo.git.diff("--cached")`).
* Print it.
#### DONE
---

### ✅ Task 4 – Print Diff Per File

* Loop through staged files.
* Print their diffs separately (filename as a header).

  ```
  --- app.py ---
  diff --git a/app.py b/app.py
  ...
  ```
#### DONE
---

### ✅ Task 5 – Store in a Dict

* Build a dictionary: `{ "filename": "diff text" }`.
* Print just the **keys** (to check files are stored).
* Then print the first 200 chars of each diff (to preview without flooding terminal).

#### DONE
---

### ✅ Task 6 – Extract Only Added/Removed Lines

(Advanced, optional now — but useful later for AI.)

* Parse the diff text and collect only lines starting with `+` or `-` (ignoring headers like `+++`, `---`).
* Example:

  ```
  + print("new line")
  - print("old line")
  ```

---

If you do these 6 tasks, you’ll be 100% comfortable with GitPython basics.
Then you’re ready to **connect GitPython → CLI (argparse/click)** → AI later.

---