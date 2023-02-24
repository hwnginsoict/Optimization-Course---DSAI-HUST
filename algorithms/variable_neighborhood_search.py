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

#variable neighborhood search

import random
import math

curdist = 0
curpath = [0]
curgoods = [0]*n
curleft = n
curpool = []

bestdist = 10**10
bestpath = []

def outp():
    global bestpath, d, bestdist 
    for i in range(len(bestpath)-1):
        print(*d[bestpath[i]][bestpath[i+1]][1], end=' ')
    print(0)
    print(bestdist)

full = [i for i in range(1, m+1)]
random.shuffle(full)
full *= 2
r = 0
last_r = 0

def initial():
    # global curpath, curdist, d
    # curpath = [i for i in range(1, m+1)]
    # random.shuffle(curpath)
    # curpath = [0] + curpath + [0]
    # for i in range(len(curpath)-1):
    #     curdist += d[curpath[i]][curpath[i+1]][0]

    global full, r, curleft, n, curgoods, Q, curpath, curdist, curpool, m, last_r
    curdist = 0
    curpath = [0]
    curgoods = [0]*n
    curleft = n
    ir = 0
    while curleft > 0:
        for j in range(n):
            if curgoods[j] < q[j] and curgoods[j] + Q[j][full[r]-1] >= q[j]:
                curleft -= 1
            curgoods[j] += Q[j][full[r]-1]
        curdist += d[curpath[ir]][full[r]][0]
        curpath.append(full[r])
        r += 1
        ir += 1
    curdist += d[curpath[ir]][0][0]
    curpath += [0]
    curpool = full[:last_r] + full[r:m] if r < m else full[r:last_r+m]
    last_r = r

def cut(path, dist, goods, left, pool, num):
    global d, q, Q
    ret = dist
    ret_path = []
    ret_goods = []
    ret_left = left
    ret_pool = []
    for i1 in range(1, len(path)-1):
        x1 = path[i1]
        for k in range(n):
            if goods[k] >= q[k] and goods[k]-Q[k][x1-1] < q[k]:
                left += 1
            goods[k] -= Q[k][x1-1]
        dist += d[path[i1-1]][path[i1+1]][0] \
              - d[path[i1-1]][x1][0] - d[x1][path[i1+1]][0]
        path = path[:i1] + path[i1+1:]
        pool.append(x1)

        if left <= 0 and dist < ret:
            ret = dist
            ret_path = path[:]
            ret_goods = goods[:]
            ret_left = left
            ret_pool = pool[:]
        
        if num >= 2:
            for i2 in range(1, len(path)-1):
                x2 = path[i2]
                for k in range(n):
                    if goods[k] >= q[k] and goods[k]-Q[k][x2-1] < q[k]:
                        left += 1
                    goods[k] -= Q[k][x2-1]
                dist += d[path[i2-1]][path[i2+1]][0] \
                      - d[path[i2-1]][x2][0] - d[x2][path[i2+1]][0]
                path = path[:i2] + path[i2+1:]
                pool.append(x2)

                if left <= 0 and dist < ret:
                    ret = dist
                    ret_path = path[:]
                    ret_goods = goods[:]
                    ret_left = left
                    ret_pool = pool[:]

                if num >= 3:
                    for i3 in range(1, len(path)-1):
                        x3 = path[i3]
                        for k in range(n):
                            if goods[k] >= q[k] and goods[k]-Q[k][x3-1] < q[k]:
                                left += 1
                            goods[k] -= Q[k][x3-1]
                        dist += d[path[i3-1]][path[i3+1]][0] \
                              - d[path[i3-1]][x3][0] - d[x3][path[i3+1]][0]
                        path = path[:i3] + path[i3+1:]
                        pool.append(x3)

                        if left <= 0 and dist < ret:
                            ret = dist
                            ret_path = path[:]
                            ret_goods = goods[:]
                            ret_left = left
                            ret_pool = pool[:]

                        path = path[:i3] + [x3] + path[i3:]
                        for k in range(n):
                            if goods[k] < q[k] and goods[k]+Q[k][x3-1] >= q[k]:
                                left -= 1
                            goods[k] += Q[k][x3-1]
                        dist += d[path[i3-1]][x3][0] + d[x3][path[i3+1]][0] \
                              - d[path[i3-1]][path[i3+1]][0]
                        pool.pop()

                path = path[:i2] + [x2] + path[i2:]
                for k in range(n):
                    if goods[k] < q[k] and goods[k]+Q[k][x2-1] >= q[k]:
                        left -= 1
                    goods[k] += Q[k][x2-1]
                dist += d[path[i2-1]][x2][0] + d[x2][path[i2+1]][0] \
                      - d[path[i2-1]][path[i2+1]][0]
                pool.pop()
                
                
        path = path[:i1] + [x1] + path[i1:]
        for k in range(n):
            if goods[k] < q[k] and goods[k]+Q[k][x1-1] >= q[k]:
                left -= 1
            goods[k] += Q[k][x1-1]
        dist += d[path[i1-1]][x1][0] + d[x1][path[i1+1]][0] \
              - d[path[i1-1]][path[i1+1]][0]
        pool.pop()

    return ret, ret_path, ret_goods, ret_left, ret_pool

def switch(path, dist, num):
    global d
    ret = dist
    ret_path = []
    for i1 in range(1, len(path)-1):
        for j1 in range(1, len(path)-1):
            if i1 == j1:
                continue

            if i1 == j1+1 or i1+1 == j1:
                y1 = min(i1, j1)
                y2 = max(i1, j1)
                dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                      - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
            else:
                dist += d[path[i1-1]][path[j1]][0] + d[path[j1]][path[i1+1]][0] \
                      + d[path[j1-1]][path[i1]][0] + d[path[i1]][path[j1+1]][0] \
                      - d[path[i1-1]][path[i1]][0] - d[path[i1]][path[i1+1]][0] \
                      - d[path[j1-1]][path[j1]][0] - d[path[j1]][path[j1+1]][0]
            path[i1], path[j1] = path[j1], path[i1]

            if dist < ret:
                ret = dist
                ret_path = path[:]

            if num >= 2:
                for i2 in range(1, len(path)-1):
                    for j2 in range(1, len(path)-1):
                        if i2 == j2:
                            continue

                        if i2 == j2+1 or i2+1 == j2:
                            y1 = min(i2, j2)
                            y2 = max(i2, j2)
                            dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                                  - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
                        else:
                            dist += d[path[i2-1]][path[j2]][0] + d[path[j2]][path[i2+1]][0] \
                                + d[path[j2-1]][path[i2]][0] + d[path[i2]][path[j2+1]][0] \
                                - d[path[i2-1]][path[i2]][0] - d[path[i2]][path[i2+1]][0] \
                                - d[path[j2-1]][path[j2]][0] - d[path[j2]][path[j2+1]][0]
                        path[i2], path[j2] = path[j2], path[i2]

                        if dist < ret:
                            ret = dist
                            ret_path = path[:]

                        if num >= 3:
                            for i3 in range(1, len(path)-1):
                                for j3 in range(1, len(path)-1):
                                    if i3 == j3:
                                        continue

                                    if i3 == j3+1 or i3+1 == j3:
                                        y1 = min(i3, j3)
                                        y2 = max(i3, j3)
                                        dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                                            - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
                                    else:
                                        dist += d[path[i3-1]][path[j3]][0] + d[path[j3]][path[i3+1]][0] \
                                            + d[path[j3-1]][path[i3]][0] + d[path[i3]][path[j3+1]][0] \
                                            - d[path[i3-1]][path[i3]][0] - d[path[i3]][path[i3+1]][0] \
                                            - d[path[j3-1]][path[j3]][0] - d[path[j3]][path[j3+1]][0]
                                    path[i3], path[j3] = path[j3], path[i3]

                                    if dist < ret:
                                        ret = dist
                                        ret_path = path[:]

                                    if i3 == j3+1 or i3+1 == j3:
                                        y1 = min(i3, j3)
                                        y2 = max(i3, j3)
                                        dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                                            - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
                                    else:
                                        dist += d[path[i3-1]][path[j3]][0] + d[path[j3]][path[i3+1]][0] \
                                            + d[path[j3-1]][path[i3]][0] + d[path[i3]][path[j3+1]][0] \
                                            - d[path[i3-1]][path[i3]][0] - d[path[i3]][path[i3+1]][0] \
                                            - d[path[j3-1]][path[j3]][0] - d[path[j3]][path[j3+1]][0]
                                    path[i3], path[j3] = path[j3], path[i3]

                        if i2 == j2+1 or i2+1 == j2:
                            y1 = min(i2, j2)
                            y2 = max(i2, j2)
                            dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                                  - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
                        else:
                            dist += d[path[i2-1]][path[j2]][0] + d[path[j2]][path[i2+1]][0] \
                                + d[path[j2-1]][path[i2]][0] + d[path[i2]][path[j2+1]][0] \
                                - d[path[i2-1]][path[i2]][0] - d[path[i2]][path[i2+1]][0] \
                                - d[path[j2-1]][path[j2]][0] - d[path[j2]][path[j2+1]][0]
                        path[i2], path[j2] = path[j2], path[i2]

            if i1 == j1+1 or i1+1 == j1:
                y1 = min(i1, j1)
                y2 = max(i1, j1)
                dist += d[path[y1-1]][path[y2]][0] + d[path[y2]][path[y1]][0] + d[path[y1]][path[y2+1]][0] \
                      - d[path[y1-1]][path[y1]][0] - d[path[y1]][path[y2]][0] - d[path[y2]][path[y2+1]][0]
            else:
                dist += d[path[i1-1]][path[j1]][0] + d[path[j1]][path[i1+1]][0] \
                      + d[path[j1-1]][path[i1]][0] + d[path[i1]][path[j1+1]][0] \
                      - d[path[i1-1]][path[i1]][0] - d[path[i1]][path[i1+1]][0] \
                      - d[path[j1-1]][path[j1]][0] - d[path[j1]][path[j1+1]][0]
            path[i1], path[j1] = path[j1], path[i1]

    return ret, ret_path

def slip(path, dist, num):
    global d
    ret = dist
    ret_path = []
    for i1 in range(1, len(path)-1):
        x1 = path[i1]

        dist += d[path[i1-1]][path[i1+1]][0] \
              - d[path[i1-1]][x1][0] - d[x1][path[i1+1]][0]
        path = path[:i1] + path[i1+1:]
        for j1 in range(1, len(path)):
            dist += d[path[j1-1]][x1][0] + d[x1][path[j1]][0] \
                  - d[path[j1-1]][path[j1]][0]
            path = path[:j1] + [x1] + path[j1:]

            if dist < ret:
                ret = dist
                ret_path = path[:]

            if num >= 2:
                for i2 in range(1, len(path)-1):
                    x2 = path[i2]

                    dist += d[path[i2-1]][path[i2+1]][0] \
                          - d[path[i2-1]][x2][0] - d[x2][path[i2+1]][0]
                    path = path[:i2] + path[i2+1:]
                    for j2 in range(1, len(path)):
                        dist += d[path[j2-1]][x2][0] + d[x2][path[j2]][0] \
                              - d[path[j2-1]][path[j2]][0]
                        path = path[:j2] + [x2] + path[j2:]

                        if dist < ret:
                            ret = dist
                            ret_path = path[:]

                        if num >= 3:
                            for i3 in range(1, len(path)-1):
                                x3 = path[i3]

                                dist += d[path[i3-1]][path[i3+1]][0] \
                                      - d[path[i3-1]][x3][0] - d[x3][path[i3+1]][0]
                                path = path[:i3] + path[i3+1:]
                                for j3 in range(1, len(path)):
                                    dist += d[path[j3-1]][x3][0] + d[x3][path[j3]][0] \
                                          - d[path[j3-1]][path[j3]][0]
                                    path = path[:j3] + [x3] + path[j3:]

                                    if dist < ret:
                                        ret = dist
                                        ret_path = path[:]

                                    dist += d[path[j3-1]][path[j3+1]][0] \
                                          - d[path[j3-1]][x3][0] - d[x3][path[j3+1]][0]
                                    path = path[:j3] + path[j3+1:]
                                
                                path = path[:i3] + [x3] + path[i3:]
                                dist += d[path[i3-1]][x3][0] + d[x3][path[i3+1]][0] \
                                      - d[path[i3-1]][path[i3+1]][0]

                        dist += d[path[j2-1]][path[j2+1]][0] \
                              - d[path[j2-1]][x2][0] - d[x2][path[j2+1]][0]
                        path = path[:j2] + path[j2+1:]
                    
                    path = path[:i2] + [x2] + path[i2:]
                    dist += d[path[i2-1]][x2][0] + d[x2][path[i2+1]][0] \
                          - d[path[i2-1]][path[i2+1]][0]

            dist += d[path[j1-1]][path[j1+1]][0] \
                  - d[path[j1-1]][x1][0] - d[x1][path[j1+1]][0]
            path = path[:j1] + path[j1+1:]
        
        path = path[:i1] + [x1] + path[i1:]
        dist += d[path[i1-1]][x1][0] + d[x1][path[i1+1]][0] \
              - d[path[i1-1]][path[i1+1]][0]
        
    return ret, ret_path

def swap(path, dist, goods, left, pool, num):
    global d, q, Q
    ret = dist
    ret_path = []
    ret_goods = []
    ret_left = left
    ret_pool = []
    for i1 in range(1, len(path)-1):
        for j1 in range(len(pool)):
            for k in range(n):
                if goods[k] < q[k] and goods[k] + Q[k][pool[j1]-1] - Q[k][path[i1]-1] >= q[k]:
                    left -= 1
                elif goods[k] >= q[k] and goods[k] + Q[k][pool[j1]-1] - Q[k][path[i1]-1] < q[k]:
                    left += 1
                goods[k] += Q[k][pool[j1]-1] - Q[k][path[i1]-1]
            dist += d[path[i1-1]][pool[j1]][0] + d[pool[j1]][path[i1+1]][0] \
                  - d[path[i1-1]][path[i1]][0] - d[path[i1]][path[i1+1]][0]
            path[i1], pool[j1] = pool[j1], path[i1]

            if left <= 0 and dist < ret:
                ret = dist
                ret_path = path[:]
                ret_goods = goods[:]
                ret_left = left
                ret_pool = pool[:]

            if num >= 2:
                for i2 in range(1, len(path)-1):
                    for j2 in range(len(pool)):
                        for k in range(n):
                            if goods[k] < q[k] and goods[k] + Q[k][pool[j2]-1] - Q[k][path[i2]-1] >= q[k]:
                                left -= 1
                            elif goods[k] >= q[k] and goods[k] + Q[k][pool[j2]-1] - Q[k][path[i2]-1] < q[k]:
                                left += 1
                            goods[k] += Q[k][pool[j2]-1] - Q[k][path[i2]-1]
                        dist += d[path[i2-1]][pool[j2]][0] + d[pool[j2]][path[i2+1]][0] \
                            - d[path[i2-1]][path[i2]][0] - d[path[i2]][path[i2+1]][0]
                        path[i2], pool[j2] = pool[j2], path[i2]

                        if left <= 0 and dist < ret:
                            ret = dist
                            ret_path = path[:]
                            ret_goods = goods[:]
                            ret_left = left
                            ret_pool = pool[:]

                        if num >= 3:
                            for i3 in range(1, len(path)-1):
                                for j3 in range(len(pool)):
                                    for k in range(n):
                                        if goods[k] < q[k] and goods[k] + Q[k][pool[j3]-1] - Q[k][path[i3]-1] >= q[k]:
                                            left -= 1
                                        elif goods[k] >= q[k] and goods[k] + Q[k][pool[j3]-1] - Q[k][path[i3]-1] < q[k]:
                                            left += 1
                                        goods[k] += Q[k][pool[j3]-1] - Q[k][path[i3]-1]
                                    dist += d[path[i3-1]][pool[j3]][0] + d[pool[j3]][path[i3+1]][0] \
                                        - d[path[i3-1]][path[i3]][0] - d[path[i3]][path[i3+1]][0]
                                    path[i3], pool[j3] = pool[j3], path[i3]

                                    if left <= 0 and dist < ret:
                                        ret = dist
                                        ret_path = path[:]
                                        ret_goods = goods[:]
                                        ret_left = left
                                        ret_pool = pool[:]

                                    for k in range(n):
                                        if goods[k] < q[k] and goods[k] + Q[k][pool[j3]-1] - Q[k][path[i3]-1] >= q[k]:
                                            left -= 1
                                        elif goods[k] >= q[k] and goods[k] + Q[k][pool[j3]-1] - Q[k][path[i3]-1] < q[k]:
                                            left += 1
                                        goods[k] += Q[k][pool[j3]-1] - Q[k][path[i3]-1]
                                    dist += d[path[i3-1]][pool[j3]][0] + d[pool[j3]][path[i3+1]][0] \
                                        - d[path[i3-1]][path[i3]][0] - d[path[i3]][path[i3+1]][0]
                                    path[i3], pool[j3] = pool[j3], path[i3]

                        for k in range(n):
                            if goods[k] < q[k] and goods[k] + Q[k][pool[j2]-1] - Q[k][path[i2]-1] >= q[k]:
                                left -= 1
                            elif goods[k] >= q[k] and goods[k] + Q[k][pool[j2]-1] - Q[k][path[i2]-1] < q[k]:
                                left += 1
                            goods[k] += Q[k][pool[j2]-1] - Q[k][path[i2]-1]
                        dist += d[path[i2-1]][pool[j2]][0] + d[pool[j2]][path[i2+1]][0] \
                            - d[path[i2-1]][path[i2]][0] - d[path[i2]][path[i2+1]][0]
                        path[i2], pool[j2] = pool[j2], path[i2]
            
            for k in range(n):
                if goods[k] < q[k] and goods[k] + Q[k][pool[j1]-1] - Q[k][path[i1]-1] >= q[k]:
                    left -= 1
                elif goods[k] >= q[k] and goods[k] + Q[k][pool[j1]-1] - Q[k][path[i1]-1] < q[k]:
                    left += 1
                goods[k] += Q[k][pool[j1]-1] - Q[k][path[i1]-1]
            dist += d[path[i1-1]][pool[j1]][0] + d[pool[j1]][path[i1+1]][0] \
                  - d[path[i1-1]][path[i1]][0] - d[path[i1]][path[i1+1]][0]
            path[i1], pool[j1] = pool[j1], path[i1]

    return ret, ret_path, ret_goods, ret_left, ret_pool

ext = 3 if m*n <= 200 else 2

def next():
    global curpath, curdist, curgoods, curleft, curpool, end, bestdist, bestpath, ext
    for i in range(1, ext+1):
        dist1, path1, goods1, left1, pool1 = cut(curpath, curdist, curgoods, curleft, curpool, i)
        dist2, path2 = switch(curpath, curdist, i)
        dist3, path3 = slip(curpath, curdist, i)
        dist4, path4, goods4, left4, pool4 = swap(curpath, curdist, curgoods, curleft, curpool, i-1)
        x = min(dist1, dist2, dist3, dist4)
        if x < curdist:
            curdist = x
            if dist1 == x:
                curpath = path1[:]
                curgoods = goods1[:]
                curleft = left1
                curpool = pool1[:]
            elif dist2 == x:
                curpath = path2[:]
            elif dist3 == x:
                curpath = path3[:]
            elif dist4 == x:
                curpath = path4[:]
                curgoods = goods4[:]
                curleft = left4
                curpool = pool4[:]
            break
        if i == ext:
            end = True

end = False

def VNS():
    global bestdist, bestpath
    while True:
        next()
        if end:
            break
    if curdist < bestdist:
        bestdist = curdist
        bestpath = curpath

while r < m:
    initial()
    VNS()
outp()