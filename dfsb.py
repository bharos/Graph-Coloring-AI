import sys
import copy
import math
import time
class CSP:
    def __init__(self, mode, firstLine, inputLines ):

        self.start_time = time.time()
        self.FAILURE = False
        self.SUCCESS = True
        self.mode = mode
        self.constraints = inputLines
        self.varNums = int(firstLine[0])
        self.variables = [v for v in range(int(firstLine[0]))]
        self.neighbors = {key:[] for key in range(0,int(firstLine[0]))}
        self.domains = {key: [i for i in range(0,int(firstLine[2]))] for key in range(0, int(firstLine[0]))}
        self.currentDomain = {key: [i for i in range(0, int(firstLine[2]))] for key in range(0, int(firstLine[0]))}
    #    print(self.currentDomain)

        for arc in inputLines:
            self.neighbors[int(arc[0])].append(int(arc[1]))
            self.neighbors[int(arc[1])].append(int(arc[0]))


        #    print(self.domains)

        #    print(self.neighbors)

def minimum_remaining_values(csp, unassigned_vars):

    minimum = math.inf
    for v in unassigned_vars:
        if minimum > len(csp.currentDomain[v]):
            minimum = len(csp.currentDomain[v])

    minimum_vars = [v  for v in unassigned_vars if len(csp.currentDomain[v]) == minimum]

    if __debug__:
        print("minimum_vars = ",end=" ")
        print(minimum_vars)

    maxDegree = -1
    max_degree_var = -1
    for v in minimum_vars:
        if len(csp.neighbors[v]) > maxDegree:
            maxDegree = len(csp.neighbors[v])
            max_degree_var = v

    return max_degree_var




def select_unassigned_variable(assignment,csp):

    if csp.mode == '1':
        # First unassigned variable
        for var in range(csp.varNums):
            if var not in assignment:
                return var
    else:
            unassigned_vars = [v for v in csp.variables if v not in assignment]
            mrv_var = minimum_remaining_values(csp, unassigned_vars)
            if __debug__:
                print(mrv_var)



            return mrv_var

def order_domain_values(var, assignment, csp):
    if mode == '1':
        if len(csp.currentDomain) == 0:
            return csp.domains[var]
        return csp.currentDomain[var]

    if mode=='2':
        # If mode 2, then return least conflicting value

        lcv_dict = {key:0 for key in csp.currentDomain[var]}

        #Count each domain colors occuring in neighbor, and increment it in lcv_dict if it is a conflict
        for neighbor in csp.neighbors[var]:
            #check each value in current domain of the variable in neighbor's domain
            for value in csp.currentDomain[var]:
                if value in csp.currentDomain[neighbor]:
                    #when value is found in neighbor, increment its count in lcv_dict
                    lcv_dict[value] = lcv_dict[value]+1

     #   print(lcv_dict)

        #get the least conflicting value
        lcv = []
     #   print(lcv_dict)
        lcv = sorted(lcv_dict, key=lcv_dict.get)

      #  print('var = '+str(var)+' lcv = ',end="")
      #  print(lcv)
        return [key for key in lcv]


def revise_values(csp, Xi, Xj):
    revised = False
#    print("Xi = "+str(Xi)+ "Xi domain = ",end=" ")
 #   print(csp.currentDomain[Xi])
  #  print("Xj = "+str(Xj)+ " Xj domain = ", end=" ")
   # print(csp.currentDomain[Xj])
    if len(csp.currentDomain[Xj]) == 1 and csp.currentDomain[Xj][0] in csp.currentDomain[Xi]:
    #        print("Remove "+str(csp.currentDomain[Xj][0]))
            csp.currentDomain[Xi].remove(csp.currentDomain[Xj][0])
            revised = True

    return revised


def AC3(csp,queue):
    while len(queue) > 0:
        (Xi, Xj) = queue.pop(0)
        if revise_values(csp, Xi, Xj):
            if len(csp.currentDomain[Xi]) == 0:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk == Xj:
                    continue
                queue.append((Xk, Xi))
    return True

def is_consistent(csp, var, val, assignment):
    #for each neighbor in the list of neighbors for the current variable,
    for neighbor in csp.neighbors[var]:
        #if the neighbor has an assignment,
        if neighbor in assignment:
            #check if it has consistent value
            if val == assignment.get(neighbor, None):
                return False

    return True

counter = 0
def recursive_backtrack(assignment,csp):
        global counter
        counter+=1
        print("Recursive_backtrack")
    #    print("In recursive_backtrack")


        #check if assignment has a value for all the variables
        if len(assignment) == csp.varNums:
            return assignment

        var = select_unassigned_variable(assignment, csp)
      #  print("variable = "+str(var))
        domain_values = copy.deepcopy(order_domain_values(var, assignment, csp))
      #  print(domain_values)
        for  value in domain_values:
     #     print("Trying value "+str(value)+" on variable "+str(var))
          if is_consistent(csp,var,value,assignment):
              assignment[var] = value
              result = recursive_backtrack(assignment, csp)
              if result != csp.FAILURE:
                  return result
              #if not success remove the current variable assignment
              del assignment[var]

        return csp.FAILURE


def backtrack_order_AC3(assignment, csp):
    global  counter
    counter+=1
    #if __debug__:
  #  print("In backtrack + Order & AC3")
    # check if assignment has a value for all the variables
    if len(assignment) == csp.varNums:
        return assignment
    var = select_unassigned_variable(assignment,csp)

    #print("variable = " + str(var))
    domain_values = copy.deepcopy(order_domain_values(var, assignment, csp))
  #  print(domain_values)
    backup_domain = copy.deepcopy(csp.currentDomain)
    for value in domain_values:
       # print("Trying value " + str(value) + " on variable " + str(var))
        if is_consistent(csp, var, value, assignment):
            assignment[var] = value
        #    if __debug__:
            print("Assignment : ",end = " ")
            print(assignment)
            csp.currentDomain[var] = [value]
            #Perform Arc Consistency
            inference = AC3(csp,[(Xj, var) for Xj in csp.neighbors[var]])
            if inference != csp.FAILURE:
                result = backtrack_order_AC3(assignment, csp)
                if result != csp.FAILURE:
                    return result
            # if not success remove the current variable assignment
           # print("Fail..backtrack")
        del assignment[var]
        csp.currentDomain = copy.deepcopy(backup_domain)
            #remove inferences from assignment


    return csp.FAILURE


#validate command line input, return 0 if invalid format ,  1 if valid
def validateInputs(args):

    if len(args) != 3 or not(int(args[1]) == 1 or int(args[1]) == 2):
        print("Invalid input format.. Usage: py dfsb.py <mode> <Input file-name>")
        return 0
    else:
        return 1


if __name__ == '__main__':

    in_file = ''

    if validateInputs(sys.argv) == 1:

        if len(sys.argv) == 3:
            mode = sys.argv[1]
            in_file = open(sys.argv[2], 'r')

            # Read inputs from file
            firstLine = in_file.readline().strip().split('\t')

            inputLines = []
            # Read the constraints
            print(firstLine)
            for i in range(int(firstLine[1])):
                inputLines.append(in_file.readline().strip().split('\t'))

            # Create CSP object with values initialised
            csp = CSP(mode, firstLine, inputLines)

            if mode == '1':
               result = recursive_backtrack({},csp)

            if mode == '2':
                result = backtrack_order_AC3({},csp)

            if result == csp.FAILURE:
               print("There is no consistent assignment possible")
            else:
               print("\n\n Valid assignment found : \n")
               print(result)
               for r in result:
                   print(result[r])

            print("time = ",time.time()- csp.start_time)
            print("steps = ",counter)
