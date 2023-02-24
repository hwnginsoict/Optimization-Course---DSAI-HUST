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

#greedy algorithm 1

def check(sum):
  for i in range (len(sum)):
    if sum[i]<q[i]:
      return False
  return True

visit=[True for i in range (n)]
sum=[0 for i in range (n)]
remain=[]
for i in range(1,m+1):
  remain.append(i)
start=0
path=[0]
pathcost=0
while (check(sum)==False and len(remain)!=0):
  local_min=d[start][remain[0]][0]
  start=remain[0]
  for i in range (1,len(remain)):
    if d[start][remain[i]][0] < local_min:
      local_min = d[start][remain[i]][0]
      start=remain[i]
  pathcost+=local_min
  remain.remove(start)
  for i in range (n): #len of sum
    sum[i]+=Q[i][start-1]
  path.append(start)
path.append(0)
pathcost+=d[start][0][0]
print(*path)
print(pathcost)
