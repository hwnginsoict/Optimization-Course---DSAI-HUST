#input from file
with open('input.txt') as f:
    al=f.readlines()
# print(al)
(m, n) = al[0].strip().split(' ')
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

#dynamic programming

inf = 10**10

DP = {}
next = {}

def dp(shelves, last, goods, left):
    if (shelves, last, tuple(goods), left) in DP:
        return DP[(shelves, last, tuple(goods), left)]
    if left <= 0:
        next[(shelves, last, tuple(goods), left)] = (0,0,0,0)
        return d[last][0][0]
    if shelves == 1 << m:
        return inf
    bin = 1
    res = inf
    check = False
    for j in range(1, m+1):
        if shelves&bin == 0:         
            Goods = goods[:]            
            Left = left
            for i in range(n):
                Goods[i] += Q[i][j-1]
                if goods[i] < q[i] and Q[i][j-1] > 0:
                    check = True                    
                    if Goods[i] >= q[i]:
                        Left -= 1
            if check:
                x = dp(shelves|bin, j, Goods, Left) + d[last][j][0]
                if x < res:
                    res = x
                    next[(shelves, last, tuple(goods), left)] = (shelves|bin, j, tuple(Goods), Left)
        bin <<= 1
    DP[(shelves, last, tuple(goods), left)] = res
    return DP[(shelves, last, tuple(goods), left)]

def outp():
    x = dp(0, 0, [0]*n, n)
    i = (0, 0, tuple([0]*n), n)
    while i != (0,0,0,0):
        print(*d[i[1]][next[i][1]][1], end=' ')
        i = next[i]
    print(0)
    print(x)

preprocess()
outp()