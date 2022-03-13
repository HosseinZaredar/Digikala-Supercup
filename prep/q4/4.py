import numpy as np

r, c = map(int, input().split())

boxes = []
for _ in range(r):
    boxes += [list(map(int, input().split()))]

boxes = np.array(boxes)

sigma = np.sum(boxes)
ones = np.sum(boxes != 0)

# -- first senario --

side_max = np.max(boxes, axis=1)
front_max = np.max(boxes, axis=0)

for i in range(r):
    for j in range(c):
        if side_max[i] == front_max[j] and boxes[i, j] != 0:
            front_max[j] = 0
            break

num_maxes = sum(side_max != 0) + sum(front_max != 0)
sum_maxes = sum(side_max) + sum(front_max)

first = sigma - sum_maxes - (ones - num_maxes)

# -- second senario --

side_max = np.max(boxes, axis=1)
front_max = np.max(boxes, axis=0)

for i in range(r-1, -1, -1):
    for j in range(c):
        if side_max[i] == front_max[j] and boxes[i, j] != 0:
            front_max[j] = 0
            break

num_maxes = sum(side_max != 0) + sum(front_max != 0)
sum_maxes = sum(side_max) + sum(front_max)

second = sigma - sum_maxes - (ones - num_maxes)

# -- third senario --

side_max = np.max(boxes, axis=1)
front_max = np.max(boxes, axis=0)

for i in range(r):
    for j in range(c-1, -1, -1):
        if side_max[i] == front_max[j] and boxes[i, j] != 0:
            front_max[j] = 0
            break

num_maxes = sum(side_max != 0) + sum(front_max != 0)
sum_maxes = sum(side_max) + sum(front_max)

third = sigma - sum_maxes - (ones - num_maxes)

# -- forth senario --

side_max = np.max(boxes, axis=1)
front_max = np.max(boxes, axis=0)

for i in range(r-1, -1, -1):
    for j in range(c-1, -1, -1):
        if side_max[i] == front_max[j] and boxes[i, j] != 0:
            front_max[j] = 0
            break

num_maxes = sum(side_max != 0) + sum(front_max != 0)
sum_maxes = sum(side_max) + sum(front_max)

forth = sigma - sum_maxes - (ones - num_maxes)


print(max(first, second, third, forth))
