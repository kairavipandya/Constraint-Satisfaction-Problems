class CSP:
    def __init__(self, variables, domains, constraints, fc):
        self.variables = variables
        self.domains = {var: list(domain) for var, domain in domains.items()}
        self.constraints = constraints
        self.fc = fc
    
    def apply_inferences(self, inferences):
        for var, values in inferences.items():
            self.domains[var] = values

    def remove_inferences(self, inferences):
        for var, values in inferences.items():
            self.domains[var] = list(set(self.domains[var]) | set(values))

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

#psuedo code for backtracking
#function BACKTRACKING-SEARCH(sp) returns a solution or failure
def backtracking_search(csp):
    #return BACKTRACK(csp, {})
    return backtrack(csp, {})
#function BACKTRACK(sp, assignment) returns a solution or failure
def backtrack(csp, assignment, depth=0):
    #if assignment is complete then return assignment
    if is_complete(csp, assignment):
        print_assignment(csp, assignment, 'solution')
        return assignment
    #var - SELECT-UNASSIGNED-VARIABLE(csp, assignment)
    var = select_unassigned_variable(csp, assignment)
    #for each value in ORDER-DOMAIN-VALUES(sp, var, assignment)
    for value in order_domain_values(csp, var, assignment):
        assignment_copy = assignment.copy()
        assignment_copy[var] = value
        #if value is consistent with assignment then
        if is_consistent(var, value, assignment, csp.constraints):
            #add {var = value } to assignment
            assignment[var] = value
            #inferences - INFERENCE(csp, var, assignment)
            inferences = forward_checking(csp, var, value, assignment) if csp.fc else {}
            #if inferences ‡ failure then
            if inferences != 'failure':
                #add inferences to csp
                result = backtrack(csp, assignment, depth+1)
                #if result + failure then return result
                if result != 'failure':
                    return result
                #remove inferences from csp
                csp.remove_inferences(inferences)
            del assignment[var]
        #remove {var = valu} from assignment
        else:
            print_assignment(csp, assignment, 'failure')
    if depth == 0:
        print('failure')
    #return failure
    return 'failure'

def is_complete(csp, assignment):
    return len(assignment) == len(csp.variables) and all(is_consistent(var, assignment[var], assignment, csp.constraints) for var in assignment)

def select_unassigned_variable(csp, assignment):
    unassigned_vars = [v for v in csp.variables if v not in assignment]
    return min(unassigned_vars, key=lambda var: len(csp.domains[var]))

def order_domain_values(csp, var, assignment):
    return sorted(csp.domains[var])

def is_consistent(var, value, assignment, constraints):
    for v1, op, v2 in constraints:
        if v1 == var and v2 in assignment:
            op_for_eval = '==' if op == '=' else op
            if not eval(f"{value} {op_for_eval} {assignment[v2]}"):
                return False
        elif v2 == var and v1 in assignment:
            op_for_eval = '==' if op == '=' else op
            if not eval(f"{assignment[v1]} {op_for_eval} {value}"):
                return False
    return True

def forward_checking(csp, var, value, assignment):
    inferences = {}
    for (v1, op, v2) in csp.constraints:
        if var in (v1, v2) and not is_consistent(var, value, assignment, [(v1, op, v2)]):
            return 'failure'
        if var in (v1, v2):
            other_var = v2 if v1 == var else v1
            if other_var not in assignment:
                inferences[other_var] = [val for val in csp.domains[other_var] if is_consistent(other_var, val, {**assignment, var: value}, [(v1, op, v2)])]
                if not inferences[other_var]:
                    return 'failure'
    csp.apply_inferences(inferences)
    return inferences

def print_assignment(csp, assignment, result):
    sorted_assignment = sorted(assignment.items(), key=lambda item: csp.variables.index(item[0]))
    assignments_str = ', '.join(f'{var}={value}' for var, value in sorted_assignment)
    print(f'{assignments_str} {result}')


def main(var_file, con_file, fc_option):
    variables, domains = read_var_file(var_file)
    constraints = read_con_file(con_file)
    csp = CSP(variables, domains, constraints, fc_option == 'fc')
    solution = backtracking_search(csp)
    if solution == 'failure':
        print('No solution found.')

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python main.py <var_file> <con_file> <none|fc>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
