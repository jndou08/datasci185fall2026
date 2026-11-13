# DATASCI 185 Quiz Study Guide: OOP and Pandas

## OOP

**self, cls, and bare names**
- `self.x` is an attribute of this object. A bare `x` is a parameter or local variable.
- Don't write `self.days_late` if `days_late` is only a parameter of the method.
- Don't write `self.self.x`.
- `cls.x = value` changes a class variable for every instance (class methods only).
- In a class method, never set attributes on `cls` as scratch variables. Use plain locals, then `return cls(...)`.

**Class variables**
- Define them in the class body, outside any method (`bonus_rate = 0.10`).
- Read them inside methods with `self.bonus_rate`.
- Change them only through a `@classmethod` that sets `cls.bonus_rate = value`.

**Inheritance**
- `class Child(Parent):` inherits everything.
- To override, define a method with the same name.
- An inherited method that calls `self.set_x(...)` automatically uses the child's override.

**Asserts**
- Copy the message text exactly from the spec.
- Read the bounds carefully: "0 or more" means `>= 0`, not `> 0`.
- Check the value **before** changing the object. Compute the total first, then assert, then set.

**Methods that change vs. return**
- A mutating method (like `extend`) changes `self` and returns nothing.
- `__add__` must `return` a **new** object and leave both originals alone.
- A function with no `return` gives back `None`. This is the cause of a surprise `None`.

**Dunder methods**
- `print(obj)` uses `__str__`. Showing an object alone in a cell uses `__repr__`.
- `__add__`, `__lt__` and `__eq__` take `(self, other)` and compare or combine the two objects' attributes.

**Class method as an alternative constructor**
```python
@classmethod
def from_minutes(cls, total):
    return cls(total // 60, total % 60)
```

**Loops over objects**
- Counter: start at 0 and use `count += 1`. `sum + x` without `=` does nothing.
- Running best: keep the best object so far and compare each object to it.
- Pairing with a nested loop: the inner loop is `range(i + 1, n)`. Skip anyone already paired. Pair with the **first** match, then `break`.
- Building objects from a dict: `for name in d.keys(): self.items.append(Cls(name, d[name]))`.

## Pandas

**Selecting**
- `.iloc[rows, cols]` is stop-exclusive, so `0:3` gives rows 0, 1, 2.
- Get a column position with `list(enumerate(df.columns))`. The order of the list you pass is the order of the output columns.
- Boolean mask: `df.loc[df["year"] == 1980, "col"]`.
- `.query("`Col Name` == @var and Other >= @n")`: backticks for names with spaces, `@` for Python variables.
- After `.query()`, add `.copy()` before adding columns, to avoid `SettingWithCopyWarning`.

**New columns**
- Single-column `.apply(func)` passes one value at a time.
- For two columns, use element-wise arithmetic: `df["w"] / (df["h"] / 100) ** 2`. Mind the parentheses.
- Sort: `.sort_values("col", ascending=False)`, then `.iloc[0:3, [..]]`.

**Cleaning and recoding**
- Text to numbers: `pd.to_numeric(df["col"], errors="coerce")`. Bad entries become `NaN`.
- Groups: `pd.cut(df["col"], bins=[0, 90, 130, 250], right=True, labels=[...])`. Values outside the bins, and `NaN`, stay `NaN`.
- Merge: `pd.merge(left=a, right=b, how="left", on="key")`. A left merge keeps every row of `a`; rows with no match get `NaN`.

**Plots**
- Overlay: two `plt.hist(..., alpha=0.5, label="...")` calls, then `plt.legend()`.
- Always label both axes and add a title.
- Check that the labels match the right series.

## Debug checklist

| Error | Usual cause |
|---|---|
| `AttributeError: ... no attribute 'x'` | Wrote `self.x` for a parameter, or `self.self.x` |
| `KeyError: 'col'` | The column was never added to this DataFrame, `read_csv` was re-run, or the name is misspelled |
| `NameError` | A variable used outside the loop or method that defined it |
| `SyntaxError ... augmented assignment` | `f() += 1`. Call the setter method instead |
| Output shows `None` | The method or function has no `return` |
| Output is a number, not an object | `__add__` returned a number, not a new object |
| Only the first error line shows | Put each failing line in its own cell |