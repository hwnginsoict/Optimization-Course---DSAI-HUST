import random
import copy
import time
from ortools.sat.python import cp_model

class PickupProb:
    def __init__(self, mode='text', m=4, n=3):
        if mode == 'fast': # A fast example
            self.m = 10
            self.n = 10
            tempQ = [
[475, 557, 202, 882, 480, 140, 552, 758, 484, 740],
[364, 918, 193, 404, 566, 38, 100, 466, 988, 138],
[365, 422, 867, 88, 522, 99, 495, 715, 285, 550],
[802, 300, 783, 656, 221, 343, 785, 605, 681, 391],
[559, 19, 156, 690, 833, 79, 988, 894, 652, 320],
[435, 900, 645, 186, 108, 329, 631, 407, 460, 106],
[150, 71, 398, 520, 701, 256, 221, 706, 523, 107],
[761, 41, 480, 130, 346, 394, 540, 784, 671, 738],
[503, 941, 241, 707, 408, 989, 84, 988, 377, 410],
[609, 942, 359, 936, 988, 135, 421, 572, 361, 401],
]
            self.d = [
[0, 538, 786, 23, 764, 84, 963, 336, 459, 998, 964],
[467, 0, 920, 122, 482, 351, 947, 702, 51, 359, 547],
[907, 572, 0, 231, 654, 26, 73, 57, 908, 454, 74],
[424, 645, 393, 0, 320, 19, 251, 870, 581, 554, 580],
[67, 212, 573, 875, 0, 298, 423, 311, 546, 393, 164],
[966, 734, 577, 486, 380, 0, 880, 497, 239, 992, 424],
[520, 544, 809, 376, 722, 59, 0, 209, 877, 557, 874],
[286, 776, 486, 32, 264, 267, 802, 0, 786, 238, 538],
[157, 563, 512, 743, 695, 441, 115, 907, 0, 558, 757],
[676, 448, 483, 420, 267, 585, 560, 41, 576, 0, 110],
[573, 976, 218, 217, 507, 94, 136, 257, 369, 783, 0],
]
            self.q = [3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000, 3000]
            self.Q = [list(x) for x in zip(*tempQ)]
            self.Q.insert(0, [0 for i in range(self.n)])
        
        if mode == 'random': # Generate a random problem
            self.m = m
            self.n = n
            self.Q = [[0 for i in range(n)] for j in range(m)]
            self.d = [[0 for i in range(m+1)] for j in range(m+1)]
            self.q = [0 for i in range(n)]
            self.Q.insert(0, [0 for i in range(self.n)])

            for i in range(self.m):
                for j in range(self.n):
                    self.Q[i][j] = random.randint(0, 4)
            
            for i in range(self.m+1):
                for j in range(self.m+1):
                    if i == j:
                        self.d[i][j] = 0
                    else:
                        self.d[i][j] = random.randint(2, 9)

            for i in range(self.n):
                self.q[i] = random.randint(10, 15)

        if mode == 'user': # Prompt the user to input the problem
            [self.n, self.m] = [int(i) for i in input('Enter values for n and m separated by a space:').split()]
            
            print('Enter values in Q row by row:')
            self.Q = [[int(i) for i in input().split()] for j in range(self.n)]
            k = [list(x) for x in zip(*self.Q)]
            self.Q=k
            self.Q.insert(0, [0 for i in range(self.n)])
            
            print('Enter values for d row by row:')
            self.d = [[int(i) for i in input().split()] for j in range(self.m+1)]

            print('Enter values in q:')
            self.q = [int(i) for i in input().split()]
            
        if mode == 'text': # take value from the input.txt
            with open('input.txt') as f:
                al=f.readlines()
            # print(al)
            (self.n, self.m) = al[0].strip().split(' ')
            self.m=int(self.m)
            self.n=int(self.n)
            self.Q=[[] for i in range(self.n)]
            for i in range(self.n): 
                k = al[i+1].strip('\n').split(' ')
                for j in range (self.m):
                    self.Q[i].append(int(k[j]))
            #print(self.Q)
            k = [list(x) for x in zip(*self.Q)]
            self.Q=k
            self.Q.insert(0, [0 for i in range(self.n)])
            self.d=[[]for i in range(self.m+1)]
            for i in range(self.m+1):
                k = al[i+self.n+1].strip('\n').split(' ')
                for j in range(self.m+1):
                    self.d[i].append(int(k[j]))
            self.q=[]
            #print(d)
            k = al[self.m+self.n+2].strip('\n').split(' ')
            for i in range(self.n):
                self.q.append(int(k[i]))
            #print(q)

        # Prepocess
        self.prep = copy.deepcopy(self.d)
        self.path = list(
            list( str(j)+'->' for i in range(self.m+1)) for j in range(self.m+1)
        )

        for k in range(self.m+1):
            for i in range(self.m+1):
                for j in range(self.m+1):
                    if self.prep[i][j] > self.d[i][k] + self.d[k][j]:
                        self.prep[i][j] = self.d[i][k] + self.d[k][j]
                        self.path[i][j] = self.path[i][k] + self.path[k][j]
    
    def printProb(self): # Print the problem
        print('m = ', self.m)
        print('n = ', self.n)
        print('Q = ', self.Q)
        print('d = ', self.d)  
        print('q = ', self.q) 
        print()
        
    def solveCP(self):
        def solveN(num_var):
            model = cp_model.CpModel()

            x = list(
                list(model.NewBoolVar('') for i in range(self.m+1)) for j in range(num_var)
            )
            path = list(
                list(
                    list(
                        model.NewBoolVar('') for i in range(self.m+1)
                    ) for j in range(self.m+1)
                ) for k in range(num_var-1)
            )

            for i in range(num_var):
                model.AddExactlyOne(x[i][j] for j in range(self.m+1))
            
            for i in range(1, self.m+1):
                model.Add(sum(x[j][i] for j in range(num_var)) <= 1)

            for i in range(num_var):
                if i == 0 or i == num_var-1:
                    model.Add(x[i][0] == 1)
                else:
                    model.Add(x[i][0] == 0)

            for i in range(self.n):
                model.Add(sum(sum(self.Q[j][i]*x[k][j] for j in range(self.m+1)) for k in range(num_var)) >= self.q[i])
                
            for k in range(num_var-1):
                for i in range(self.m+1):
                    for j in range(self.m+1):
                        model.Add(x[k][i]+x[k+1][j] >= 2).OnlyEnforceIf(path[k][i][j])
                        model.Add(x[k][i]+x[k+1][j] < 2).OnlyEnforceIf(path[k][i][j].Not())

            objective_terms = []
            for k in range(num_var-1):
                temp = sum(sum(self.prep[i][j]*path[k][i][j] for i in range(self.m+1)) for j in range(self.m+1))
                objective_terms.append(temp)
            model.Minimize(sum(objective_terms))

            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = 20
            status = solver.Solve(model)
            
            if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
                print(f'Total distance: {solver.ObjectiveValue()}')
                path = ''
                pre = 0
                for i in range(1, num_var):
                    for j in range(self.m+1):
                        if solver.BooleanValue(x[i][j]):
                            path += self.path[pre][j]
                            pre = j
                path = path + '0'
                print('Path: ', path)
                return solver.ObjectiveValue(), path
            else:
                print('No solution found.')
                return float('inf'), None

        best = float('inf')
        best_path = None
        for i in range(3, self.m+3):
            print('Shelves visited:', i-2)
            temp = solveN(i)
            if temp[0] < best:
                best = temp[0]
                best_path = temp[1]
            print('Best so far: ', best, '\n')
        
        if best == float('inf'):
            print('Can\'t find a solution')

        return best, best_path

pr = PickupProb()
pr.printProb()
start = time.perf_counter()
best, best_path = pr.solveCP()
lon = time.perf_counter() - start
print('Best path found: ', best_path)
print('Best path\'s cost: ', best)
print('Done\n')
path_min = [int(i) for i in best_path.split('->')]
print(*path_min)
print(best)
print('Time to solve:', lon*1000, 'ms')
