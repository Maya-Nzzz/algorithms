def hungarian(matrix, n):
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    g = [0] * (n + 1)
    way = [0] * (n + 1)

    for i in range(1, n + 1):
        g[0] = i
        min_v = [float('inf')] * (n + 1)
        seen = [False] * (n + 1)
        j0 = 0
        while True:
            seen[j0] = True
            i0 = g[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, n + 1):
                if not seen[j]:
                    cur = matrix[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < min_v[j]:
                        min_v[j] = cur
                        way[j] = j0
                    if min_v[j] < delta:
                        delta = min_v[j]
                        j1 = j
            for j in range(n + 1):
                if seen[j]:
                    u[g[j]] += delta
                    v[j] -= delta
                else:
                    min_v[j] -= delta
            j0 = j1
            if g[j0] == 0:
                break
        while True:
            j1 = way[j0]
            g[j0] = g[j1]
            j0 = j1
            if j1 == 0:
                break
    return -v[0]


n = int(input().strip())
matrix = []
total_trash = 0
for _ in range(n):
    row = list(map(int, input().split()))
    matrix.append(row)
    total_trash += sum(row)

total_max = max(max(row) for row in matrix) if matrix else 0
cost_matrix = [[total_max - x for x in row] for row in matrix]
min_cost = hungarian(cost_matrix, n)

max_in_place = n * total_max - min_cost
min_effort = total_trash - max_in_place
print(min_effort)
