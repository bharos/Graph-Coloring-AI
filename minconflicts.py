import sys
import copy
import math
import random
import time
class CSP:
    def __init__(self, firstLine, inputLines ):
        self.visited_count = 300
        self.counter = 0
        self.counter_limit = 20
        #self.cooloff = 30

        self.tabu_list = []
        self.FAILURE = False
        self.SUCCESS = True

        self.constraints = inputLines
        self.varNums = int(firstLine[0])
        self.variables = [v for v in range(int(firstLine[0]))]
        self.neighbors = {key:[] for key in range(0,int(firstLine[0]))}
        self.domain = [d for d in range(int(firstLine[2]))]

        for arc in inputLines:
            self.neighbors[int(arc[0])].append(int(arc[1]))
            self.neighbors[int(arc[1])].append(int(arc[0]))
      #  print(self.variables)
       # print(self.neighbors)
        #print(self.domain)

        for arc in inputLines:
            self.neighbors[int(arc[0])].append(int(arc[1]))
            self.neighbors[int(arc[1])].append(int(arc[0]))

        #Track the starting time of execution
        self.start = time.time()


def is_solution(csp, assignment):

        #Check if the constraints have conflicting values
        for constraint in csp.constraints:
            if assignment[int(constraint[0])] == assignment[int(constraint[1])]:
#                print('constraint',end=" ")
 #               print(constraint)
                return False
        #No conflicts, hence assignment is consistent
        return True


def count_conf(csp, assignment):

    count = 0
    # Check if the constraints have conflicting values
    for constraint in csp.constraints:
        if assignment[int(constraint[0])] == assignment[int(constraint[1])]:
            #                print('constraint',end=" ")

      #      print(constraint)
            count+=1
    # No conflicts, hence assignment is consistent
    return count


def count_conflicts(csp, var, value, assignment):

    temp_assignment = copy.deepcopy(assignment)
    temp_assignment[var] = value
    count = 0
    # Check if the constraints have conflicting values
    for constraint in csp.constraints:
        if temp_assignment[int(constraint[0])] == temp_assignment[int(constraint[1])]:
            count += 1

    return count

def get_probability(csp, deltaE):


    #get the current time difference
    time_diff = time.time() - csp.start

    diff = csp.cooloff -time_diff


    print("conf = ",deltaE," diff= ",diff)

    probability = pow(math.e, -deltaE/diff)

    if diff < 0:
        probability = 0.1
    print(probability)

    return random.random() < probability


#Randomly choose a conflicted variable
def choose_variable(csp, assignment):
    if csp.counter > csp.counter_limit:
     #   print("Plateauuuuuuuuuxxxxxx")
        random_var = random.randrange(0,csp.varNums)

     #   print("Random var = "+str(random_var))
        return random_var

    while True:

        conflict_variables = []

        for var in range(0,csp.varNums):
            for neighbor in csp.neighbors[var]:
                if assignment[neighbor] == assignment[var]:
                    conflict_variables.append(var)
                    break

     #   print(conflict_variables)
     #   print(len(conflict_variables))

        random_var = conflict_variables[random.randrange(len(conflict_variables))]

     #   for neighbor in csp.neighbors[random_var]:
     #       if assignment[neighbor] == assignment[random_var]:
                #print("random var = " + str(random_var))
                #return random_var
     #   print("failed random_var = "+str(random_var))

        return  random_var


def min_conflict_value(csp, var, assignment):
        if (csp.counter > csp.counter_limit):

        #    print("plateaauuuuuuuxx")
         #   print('  _________\n /         \\\n |  /\\ /\\  |\n |    -    |\n |  \\___/  |\n \\_________/');
            csp.tabu_list = []
            min_conf_val = csp.domain[random.randrange(0,len(csp.domain))]
            csp.counter = 0

        else:
            min_conf = math.inf
            conf_dict = {}
         #   print("Current conf = ",end= " ")
        #    print(count_conf(csp,assignment))
            for value in csp.domain:
                conf =  count_conflicts(csp, var, value, assignment)
                if conf not in conf_dict:
                    conf_dict[conf] = []
                conf_dict[conf].append(value)

                if conf < min_conf:
                    min_conf = conf
                    min_conf_val = value

          #  print(conf_dict)
           # print(conf_dict[min_conf])

            min_conf_val = conf_dict[min_conf][random.randrange(0,len(conf_dict[min_conf]))]

        return min_conf_val


steps = 0
def min_conflicts(assignment, csp):

    global steps
    #var = -1
    #value = -1
   # initial_conflicts = math.inf

    #create an initial random complete assignment
    domain_size = len(csp.domain)
    for v in range(csp.varNums):
        assignment[v] = random.randrange(0,domain_size)
    #print(assignment)
    prev_assignment = []
    while True:
        steps += 1
       # for v in range(csp.varNums):
        #    assignment[v] = random.randrange(0,domain_size)
     #   print(assignment)
       # if counter == 50:
        #   print("Go Random")
         #  for v in range(csp.varNums):
          #     assignment[v] = random.randrange(0,domain_size)

        if is_solution(csp, assignment):
            return assignment
     #   if(var >= 0):
      #      initial_conflicts = count_conflicts(csp,var,value,assignment)


        var = choose_variable(csp, assignment)

      #  print('rand var = ',str(var),end=" , ")
        value = min_conflict_value(csp, var, assignment)
    #    print('min conf val = ' + str(value),end=" , ")
     #   print("counter = ",csp.counter)

      #  if len(csp.tabu_list) == csp.visited_count:
       #     print("poppppp")
       #     csp.tabu_list.pop(0)

        temp_assignment = copy.deepcopy(assignment)
        temp_assignment[var] = value

 #       current_conflicts = count_conf(csp,temp_assignment)
#        diff_in_conf = current_conflicts-initial_conflicts
  #      if diff_in_conf > 0:
   #         if not get_probability(csp,diff_in_conf):
    #            print("Decision : False")
     #           continue

      #      else:
       #         print("Decision : True")

        if temp_assignment in csp.tabu_list:

                csp.counter += 1
                continue

        assignment[var] = value
        csp.tabu_list.append(copy.deepcopy(assignment))


    return False

#validate command line input, return 0 if invalid format ,  1 if valid
def validateInputs(args):

    if len(args) != 2:
        print("Invalid input format.. Usage: py dfsb.py  <Input file-name>")
        return 0
    else:
        return 1


if __name__ == '__main__':

    in_file = ''

    if validateInputs(sys.argv) == 1:

        if len(sys.argv) == 2:
            in_file = open(sys.argv[1], 'r')

            # Read inputs from file
            firstLine = in_file.readline().strip().split('\t')

            inputLines = []
            # Read the constraints
            print(firstLine)
            for i in range(int(firstLine[1])):
                inputLines.append(in_file.readline().strip().split('\t'))

            # Create CSP object with values initialised
            csp = CSP(firstLine, inputLines)


            result = min_conflicts({},csp)
            csp.end = time.time()




            if result == csp.FAILURE:
               print("There is no consistent assignment possible")
            else:
               print("\n\n Valid assignment found : \n")
               print(result)
            print("Time : ",csp.end-csp.start)
            print(steps)
