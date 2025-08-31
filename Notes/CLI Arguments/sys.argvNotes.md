#  Notes `sys.argv` in Python

---

## 🔹 What is `sys.argv`?

* `sys.argv` is a **list of strings** in Python.
* It comes from the **command line** when you run a script.
* Always available if you `import sys`.

---

## 🔹 Key Points

1. `sys.argv[0]` → always the script name.
   Example: if you run `python cli.py gen`, then `sys.argv[0] == "cli.py"`.

2. `sys.argv[1:]` → everything after the script name.
   Example: `python cli.py gen -m "Fix bug"` →
   `sys.argv[1:] == ["gen", "-m", "Fix bug"]`

3. It’s just a **list**, so you can slice, loop, or check values.

---

## 🔹 Example 1: Inspect Arguments

```python
import sys

print("Raw sys.argv:", sys.argv)
print("Script name:", sys.argv[0])
if len(sys.argv) > 1:
    print("First arg:", sys.argv[1])
```

Run:

```bash
python cli.py hello world
```

Output:

```
Raw sys.argv: ['cli.py', 'hello', 'world']
Script name: cli.py
First arg: hello
```

---

## 🔹 Example 2: Simple Command Handling

```python
import sys

if len(sys.argv) < 2:
    print("Usage: python cli.py <command>")
    sys.exit(1)

command = sys.argv[1]

if command == "gen":
    print("Would generate commit message")
elif command == "diff":
    print("Would show staged diffs")
else:
    print("Unknown command:", command)
```

---

## 🔹 Example 3: Flags and Options

```python
import sys

if len(sys.argv) >= 3 and sys.argv[1] == "gen" and sys.argv[2] == "-m":
    message = " ".join(sys.argv[3:])
    print("Commit message is:", message)
else:
    print("Usage: python cli.py gen -m <message>")
```

Run:

```bash
python cli.py gen -m "Fix login bug"
```

Output:

```
Commit message is: Fix login bug
```

---

# ✅ Practice Tasks

### Task 1 – Echo arguments

Write a script that just prints every argument one by one using a loop.

Input:

```bash
python cli.py hello world test
```

Output:

```
Arg 1: hello
Arg 2: world
Arg 3: test
```

---

### Task 2 – Implement `gen`

* Run with: `python cli.py gen -m "Your commit message"`.
* Print: `Generated commit message: <message>`.

---

### Task 3 – Implement `diff`

* Run with: `python cli.py diff`.
* Print: `Showing staged diffs...` (later will connect to GitPython).

---

### Task 4 – Error handling

* If no args: print `"Usage: python cli.py <command>"`.
* If unknown command: print `"Unknown command: <name>"`.

---

# 🔑 Takeaway

* `sys.argv` = **manual argument parsing**.
* Good for **learning**, but for real tools → use **`argparse`** or **`click`**.

---