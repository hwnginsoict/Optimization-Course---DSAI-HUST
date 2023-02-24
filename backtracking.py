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

# backtracking

f = 0
fmin = 10**10
path = []
pathmin = []
visit = [0 for i in range(m+1)]
bt = [0 for i in range(m+1)]
p = [0 for i in range(n)]

def outp():
    global fmin, pathmin
    print(*pathmin)
    print(fmin)

dist = [10**10 for i in range(n)]

def bound():
    global dist, Q
    for k in range(n):
        for j in range(1, m+1):
            for i in range(m+1):
                if i != j:
                    dist[k] = min(dist[k], d[i][j][0]/Q[k][j-1])

def sol(last):
    global f, fmin, p, path, pathmin
    for i in range(n):
        if p[i] < q[i]:
            return False
    if f + d[last][0][0] < fmin:
        fmin = f + d[last][0][0]
        pathmin = path + d[last][0][1] + [0]
    return True

def backtrack(x,last):
    global f, path, visit, bt, p, fmin, q, dist
    if sol(last):
        return
    for i in range(1, m+1):
        if visit[i] == 0:
            if f + d[last][i][0] > fmin:
                continue
            check = False
            for j in range(n):
                if f + d[last][i][0] + dist[j]*max(0, q[j]-p[j]-Q[j][i-1]) > fmin:
                    check = True
                    break
            if check:
                continue
            bt[x] = i
            f += d[last][i][0]
            path += d[last][i][1]
            visit[i] = 1
            for j in range(n):
                p[j] += Q[j][i-1]
            backtrack(x+1, i)
            for j in range(n):
                p[j] -= Q[j][i-1]
            visit[i] = 0
            for j in range(len(d[last][i][1])):
                path.pop()
            f -= d[last][i][0]

bound()
backtrack(0,0)
outp()