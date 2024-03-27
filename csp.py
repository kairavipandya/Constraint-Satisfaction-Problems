from collections import defaultdict

class CSP:
    def __init__(self, var_file, con_file, consistency):
        self.variables = self.__parse_var_file(var_file)
        self.constraints = self.__parse_con_file(con_file)
        self.consistency = consistency
        self.assignment = {}

    def __parse_var_file(self, filename):
        variables = {}
        with open(filename, 'r') as f:
            for line in f:
                var, domain = line.strip().split(':')
                variables[var] = [int(x) for x in domain.split()]  # Correct domain parsing
        return variables

    def __parse_con_file(self, filename):
        constraints = []
        with open(filename, 'r') as f:
            for line in f:
                var1, op, var2 = line.strip().split()
                if op == "!": op = "!="  # Adjusting inequality operator
                constraints.append((var1, op, var2))
        return constraints

    def is_consistent(self, var, value, assignment):
        for (var1, op, var2) in self.constraints:
            if var1 == var and var2 in assignment:
                if not self.__eval_constraint(op, value, assignment[var2]):
                    return False
            if var2 == var and var1 in assignment:
                if not self.__eval_constraint(op, assignment[var1], value):
                    return False
        return True

    def __eval_constraint(self, op, val1, val2):
        if op == '=':
            return val1 == val2
        elif op == '!=':
            return val1 != val2
        elif op == '>':
            return val1 > val2
        elif op == '<':
            return val1 < val2

    def select_unassigned_variable(self, assignment):
        # Implementing Most Constrained Variable Heuristic
        unassigned_vars = [v for v in self.variables.keys() if v not in assignment]
        return min(unassigned_vars, key=lambda var: (len(self.variables[var]), var))

    def order_domain_values(self, var, assignment):
        # Implementing Least Constraining Value Heuristic
        # This simple implementation does not fully realize LCV, should be extended
        return sorted(self.variables[var], key=lambda val: self.count_conflicts(var, val, assignment))

    def count_conflicts(self, var, value, assignment):
        # Count how many conflicts adding {var: value} would cause
        count = 0
        for constraint in self.constraints:
            var1, op, var2 = constraint
            if var1 == var and var2 in self.variables and var2 not in assignment:
                for val2 in self.variables[var2]:
                    if not self.__eval_constraint(op, value, val2):
                        count += 1
            elif var2 == var and var1 in self.variables and var1 not in assignment:
                for val1 in self.variables[var1]:
                    if not self.__eval_constraint(op, val1, value):
                        count += 1
        return count

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            self.print_assignment(assignment)
            return True
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                if self.backtrack(assignment):
                    return True
                assignment.pop(var)
        return False

    def print_assignment(self, assignment):
        print(', '.join(f"{var}={assignment[var]}" for var in sorted(assignment.keys())) + " solution")

    def solve(self):
        if not self.backtrack(self.assignment):
            print("No solution found.")

def main(var_file, con_file, consistency):
    csp = CSP(var_file, con_file, consistency)
    csp.solve()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python csp_solver.py <var_file> <con_file> <consistency>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
