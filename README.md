# json-o-sql
(Learning project)
A Python-based JSON document store with SQL-like query operations. Processes JSON files using Python logic, mapped from SQL syntax, with a FastAPI interface.

<img width="589" height="287" alt="image" src="https://github.com/user-attachments/assets/187c6b6e-1f43-44c9-b4a6-cb35a38f963e" />

---
### Core Engine (`src/engine.py`)

The `JSONDB` class wraps a JSON file and provides CRUD operations using Python dictionaries to express SQL-like conditions.

**How Conditions Work**

A condition is a nested dict: `{"column": {">": value}}`. The outer key is the column name, the inner key is the operator.

```python
# condition dict structure
{"age": {">": 20}, "status": {"==": "active"}}
# col="age",  condition={">": 20}
# col="status", condition={"==": "active"}
```

`is_valid` iterates nothing -- it destructures the single operator-value pair from the inner dict and runs it through Python's `match`/`case`:

```python
sign, rhs = list(condition.items())[0]   # unpacks ">" and 20
match sign:
    case "<":  return obj[col] < rhs
    case "==": return obj[col] == rhs
    # ...
```

Each `case` is a direct Python comparison. No string eval, no `eval()`. If `obj[col]` is `None` (missing key) it short-circuits to `False`.

**How `select_where` Filters and Projects**

A single list comprehension with a guard does both jobs:

```python
return [
    {k: obj.get(k) for k in selected_columns if k in obj}
    for obj in data
    if all(
        self.is_valid(obj, col, condition)
        for col, condition in conditions.items()
    )
]
```

`all()` iterates every `(col, condition)` pair from the conditions dict. If every `is_valid` returns `True`, the outer comprehension keeps the row and projects only the requested columns into a new dict. `select_all` is the same but skips both the guard and the projection.

**How `update_where` Mutates In Place**

```python
for obj in data:
    if all(self.is_valid(obj, col, condition) for col, condition in conditions.items()):
        for key, val in new_vals:
            obj[key] = val
```

A forward loop over the list mutates matching dicts directly. After the loop, the file is rewritten:

```python
f.seek(0)
f.truncate()
json.dump(data, f, indent=4)
```

`seek(0)` moves the cursor to the start, `truncate()` drops any leftover bytes from the previous write, then `dump` serialises the whole list.

**How `delete_where` Builds a New List**

Uses the same `all` + `is_valid` pattern but negated with `not`:

```python
new_data = [
    obj for obj in data
    if not all(self.is_valid(...))
]
```

Rows that fail the condition get kept. Then the same seek/truncate/dump cycle replaces the file.

**How `insert` Appends**

Reads the full list, `data.append(obj)` adds the new row, writes everything back. Same atomic-write pattern.

**File I/O Pattern**

All write operations follow the same sequence:

1. Open with `"r+"` (read + write, no truncation on open)
2. `json.load(f)` reads the full array into memory
3. Modify the Python list/dicts in place
4. `f.seek(0)` to rewind
5. `f.truncate()` to clear stale data
6. `json.dump(data, f, indent=4)` to persist

---



