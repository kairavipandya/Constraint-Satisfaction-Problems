# CSP solver using backtracking and forward checking for AI class assignment

# CSP representation
class CSP:
    def __init__(self, variables, domains, constraints, fc):
        self.variables = variables
        self.domains = {var: list(domain) for var, domain in domains.items()}  # Copy the domains
        self.constraints = constraints
        self.fc = fc

    def apply_inferences(self, inferences):
        for var, values in inferences.items():
            self.domains[var] = values

    def remove_inferences(self, inferences):
        for var, values in inferences.items():
            self.domains[var] = list(set(self.domains[var]) | set(values))  # Revert domains to their original state

# Function to read the .var file
def read_var_file(var_file):
    variables, domains = [], {}
    with open(var_file, 'r') as file:
        for line in file:
            var, vals = line.strip().split(': ')
            domains[var] = [int(val) for val in vals.split()]
            variables.append(var)
    return variables, domains

def read_con_file(con_file):
    constraints = []
    with open(con_file, 'r') as file:
        for line in file:
            parts = line.strip().split()
            var1, op, var2 = parts[0], parts[1], parts[2]
            constraints.append((var1, op, var2))
    return constraints

# Backtracking search algorithm
def backtracking_search(csp):
    return backtrack(csp, {})

# Helper function for the backtracking search
def backtrack(csp, assignment):
    if is_complete(csp, assignment):
        return assignment
    var = select_unassigned_variable(csp, assignment)
    for value in order_domain_values(csp, var, assignment):
        if is_consistent(var, value, assignment, csp.constraints):
            assignment[var] = value
            inferences = forward_checking(csp, var, value, assignment) if csp.fc else {}
            if inferences != 'failure':
                result = backtrack(csp, assignment)
                if result != 'failure':
                    return result
                csp.remove_inferences(inferences)
            del assignment[var]
    return 'failure'

# Checks if the current assignment is complete
def is_complete(csp, assignment):
    return set(assignment.keys()) == set(csp.variables)

# Selects the next variable to assign
def select_unassigned_variable(csp, assignment):
    unassigned_vars = [v for v in csp.variables if v not in assignment]
    return min(unassigned_vars, key=lambda var: len(csp.domains[var]))

# Orders the domain values for a given variable
def order_domain_values(csp, var, assignment):
    return sorted(csp.domains[var])

def is_consistent(var, value, assignment, constraints):
    for v1, op, v2 in constraints:
        if v1 == var and assignment.get(v2) is not None:
            # Replace '=' with '==' for evaluation
            op_for_eval = '==' if op == '=' else op
            expression = f"{value} {op_for_eval} {assignment[v2]}"
            print(f"Evaluating expression: {expression}")
            if not eval(expression):
                return False
        elif v2 == var and assignment.get(v1) is not None:
            # Replace '=' with '==' for evaluation
            op_for_eval = '==' if op == '=' else op
            expression = f"{assignment[v1]} {op_for_eval} {value}"
            if not eval(expression):
                return False
    return True

# Applies forward checking to reduce domains
def forward_checking(csp, var, value, assignment):
    inferences = {}
    for (v1, op, v2) in csp.constraints:
        if var in (v1, v2) and not is_consistent(var, value, assignment, [(v1, op, v2)]):
            return 'failure'  # Inconsistent assignment
        if var in (v1, v2):
            other_var = v2 if v1 == var else v1
            if other_var not in assignment:
                inferences[other_var] = [val for val in csp.domains[other_var] if is_consistent(other_var, val, {**assignment, var: value}, [(v1, op, v2)])]
                if not inferences[other_var]:  # Empty domain means failure
                    return 'failure'
    csp.apply_inferences(inferences)
    return inferences

# Main function to run the CSP solver
def main(var_file, con_file, fc_option):
    variables, domains = read_var_file(var_file)
    constraints = read_con_file(con_file)
    csp = CSP(variables, domains, constraints, fc_option == 'fc')
    solution = backtracking_search(csp)
    if solution != 'failure':
        print(' '.join(f'{var}={value}' for var, value in sorted(solution.items())) + ' solution')
    else:
        print('failure')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <var_file> <con_file> <none|fc>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
