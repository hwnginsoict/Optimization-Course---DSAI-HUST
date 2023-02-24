#input from file
with open('input.txt') as f:
    al=f.readlines()
# print(al)
(n, m) = al[0].strip().split(' ')
m=int(m)
n=int(n)
Q=[[]for i in range(n)]
for i in range(n):
    k = al[i+1].strip('\n').split(' ')
    for j in range (m):
        Q[i].append(int(k[j]))
# print(Q)
d=[[]for i in range(m+1)]
for i in range(m+1):
    k = al[i+n+1].strip('\n').split(' ')
    for j in range(m+1):
        d[i].append([int(k[j]),[i]])
q=[]
# print(d)
k = al[m+n+2].strip('\n').split(' ')
for i in range(n):
    q.append(int(k[i]))
# print(q)

#pre-processing

def preprocess():
    #the preprocess path turn the objective solution into a path in which each self is visited once
    #using Floyd Warshall algorithm to find shortest path between any 2 shelves
    for k in range(m+1):
        for i in range(m+1):
            for j in range(m+1):
                if d[i][j][0] > d[i][k][0] + d[k][j][0]:
                    d[i][j][0] = d[i][k][0] + d[k][j][0]
                    d[i][j][1] = d[i][k][1] + d[k][j][1]
preprocess()

#genetic algorithm
max_generation = 200
crossover_rate = 0.9
mutation_rate = 0.05
pop_size = 2000
def random_indivs(m):
    lst=[]
    for i in range (1,m+1):
        lst.append(i)
    random.shuffle(lst)
    return lst
def check(sum):
  for i in range (len(sum)):
    if sum[i]<q[i]:
      return False
  return True
def calculate_fitness(indivs):
    global end
    sum=[0 for i in range (n)]
    pathcost=d[0][indivs[0]][0]
    for j in range(n):
        sum[j]+=Q[j][indivs[0]-1]
    for i in range (1,m): #len of indivs
        if check(sum):
          end=indivs[i-1]
          break
        pathcost+=d[indivs[i-1]][indivs[i]][0]
        for j in range(n):
            sum[j]+=Q[j][indivs[i]-1]
    pathcost+=d[end][0][0]
    return pathcost

def swap_mutation(indivs):
    p1=random.randint(1,m//2)
    p2=random.randint(1,m//2)
    while (p1==p2):
        p2=random.randint(1,m//2)
    temp=indivs[p1]
    indivs[p1]=indivs[p2]
    indivs[p2]=temp
def random_population(pop_size):
    pop=[]
    while (len(pop) <= pop_size):
        point=random_indivs(m)
        pop.append(point)
    return pop
def single_point_crossover(point1, point2):
    o1=[]
    o2=[]
    v1=[]
    v2=[]
    for i in range (m+10):
        v1.append(0)
        v2.append(0)
    p=random.randint(1,m//2)
    for i in range (p):
        o1.append(point2[i])
        o2.append(point1[i])
        v1[point2[i]]=1
        v2[point1[i]]=1
    index=0
    for i in range (p,m):
        while(v1[point1[index]]!=0):
            index+=1
        o1.append(point1[index])
        v1[o1[i]]=1
    index=0
    for i in range (p,m):
        while(v2[point2[index]]!=0):
            index+=1
        o2.append(point2[index])
        v2[o2[i]]=1
    return [o1,o2]
def comparator(point):
    return (calculate_fitness(point))
def survivor_selection(pop,pop_size):
    pop.sort(key=comparator)
    while (len(pop) > pop_size):
        pop.pop(180)
        # pop.pop()
def reproduction(pop):
    offspring=[]
    while (len(offspring) < pop_size):
        p1=random.randint(0,pop_size/2)
        p2=random.randint(0,pop_size/2)
        while(p1==p2):
            p2=random.randint(0,pop_size/2)
        if(random.randint(1,10)/10 < crossover_rate):
            #print(p1,p2)
            child=single_point_crossover(pop[p1],pop[p2])
            offspring.append(child[0])
            offspring.append(child[1])
    for i in range(len(offspring)):
        if(random.randint(1,100)/100 < mutation_rate):
            swap_mutation(offspring[i])
    return offspring
def print_path(indivs):
    sum=[0 for i in range (n)]
    result=[0,indivs[0]]
    for j in range(n):
        sum[j]+=Q[j][indivs[0]-1]
    for i in range (1,m): #len of indivs
        if check(sum):
            break
        for j in range(n):
            sum[j]+=Q[j][indivs[i]-1]
        result.append(indivs[i])
    result.append(0)
    return(result)
def outp(Path):
    print(*d[0][Path[0]][1], end=' ')
    for i in range(len(Path)-1):
        print(*d[Path[i]][Path[i+1]][1], end=' ')
    print(*d[Path[len(Path)-1]][0][1], end=' ')
    print(0)
def main():
    generation=0
    pop=random_population(pop_size)
    while(generation < max_generation):
        generation+=1
        offspring=reproduction(pop)
        for i in range(len(offspring)):
            pop.append(offspring[i])
        survivor_selection(pop,pop_size)
        best=calculate_fitness(pop[0])
        # print("Generation",generation,"has the best result:",best)
    print("Best result is:",best)
    print("Best path is: ",end='')
    outp(print_path(pop[0])[1:-1])
    return [best,print_path(pop[0])]
def reinforce():
  for i in range(10):
    if(i==0): 
      k=main()
      glo=k[0]
    else:
      k=main()
      if(k[0]<glo): 
        glo=k[0]
        path=k[1]
  print(glo)
  print(*path)
main()
#reinforce()