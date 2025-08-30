# Python AICommitGenerator CLI & Package – Learning Tracker


## Goal

Build a CLI tool `ai-commit-gen` that:

* Reads staged diffs using GitPython
* Parses arguments using Click (preferred)
* Generates commit messages (first fake, later powered by AI Gemini 2.5 Pro)
* Ships as a Python package
* Finally, connects to a Next.js frontend

---

## Learning Path

### Step 1 – GitPython (done, refine one more task)

* [x] Learn basics of gitpython
* [x] Get staged files
* [x] Get diffs of staged changes → `repo.git.diff('--cached')`
* [ ] Write a helper function `get_staged_diff()` returning diff as text

**Reference:**

* GitPython Docs: [https://gitpython.readthedocs.io/en/stable/](https://gitpython.readthedocs.io/en/stable/)
* Example Tutorial: [https://www.pythonguis.com/tutorials/gitpython-intro/](https://www.pythonguis.com/tutorials/gitpython-intro/)

---

### Step 2 – CLI Arguments

* [x] Learn sys.argv basics
* [ ] Learn argparse → build a CLI with commands:

  * `gen` → generate commit message
  * `diff` → print staged diff
* [ ] Learn click → rebuild the same commands using click
* Decision: Final project will use click (cleaner & scalable).

**Reference:**

* sys.argv: [https://docs.python.org/3/library/sys.html#sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)
* argparse Tutorial: [https://docs.python.org/3/howto/argparse.html](https://docs.python.org/3/howto/argparse.html)
* click Docs: [https://click.palletsprojects.com/en/stable/](https://click.palletsprojects.com/en/stable/)

---

### Step 3 – Project Structure

```
ai_commit_tool/
│── cli.py        # entrypoint (click commands)
│── git_utils.py  # GitPython helpers
│── ai_utils.py   # AI integration (Gemini later)
│── __init__.py   # package init
tests/
│── test_cli.py
pyproject.toml    # packaging
```

* [ ] Create basic structure
* [ ] Add dummy functions (return hardcoded text)
* [ ] Make CLI import helpers

**Reference:**

* Python Packaging Guide: [https://packaging.python.org/en/latest/tutorials/packaging-projects/](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
* Structuring Python Projects: [https://docs.python-guide.org/writing/structure/](https://docs.python-guide.org/writing/structure/)

---

### Step 4 – Commit Message Rules

* [ ] Learn Conventional Commits (feat:, fix:, chore:)
* [ ] Learn imperative mood style (“Add login check” not “Added login check”)
* [ ] Write a fake generator function returning a styled commit message

Example:

```python
def generate_fake_commit_message(diff: str) -> str:
    return "feat: add basic commit generator (hardcoded)"
```

**Reference:**
* Eqraa Guide for commit message rules: [https://eqraatech.com/git-commit-message-cheatsheet/](Eqraa doc for commit messages)
* Conventional Commits Spec: [https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/)
* Git Commit Best Practices: [https://cbea.ms/git-commit/](https://cbea.ms/git-commit/)

---

### Step 5 – Connect the Pieces (Non-AI version)

* [ ] CLI gen command → calls `get_staged_diff()` → sends to fake generator
* [ ] CLI prints result in terminal
* [ ] Test locally with real git repos

**Reference:**

* Example CLI App with click: [https://realpython.com/comparing-python-command-line-parsing-libraries-argparse-docopt-click/](https://realpython.com/comparing-python-command-line-parsing-libraries-argparse-docopt-click/)
* Git diff concepts: [https://git-scm.com/docs/git-diff](https://git-scm.com/docs/git-diff)

---

### Step 6 – AI Integration (Gemini 2.5 Pro)

* [ ] Learn OpenAI/Google Generative AI Python API usage
* [ ] Implement `generate_commit_message(diff)` using AI
* [ ] Swap out fake generator with AI generator
* [ ] Add arguments like:

  * `--style` (conventional, casual, detailed)
  * `-m` (manual override)

**Reference:**

* Google Generative AI (Python SDK): [https://ai.google.dev/docs](https://ai.google.dev/docs)
* OpenAI Python Docs (for comparison): [https://platform.openai.com/docs/guides/text-generation/python](https://platform.openai.com/docs/guides/text-generation/python)

---

## Next Phases (Post-Learning)

### Packaging

* [ ] Add `pyproject.toml` with dependencies (click, gitpython, google-generativeai)
* [ ] Install locally with `pip install -e .`
* [ ] Publish to PyPI

**Reference:**

* Python Packaging (official): [https://packaging.python.org/](https://packaging.python.org/)
* Publishing to PyPI: [https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)

---

### UI (Next.js)

* [ ] Build frontend Doc UI with Next.js + Copilot

**Reference:**

* Next.js Docs: [https://nextjs.org/docs](https://nextjs.org/docs)
---

## Current Focus

Learn argparse and click → then replace current sys.argv logic with one of those.

---
