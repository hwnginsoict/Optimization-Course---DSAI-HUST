#generate input random 1
import random
[n, m]=[int(x) for x in input().split()]
Q=[[0 for i in range (m)] for j in range (n)]
d=[[[0, [j]] for i in range (m+1)] for j in range (m+1)]
for i in range (n):
  for j in range (m):
    Q[i][j]=random.randint(1,4)
for i in range (m+1):
  for j in range (m+1):
    if (i==j): d[i][j][0]=0
    else:
      d[i][j][0]=random.randint(2,9)
for i in range(n):
  print(*Q[i])
for i in range(m+1):
  for j in range(m+1):
    print(d[i][j][0], end=' ')
  print()
q=[2*m for i in range (n)]
print(*q)