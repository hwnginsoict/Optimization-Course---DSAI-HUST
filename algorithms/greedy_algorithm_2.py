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

#2nd greedy algorithm

ans = 0
Path = []

def greedy():
    global d, q, Q, ans, Path
    left = n
    visited = [False for i in range(m+1)]
    cur = 0
    picked = [0 for j in range(n)]
    while left > 0:    
        Max = 0
        for i in range(1, m+1):
            if visited[i]:
                continue
            goods = 0
            for j in range(n):
                goods += max(0, min(q[j]-picked[j], Q[j][i-1]))
            if goods/d[cur][i][0] > Max:
                Max = goods/d[cur][i][0]
                next = i
        for j in range(n):
            if picked[j] < q[j] and picked[j]+Q[j][next-1] >= q[j]:
                left -= 1
            picked[j] += Q[j][next-1]    
        ans += d[cur][next][0]
        cur = next
        Path.append(cur)
        visited[cur] = True
    ans += d[cur][0][0]

def outp():
    global Path, d, ans
    print(*d[0][Path[0]][1], end=' ')
    for i in range(len(Path)-1):
        print(*d[Path[i]][Path[i+1]][1], end=' ')
    print(*d[Path[len(Path)-1]][0][1], end=' ')
    print(0)
    print(ans)

greedy()
outp()