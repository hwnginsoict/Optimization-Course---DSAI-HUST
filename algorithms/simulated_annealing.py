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

#simulated annealing

import random
import math

def outp():
    global Path, d, ans
    print(*d[0][Path[0]+1][1], end=' ')
    for i in range(len(Path)-1):
        print(*d[Path[i]+1][Path[i+1]+1][1], end=' ')
    print(*d[Path[len(Path)-1]+1][0][1], end=' ')
    print(0)
    print(ans)

def initial():
    global two_round, m, ans, End, F, Path
    # pool = [i for i in range(m)]
    # random.shuffle(pool)
    # two_round = [0, 0]
    # for i in range(m):
    #     min = 10**10
    #     ir = 0
    #     for j in range(len(two_round)-1):
    #         x = d[two_round[j]][pool[i]+1][0] + d[pool[i]+1][two_round[j+1]][0] \
    #             - d[two_round[i]][two_round[i+1]][0]
    #         if x < min:
    #             ir = j
    #             min = x
    #     two_round.insert(ir+1, pool[i])
    # # print(two_round)
    # # exit(0)
    # two_round = two_round[1:-1]*2
    two_round = [i for i in range(m)]
    random.shuffle(two_round)
    two_round *= 2
    ans, End = value(two_round)
    F = ans
    Path = two_round[:End+1][:]

def value(path):
    global d, n, Q
    it = 0
    left = n
    ret = d[0][path[0]+1][0]
    Qtmp = [0]*n
    for j in range(n):
        if Qtmp[j]+Q[j][path[it]] >= q[j]:
            left -= 1
        Qtmp[j] += Q[j][path[it]]
    while True:
        if it > 0:
            ret += d[path[it-1]+1][path[it]+1][0]
            for j in range(n):
                if Qtmp[j] < q[j] and Qtmp[j]+Q[j][path[it]] >= q[j]:
                    left -= 1
                Qtmp[j] += Q[j][path[it]]
        if left <= 0:
            break
        it += 1
    ret += d[path[it]+1][0][0]
    return ret, it

def better(x, y):
    global T
    if y <= x:
        return True
    else:
        p = random.random()
        # print (y)
        # print(math.exp(-(y-x)/T), p)
        return True if math.exp(-(y-x)/T) >= p else False

cnt = 0
tabu_list = [(0,0)]*m

def next():
    global m, End, two_round, ans, Path, F, cnt, tabu_list
    l = 0
    r = 0
    while True:
        l, r = random.sample(range(m), 2)
        if l <= End or r <= End:
            break
    if r < l:
        r += m
    if (l,r) in tabu_list:
        return
    tabu_list[cnt%m] = (l,r)
    tmp = two_round[:]
    tmp[l:r+1] = tmp[r:(l-1 if l > 0 else None):-1]
    if r < m:
        tmp[l+m:r+m+1] = tmp[l:r+1]
    else:
        tmp[:r-m+1] = tmp[m:r+1]
        tmp[l+m:] = tmp[l:m]
    f, end = value(tmp)
    # if (l,r) in tabu_list:
    #     if f < ans:
    #         ans = f
    #         Path = tmp[:end+1]
    #         F = f
    #         two_round = tmp[:]
    #         End = end
    #         tabu_list[cnt%m] = (l,r)
    #         cnt += 1
    #     return
    if f < ans:
        ans = f
        Path = tmp[:end+1]
    if better(F, f):
        F = f
        two_round = tmp[:]
        End = end
        # tabu_list[cnt%m] = (l,r)
        cnt += 1
    # print(F)
    # print(two_round)
    # print(End)

def anneal():
    global T, cnt
    T = 2000
    cooling_rate = 3e-4
    k_max = 20000
    for k in range(k_max):
        T *= 1-cooling_rate
        next()

initial()
anneal()
outp()