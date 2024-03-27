# Constraint-Satisfaction-Problems

This Python script implements a Constraint Satisfaction Problem (CSP) solver with backtracking search and optional forward checking.

**Features:**

- Solves CSPs with variables, domains, and constraints.
- Supports equality (`=`), inequality (`!=`), greater-than (`>`), and less-than (`<`) constraints.
- Uses Minimum Remaining Values (MRV) heuristic for variable selection.
- Implements Least Constraining Value (LCV) heuristic for value selection (optional).
- Offers forward checking for improved efficiency (optional).

**Requirements:**

- Python 3.x

**Usage:**

```
python csp.py <var_file> <con_file> <consistency (none|fc)>
```

- `<var_file>`: Path to the file containing variables and their domains (one line per variable, format: `variable: domain_value1 domain_value2 ...`).
- `<con_file>`: Path to the file containing constraints (one line per constraint, format: `variable1 operator variable2`).
- `<consistency>`: Consistency enforcing procedure (`none` for backtracking only, `fc` for forward checking).

**Output:**

The program prints the branches visited in the search tree, represented by variable assignments, until a solution is found or a dead end is reached. Each assignment is printed as a comma-separated list of `variable=value` pairs.

**Example:**

```
python csp.py ex1.var ex1.con fc
```

This command might output (depending on the content of the files):

```
F=1, E=1, D=1, A=5, B=2, C=2  solution
```

```
python csp.py ex1.var1 ex1.con none
```

**Note:**

- The program does not handle invalid operators or file formats.

**Optional Forward Checking:**

- Forward checking is enabled by specifying `fc` as the consistency argument.
- It enforces arc consistency during preprocessing, potentially reducing search spac
