# Notes `argparse` in python

---
## What is argparse?

* argparse is a built-in Python module to handle command-line arguments.

* It makes your CLI tools easier to use and self-documenting (help messages).

* Instead of manually checking sys.argv, you declare arguments → parser handles them.
## 1. What does “parse” mean?

* *Parsing* = **reading text** (like `"gen -m Fix bug"`) and turning it into **structured data** Python can use.
* Example: `"python cli.py gen -m Fix bug"` → becomes:

  ```python
  {
    "command": "gen",
    "message": "Fix bug"
  }
  ```
* Without `argparse`, you would need to split the list from `sys.argv` manually.
* With `argparse`, the library does it for you + checks errors.

---

## 2. How to start using it

```python
import argparse

parser = argparse.ArgumentParser(description="My commit tool")
```

* `ArgumentParser` = the main object.
* `description` = text that shows when someone runs `--help`.

Run:

```bash
python cli.py --help
```

Output:

```
usage: cli.py [-h]
My commit tool
```

---

## 3. Adding arguments

### Positional (required, order matters)

```python
parser.add_argument("command", help="The command to run")
```

Run:

```bash
python cli.py gen
```

Now:

```python
args = parser.parse_args()
print(args.command)   # "gen"
```

---

### Optional (flags with `-` or `--`)

```python
parser.add_argument("-m", "--message", help="Commit message")
```

Run:

```bash
python cli.py -m "Fix bug"
```

Now:

```python
args.message   # "Fix bug"
```

⚡ Tip: Short flag = `-m`, long flag = `--message`. Both work.

---

## 4. Parsing the arguments

When you call:

```python
args = parser.parse_args()
```

* Python looks at what was typed in terminal.
* Matches them to the arguments you declared.
* Creates an object `args` with those values as attributes.

Example:

```bash
python cli.py gen -m "Fix login"
```

Becomes:

```python
args.command == "gen"
args.message == "Fix login"
```

---

## 5. Automatic help

You don’t need to code usage instructions yourself:

```bash
python cli.py --help
```

Shows:

```
usage: cli.py [-h] [-m MESSAGE] command
```

---

## 6. Restricting values

You can force only certain choices:

```python
parser.add_argument("--style", choices=["conventional", "simple"])
```

Run:

```bash
python cli.py gen --style invalid
```

Output:

```
error: argument --style: invalid choice: 'invalid'
```

---

## 7. Subcommands (like git commit, git diff)

You can make separate “subparsers” for each command.

```python
import argparse

parser = argparse.ArgumentParser(description="AI Commit Tool")
subparsers = parser.add_subparsers(dest="command")

# gen command
gen_parser = subparsers.add_parser("gen", help="Generate commit")
gen_parser.add_argument("-m", "--message", help="Custom commit message")

# diff command
diff_parser = subparsers.add_parser("diff", help="Show staged diffs")

args = parser.parse_args()

if args.command == "gen":
    print("Gen command, message:", args.message)
elif args.command == "diff":
    print("Diff command")
```

Run:

```bash
python cli.py gen -m "Add login"
python cli.py diff
```

---

## 8. Default values

```python
parser.add_argument("-s", "--style", default="conventional")
```

If not passed:

```python
args.style == "conventional"
```

---

# ✅ Practice Tasks

### Task 1 – Positional

* Add a **positional argument** called `name`.
* Run `python cli.py Basant` → prints `"Hello, Basant"`.
### DONE

---

### Task 2 – Optional flag

* Add `-n` or `--number` flag.
* Run `python cli.py -n 3` → prints `"You entered: 3"`.
### DONE

---

### Task 3 – Subcommands

* Add subcommands:

    * `gen` (with `-m` flag).
    * `diff` (no args).
* Run:

  ```bash
  python cli.py gen -m "Fix bug"
  python cli.py diff
  ```
### DONE

---

### Task 4 – Choices

* Add a `--style` argument with choices = `["simple", "conventional"]`.
* Run:

  ```bash
  python cli.py gen --style simple
  ```
#### DONE

---

### Task 5 – Mini Integration

* In the `diff` subcommand, instead of printing text, **call your GitPython function** to show staged diffs.

---

# 🔑 Big Takeaway

* `sys.argv` = raw list of strings (manual work).
* `argparse` = parses into structured object automatically.
* Subcommands make your CLI work like `git`.
* You get `--help` for free.
___

## Comparison: `sys.argv` vs `argparse`

| Feature                                        | `sys.argv`                                                                                                         | `argparse`                                                                                                                                       |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| **What it gives you**                          | Just a **list of strings** (raw input). Example: `['app.py', '--name', 'Basant', '--age', '21']`                   | A **parser object** that converts arguments into usable variables. Example: `Namespace(name='Basant', age=21)`                                   |
| **Parsing responsibility**                     | **You** must manually check each string, see if it matches `--name` or `--age`, then convert `"21"` to an integer. | `argparse` automatically matches flags (`--name`), assigns values, and even type-casts (`'21' → 21`).                                            |
| **Errors / Validation**                        | None built-in. If the user forgets `--age`, your program might crash or misbehave unless you code extra checks.    | Built-in. If the user forgets `--age` (when required), argparse shows a **helpful error**: `error: the following arguments are required: --age`. |
| **Help message (`-h`)**                        | Doesn’t exist unless you code it yourself.                                                                         | Automatically created: typing `python app.py -h` shows usage, arguments, descriptions.                                                           |
| **Complex features (choices, defaults, etc.)** | Must code by hand (long and error-prone).                                                                          | Built-in with one line: e.g., `parser.add_argument("--mode", choices=["fast", "slow"], default="fast")`.                                         |
| **When to use**                                | Super simple scripts where you only need maybe one or two arguments.                                               | Real applications, projects, or when you want reliability, validation, and clean help messages.                                                  |

---

## Side-by-side Example

### Using `sys.argv`

```python
import sys

# sys.argv is just a list of strings
args = sys.argv
print("Raw args:", args)

# Example: python app.py --name Basant --age 21
if "--name" in args:
    name_index = args.index("--name") + 1
    name = args[name_index]
else:
    name = None

if "--age" in args:
    age_index = args.index("--age") + 1
    age = int(args[age_index])  # manual conversion
else:
    age = None

print(f"Name: {name}, Age: {age}")
```

Output:

```
Raw args: ['app.py', '--name', 'Basant', '--age', '21']
Name: Basant, Age: 21
```

But notice how much **manual checking** you had to do.

---

### Using `argparse`

```python
import argparse

parser = argparse.ArgumentParser(description="Demo of argparse")
parser.add_argument("--name", required=True, help="Your name")
parser.add_argument("--age", type=int, required=True, help="Your age")

args = parser.parse_args()
print(f"Name: {args.name}, Age: {args.age}")
```

Now run:

```bash
python app.py --name Basant --age 21
```

Output:

```
Name: Basant, Age: 21
```

If you forget `--age`:

```
error: the following arguments are required: --age
```

If you type `-h`:

```
usage: app.py [-h] --name NAME --age AGE
Demo of argparse
```

---

✅ **Summary**:

* `sys.argv` = raw, manual, you do the parsing yourself.
* `argparse` = smarter, structured, with error handling, validation, and automatic help.

---