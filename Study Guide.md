# Quiz Study Guide: Lectures 9-12 and Lab 5

## 0. Read-before-you-submit checklist

1. **Copy every output string exactly.** Check each word, space, symbol (`°F`) and rounding against the example. Use `{variable}` in the f-string, not a typed-in value.
2. **Does the prompt say "returns" or "prints"?** Returns means `return`. Print only what is asked.
3. **Boundary words:** "at least" is `>=`, "more than" is `>`, "keyword-only" needs `*`, "start from the first item" means no made-up starting number.
4. **Accumulators** (running max or min, totals, counters) are set **before** the loop. **Per-iteration** things (a list or total for one group) are reset **inside** the loop.
5. **The name in the `for` line must match the name in the body.** A leftover global can hide the mistake.
6. **Print or show the final answer.** The grader can't see a computed value you never printed.
7. **Don't overwrite your data.** Store `.apply()` results in a new variable or column.
8. **Test the other cases:** the first item, the last item, a single item, and an item that fails.

---

## 1. Lecture 9: Dictionaries

```python
scores = {"Abed": 3.24, "Britta": 1.51}   # key : value
scores["Abed"]                 # look up -> 3.24
scores["Jeff"] = 0.51          # add a new key
scores["Abed"] = 2.51          # change an existing value
scores["Abed"] += 2            # update using the current value
scores.keys(); scores.values() # look like lists but aren't
list(scores.keys())            # real list (needed for random.shuffle)
for key in scores.keys():      # same as: for key in scores:
    print(key, scores[key])
```

**Nested dictionary (two-step lookup, left to right):**
```python
study_group = {"Abed": {"month": "March", "day": 23, "year": 2007}}
study_group["Abed"]["year"]       # 2007
study_group["year"]["Abed"]       # KeyError (wrong order)
for name in study_group.keys():
    year = study_group[name]["year"]
```

- A missing key raises `KeyError`. Wrong case (`"abed"`) and a missing quote (`Abed`) are the usual causes.
- `random.shuffle(lst)` needs a list, changes the list in place and returns nothing. It does not change the dictionary.
- **Dictionary of lists to DataFrame.** The keys become column names, and every list must be the same length.
```python
df = pd.DataFrame({"name": names, "pay": pays}); display(df)
```

**Running max (swap `>` for `<` and `0` for a big number for a running min):**
```python
best_score = 0
best_name = "nobody"
for key in d.keys():
    if d[key] > best_score:
        best_score = d[key]    # update BOTH variables together
        best_name = key
```
- Check the score with `np.max(list(d.values()))`.
- Start at 0 only if every value is above 0. Otherwise start from the first item.

**Per-group averages (nested dictionary):**
```python
for course in courses.keys():
    total = 0                  # reset for each course
    for student in courses[course].keys():
        total += courses[course][student]
    avg = total / len(courses[course])
```

---

## 2. Lecture 10: Functions

```python
def quadratic_formula(a, b, c):
    discriminant = b**2 - 4*a*c
    ...
    return x_plus, x_minus          # several values -> a tuple

root1, root2 = quadratic_formula(2, -4, -30)   # unpack in order
quadratic_formula(a=2, b=-4, c=-30)             # keywords are allowed
```

- The names of your inputs and of the variables you save results into **don't matter**. Only the order does (for positional calls).
- **No `return` means the function gives back `None`.** Printing inside the function does not give you a usable value, and `check + 1` then crashes.
- **Local vs global:**
  - Variables created inside a function don't exist outside it (`NameError`).
  - A function **can read** a global (such as `lab_partners`), but it's best to use only local variables.
  - A function can't change a number outside it. To "update" one, return it and reassign: `count = add_one(count)`.
- `return` ends the function immediately, so it also leaves any loop inside it.
- Many different function bodies can be equivalent. Watch parentheses: `x/(2*a)` is not `x/2*a`.

---

## 3. Lecture 11: lambda, `.apply()`, no-output functions

```python
fn = lambda x, y, z: x + y + z                 # one line; no "return" word
fn2 = lambda x, y, z: (x + y + z, y - z)       # two outputs need parentheses
is_pass = lambda g: g >= 55                    # can return True/False
curve = lambda g: round(10 * np.sqrt(g), 1)
```

`.apply()` runs a function on every entry of a column and returns a **Series**:
```python
new = df["grade"].apply(curve)
new.name = "curved_grade"                      # set .name EXACTLY as requested
n_pass = df["grade"].apply(is_pass).sum()      # True counts as 1, so .sum() counts them
```
- Print or `display` the result when asked.
- Storing in a new column keeps the old one: `df["level"] = df["pay"].apply(pay_level)`.
- `if`/`elif`/`else` inside a function: put the strictest condition first.

**Functions with no output** (like a plotting function) have no `return`, and you don't assign the call to anything.
```python
def labeled_bar_plot(x_vals, heights, xlabel, ylabel, title):
    plt.bar(x=x_vals, height=heights); plt.xlabel(xlabel); ...; plt.show()
```

**Functions can change their input:**
- `lst.append(...)` and `lst[-1] = ...` change the caller's list.
- `lst = lst + ["New!"]` does **not**, because it rebinds a local name.
- An integer NumPy array silently truncates: assigning `0.1` stores `0`. Use `dtype=np.float64`.

---

## 4. Lecture 12: Errors, `try`/`except`, `input()`

**Three kinds of mistakes:**
- **Syntax error:** nothing runs (missing `:` or `)`).
- **Runtime error:** runs partway, then stops with a traceback.
- **Silent error:** runs fine and gives a wrong answer. These are the dangerous ones.

**Traceback:** read from the bottom up. The last line gives the error type and message, and the line above it is the code that failed.

| Error | Usually means |
|---|---|
| `SyntaxError` / `IndentationError` | typo, or a misaligned block |
| `NameError` | misspelled variable, or a local variable used outside its function |
| `KeyError` | key not in the dictionary |
| `IndexError` | position doesn't exist (a loop one step too far) |
| `TypeError` | mixing types, e.g. `"Todd" + 9.99`, or `None + 1` |
| `ValueError` | right type, impossible value, e.g. `float("nine")` |
| `ZeroDivisionError` | dividing by a count that is 0 |

A **warning** (e.g. `RuntimeWarning` giving `nan`) doesn't stop the code, but the result is garbage.

```python
try:
    total += prices[item] * int(order[item])   # whole calculation inside try
except KeyError:
    print(f"Sorry, we don't sell {item}")
except ValueError:
    print(f"Sorry, {order[item]} isn't a valid quantity")
```
- **Name the error you expect.** A bare `except:` also swallows your own typos and prints a confident wrong message.
- **Never write `except: pass`.** It hides skipped items. Print a message or count the skips.
- Put the whole calculation in the `try`, so a failure changes nothing.
- Define `total` and `count` before the loop.
- Check `count == 0` before dividing.
- Use `if` when you can list the bad cases in advance, and `try` when you can't.

**`input()` always returns a string.** Convert it at once, `int(input(...))` or `float(input(...))`.
```python
while True:
    typed = input("Choose N: ")
    try:
        N = int(typed)
    except ValueError:
        print(typed, "is not a whole number."); continue   # ask again
    if N < 0 or N > 49:                                    # check the VALUE too
        print(N, "is out of range."); continue
    break                                                  # or `return N` inside a function
```
- `continue` jumps back to the top of the loop. `break` leaves it.

**Raise your own error:** `raise ValueError(f"{name} is not one of the 50 candidates.")`

**Silent-error examples to remember:**
- A running max that never updates `best_skill` reports `0`. Any impossible number is a clue.
- `season_of`: `"March"` is in both the Winter and Spring lists, so the `elif` never runs for March.

---

## 5. Lab 5: `*`, `*args`, `**kwargs`

```python
def birthday(month, day, *, name=None):    # name is KEYWORD-ONLY
    ...
birthday("June", 20, name="Peter")         # works
birthday("June", 20, "Peter")              # TypeError
def birthday(*, month, day, name=None):    # EVERYTHING keyword-only
birthday("June", 20)                       # TypeError: takes 0 positional arguments
birthday(month="June", 20)                 # SyntaxError: positional follows keyword
```
- The `*` goes before the keyword-only parameters, and parameters before it stay positional-or-keyword.
- **`*args`** collects extra positional arguments into a **tuple**.
  - It accepts any types.
  - It has length 0 when nothing is passed, so `args[3]` raises `IndexError` if there are fewer than four.
  - Guard with `if len(args) >= 4:`.
- **`**kwargs`** collects keyword arguments into a **dictionary**.
  - Use `'name' in kwargs` and `kwargs['name']`.
  - It is `{}` when nothing is passed.
  - Unused keywords are accepted silently.
- **Testing two keys:** `if 'name' in kwargs and 'major' in kwargs`. Writing `'name' and 'major' in kwargs` only tests `'major'`.
- `args` and `kwargs` are just conventions. The `*` and `**` are what matter.
- **`print(*args, sep=' ', end='\n')`:** `sep="-"` changes the separator, while passing `"-"` as another argument adds it as an item.
- `make_plot(*args)` chooses `plt.hist` (1 argument) or `plt.bar` (2 arguments) with `len(args)`.
- **Final check:**
  - `def f1(*, x, y)` is `*`.
  - `def f2(*values)` is `*args`.
  - `def f3(**options)` is `**kwargs`.

---

## 6. Templates to copy

```python
# count with a counter
count = 0
for key in d.keys():
    if d[key] >= 500:          # "at least" -> >=
        count += 1
print(f"{count} people earned at least 500")

# simulation: new list per group, record the group value (not the trial index)
best_error = 1000; best_n = 0
for n in [10, 100, 1000]:
    errors = []                          # inside: resets for each n
    for trial in range(200):
        errors.append(abs(heads_fraction(n) - 0.5))
    avg_error = np.mean(errors)
    if avg_error < best_error:           # best_ variables set BEFORE the loop
        best_error = avg_error
        best_n = n                       # n, not the trial counter

# running max AND min need two separate `if`s (not `elif`)
first = list(prices.keys())[0]
low = high = prices[first]
low_item = high_item = first
for item in prices.keys():
    if prices[item] < low:  low = prices[item];  low_item = item
    if prices[item] > high: high = prices[item]; high_item = item
```

- `round(x, 2)` prints `200.0`, not `200.00`. That's fine unless the prompt demands two decimals.
- `f"{x:.2f}"` gives `200.00`, but it wasn't taught in the lectures.

---

## 7. Mistakes to avoid

| Mistake | Fix |
|---|---|
| Printing inside a function that should return | `return` the value, then print outside |
| Typing `Monday` into an f-string inside a loop | use `{day}` |
| Missing or extra words and spaces in a printed line | copy the example string exactly |
| `elif` for two independent checks (max and min) | use two separate `if`s |
| Initializing `best_*` inside the loop | set it before the outer loop |
| Not resetting a per-group list or total | create it inside the loop |
| `for key in ...` but the body uses `item` | use one name throughout |
| `amount` or `total` not set when an error happens early | do the math inside the `try` |
| Missing `*` in a keyword-only signature | `def f(a, b, *, flag=False)` |
| `.name = "curved grade"` | the string must match exactly (`"curved_grade"`) |
| Computing a count but never printing it | print the sentence the prompt asks for |
| `df = df["col"].apply(...)` replaces your DataFrame | store it in a new variable or column |
| Bare `except:` | name the error, e.g. `except ValueError:` |
| `>` when the prompt says "at least" | `>=` |