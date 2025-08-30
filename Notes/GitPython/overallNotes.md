# GitPython Notes (Beyond Diffs)

## Installation & Basic Import
```bash
pip install GitPython
```
```python
from git import Repo
```
If you only need low-level objects: `from git.objects import Commit, Tree, Blob`.

## Core Concepts (Mapping to native Git)
* Repo → `.git` directory (metadata + refs)
* Commit → snapshot + parents + metadata
* Tree → directory listing (hierarchical)
* Blob → file contents
* Index (`repo.index`) → staging area
* Reference (`repo.heads['main']`, `repo.tags['v1.0']`) → pointer to a commit
* Remote (`repo.remotes.origin`) → remote endpoint

## Creating or Cloning Repos
```python
from git import Repo
# Clone
repo = Repo.clone_from('https://github.com/user/project.git', 'project')
# Init empty
repo = Repo.init('my_repo')
```

## Working Tree & Index
```python
repo.working_tree_dir          # path to checkout
repo.git.status()              # raw git status string
repo.is_dirty()                # True if unstaged or staged changes
repo.untracked_files           # list of untracked files
```
Stage files:
```python
repo.index.add(['file1.py', 'pkg/module.py'])
repo.index.remove(['old.txt'])            # staged removal
```
Write tree & commit:
```python
repo.index.commit('feat: add new module')
```

## Reading File Contents at Specific Revs
```python
commit = repo.head.commit
blob = commit.tree / 'src' / 'main.py'
source = blob.data_stream.read().decode('utf-8')
```

## History & Logs
```python
for c in repo.iter_commits('main', max_count=5):
    print(c.hexsha[:7], c.summary, c.author.name, c.committed_datetime)
```
Filter with paths:
```python
for c in repo.iter_commits(paths='src/app.py'):
    ...
```

## Branches
List & access:
```python
repo.heads                     # sequence
repo.active_branch             # current branch object
repo.heads['feature']          # specific branch
```
Create & checkout:
```python
new_branch = repo.create_head('feature/login')  # create
new_branch.checkout()
```
Delete (force):
```python
repo.delete_head('old-branch', force=True)
```

## Tags
```python
repo.create_tag('v1.0.0')                      # lightweight
repo.create_tag('v1.1.0', message='Release')   # annotated
for t in repo.tags:
    print(t.name, t.commit.hexsha[:7])
```

## Remotes
```python
origin = repo.remotes.origin
origin.fetch()          # update refs only
origin.pull()           # fetch + merge (current branch)
origin.push()           # push current branch
```
Add new remote:
```python
repo.create_remote('upstream', url='https://github.com/other/repo.git')
```
List:
```python
[r.name for r in repo.remotes]
```

## Diff Variants (More Examples)
```python
repo.git.diff()                         # unstaged vs working tree
repo.git.diff('--cached')               # staged vs HEAD
repo.git.diff('HEAD~1..HEAD')           # range
repo.git.diff('feature', 'main', '--', 'src/')  # between branches, path-limited
```
Using objects:
```python
c1 = repo.commit('HEAD~1')
c2 = repo.commit('HEAD')
diff_index = c1.diff(c2)
for d in diff_index:
    print(d.change_type, d.a_path, '->', d.b_path)
```
Change types: 'A' added, 'M' modified, 'D' deleted, 'R' renamed.

## Reset / Checkout / Revert
```python
repo.git.checkout('main')                 # switch branch
repo.git.checkout('-b', 'new-feature')    # create + switch
repo.head.reset(index=True, working_tree=True)  # hard reset to HEAD
repo.git.reset('--hard', 'HEAD~1')        # move branch pointer + wtree
repo.git.revert('abc1234')                # new commit undoing abc1234
```
Detached HEAD caution: after `repo.git.checkout(commit_sha)` you're detached; create a branch to keep work.

## Stash (No High-Level Wrapper)
GitPython delegates; use raw git:
```python
repo.git.stash('save', 'wip: refactor')
repo.git.stash('list')
repo.git.stash('apply', 'stash@{0}')
```

## Submodules
```python
for sm in repo.submodules:
    print(sm.name, sm.module_exists())
# Update
for sm in repo.submodules:
    sm.update(init=True, recursive=True)
```
Add submodule:
```python
repo.create_submodule('libfoo', 'libs/libfoo', url='https://github.com/org/libfoo.git')
```

## Low-Level Object Access
```python
commit = repo.head.commit
parent = commit.parents[0]
print(commit.tree.hexsha)
for blob in commit.tree.traverse():
    if blob.type == 'blob':
        print(blob.path, blob.size)
```

## Performance Tips
* Prefer object methods (`commit.diff()`) over spawning CLI for large diffs.
* Avoid walking full history unless needed: limit with `max_count`.
* Use `Repo.clone_from(..., multi_options=['--depth=1'])` for shallow clones.
* For read-only analytics, cloning bare: `Repo.clone_from(url, path, bare=True)`.

## Common Pitfalls
| Issue | Explanation | Fix |
|-------|-------------|-----|
| InvalidGitRepositoryError | Path not a repo | Wrap Repo() in try/except |
| Detected dubious ownership | Git safety on shared dirs | Set safe.directory or run inside trusted path |
| Detached HEAD | Checkout commit hash directly | Create branch after checkout |
| Stale refs | Remotes not fetched | Call `remote.fetch()` before relying on remote heads |
| Performance slow | Many subprocess diffs | Use object diff APIs |

## Error Handling Pattern
```python
from git import Repo, InvalidGitRepositoryError, NoSuchPathError, GitCommandError
try:
    repo = Repo('.')
except (InvalidGitRepositoryError, NoSuchPathError) as e:
    raise SystemExit(f'Repo problem: {e}')
try:
    repo.git.fetch()
except GitCommandError as e:
    print('Fetch failed', e.stderr)
```

## Author / Committer Info
```python
repo.index.commit('msg', author=repo.config_reader().get_value('user', 'name'),
                  author_email=repo.config_reader().get_value('user', 'email'))
```
Or pass explicit Actor:
```python
from git import Actor
actor = Actor('CI Bot', 'ci@example.com')
repo.index.commit('ci: update', author=actor, committer=actor)
```

## Resolving Refs
```python
repo.commit('HEAD')
repo.commit('main')
repo.commit('abc1234')   # partial sha
repo.git.rev_parse('--short', 'HEAD')
```

## Cleaning Working Tree
```python
repo.git.clean('-fd')   # remove untracked + dirs (DANGEROUS)
```

## Archive / Export
```python
with open('snapshot.zip', 'wb') as f:
    f.write(repo.git.archive('HEAD', format='zip'))  # may need subprocess capture
```

## Quick Reference Snippets
```python
# Latest commit summary
repo.head.commit.summary
# Current branch name
repo.active_branch.name
# List changed (unstaged) files
[ d.a_path for d in repo.head.commit.diff(None) ]
# List staged files (index vs HEAD)
[ d.a_path if d.change_type != 'A' else d.b_path for d in repo.index.diff('HEAD') ]
# Count commits ahead/behind origin/main
ahead = sum(1 for _ in repo.iter_commits('main', f'origin/main..main'))
behind = sum(1 for _ in repo.iter_commits('main', f'main..origin/main'))
```

## When to Use Raw `repo.git` vs High-Level API
* Use `repo.git.*` for rare/advanced commands not wrapped (stash, worktree, sparse-checkout).
* Use object model for structured diffing, commit traversal, metadata.

---

## Minimal Checklist for Commit Message Generation Tool
1. Ensure inside repo → `Repo(path)` success.
2. Collect staged file list.
3. Build `{file: diff}` mapping (optionally truncate long diffs).
4. (Optional) Include commit context (last commit message, branch name, ahead/behind counts).
5. Send to AI.

---

## Further Ideas
* Add heuristic summarizer per file before sending to AI.
* Limit total token size by trimming unchanged context hunks.
* Detect large generated files (skip via size or extension filters).

---

## Config (Read & Write)
```python
config = repo.config_reader()
user = config.get_value('user', 'name')
# Write (needs writer)
with repo.config_writer() as cw:
    cw.set_value('user', 'signingkey', 'ABCDEF1234')
```
System vs global vs repo levels available via `Repo.config_reader(config_level='global')`.

## Blame (Annotate Lines)
```python
blame = repo.blame('HEAD', 'src/app.py')  # list of (Commit, [lines])
for commit, lines in blame:
    print(commit.hexsha[:7], len(lines))
```
Useful for attributing changes when summarizing diffs.

## Merge / Cherry-Pick / Rebase
Merge (no high-level convenience):
```python
repo.git.checkout('main')
repo.git.merge('feature-branch')   # may create conflicts
```
Cherry-pick a commit:
```python
repo.git.cherry_pick('abc1234')
```
Rebase (simple):
```python
repo.git.rebase('origin/main')
```
Handle errors with `GitCommandError` and inspect `.status` / `.stdout`.

## Detecting Merge Conflicts
After a failed merge/cherry-pick:
```python
if repo.index.unmerged_blobs():
    for path, entries in repo.index.unmerged_blobs().items():
        stages = {e.stage: e for e in entries}
        print('Conflict:', path, 'stages:', list(stages.keys()))
```
Resolve by writing file then adding and committing.

## Worktrees (Multiple Checkouts)
```python
repo.git.worktree('add', '../wt-feature', 'feature')
# List
print(repo.git.worktree('list'))
# Remove
repo.git.worktree('remove', '../wt-feature')
```
Allows parallel builds or diff analysis across branches without cloning.

## Sparse Checkout (Large Monorepos)
```python
repo.git.sparse_checkout('init', '--cone')
repo.git.sparse_checkout('set', 'src/moduleA', 'libs/core')
```
Better run right after clone with `--filter=blob:none` for performance.

## Git LFS Note
GitPython sees pointer files unless LFS smudge filter runs. For raw large objects ensure environment has LFS installed; otherwise treat large binary diffs as skipped.

## Hooks
GitPython does not manage hooks directly. You can write to `.git/hooks/pre-commit` yourself; remember to set executable bit (on Unix) and avoid executing untrusted hook scripts programmatically.

## Large Repo Considerations
* Prefer shallow clones for analytics: depth=1.
* Use path filters in `iter_commits(paths=...)`.
* Avoid reading full blobs: check `blob.size` before `blob.data_stream.read()`.
* Cache computed diffs if generating multiple AI prompts.

## Commit Stats
```python
c = repo.head.commit
print(c.stats.total)        # {'insertions': X, 'deletions': Y, 'lines': Z}
print(c.stats.files['path/to/file.py'])  # per-file dict
```
Great for summarizing magnitude of changes.

## DiffIndex Entry Attributes
From `c1.diff(c2)` each entry `d` provides:
* `d.change_type` (A,M,D,R,T)
* `d.a_path`, `d.b_path`
* `d.a_blob`, `d.b_blob` (may be None)
* `d.renamed` boolean
* `d.score` (rename score)
  You can read blob contents: `d.b_blob.data_stream.read()`.

## Reflog (Recent HEAD Movements)
```python
print(repo.git.reflog('show', 'HEAD'))
```
Useful to recover lost commits (not a high-level API wrapper beyond raw git).

## Bisect (Automated Search)
GitPython lacks dedicated helpers; use raw commands:
```python
repo.git.bisect('start')
repo.git.bisect('bad')
repo.git.bisect('good', 'v1.0.0')
# run tests externally, then mark good/bad iteratively
repo.git.bisect('reset')
```
Automate by script that interprets test exit codes and calls good/bad accordingly.

## Patches (Format / Apply)
Generate patches:
```python
repo.git.format_patch('-1', 'HEAD')      # last commit patch file(s)
```
Apply patch:
```python
repo.git.apply('0001-some-change.patch')
```
For staged patch creation from index: `repo.git.diff('--cached', '-U0')` or `format_patch` after commit.

## Credentials & Auth
* HTTPS with PAT: embed token once then prefer credential helper.
* SSH: rely on ssh-agent outside GitPython.
* Avoid storing tokens in repo; pass via environment when constructing URLs.

## GPG / Signing
Signing controlled by git config (`commit.gpgsign`, `user.signingkey`). GitPython defers to underlying git; set config values then normal commits will be signed (if gpg available). No direct high-level wrapper.

## Thread / Process Safety
* Avoid sharing a single mutable `Repo` across threads for writes.
* For read-only analytics it's usually fine; create separate instances if in doubt.
* Heavy parallel history walks: pre-fetch commits list, then process in workers.

## AI Commit Message Integration Tips
* Pre-compress diffs: keep only changed line hunks plus 3 lines context.
* Provide per-file stats (insertions/deletions) to guide model focus.
* Include branch name + ahead/behind + scope inference (e.g., top-level dir names).
* Enforce conventional commit prefix heuristically before final save.

---

