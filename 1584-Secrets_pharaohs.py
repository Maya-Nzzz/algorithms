# Алгоритм минимальной стоимости потока для вычисления наименьшего количества перестановок
# Каждый блок из 4 элементов ((i,j), его отражения по строке, по столбцу и по диагонали)
# можно представить как группу из 4 ячеек, которые должны содержать одинаковую букву.
# Мы хотим распределить доступные буквы по этим блокам с минимальными изменениями.
from collections import deque, Counter


class Edge:
    __slots__ = ['v', 'cap', 'cost', 'rev']

    def __init__(self, v, cap, cost, rev):
        self.v = v
        self.cap = cap
        self.cost = cost
        self.rev = rev


def add_edge(graph, u, v, cap, cost):
    graph[u].append(Edge(v, cap, cost, len(graph[v])))
    graph[v].append(Edge(u, 0, -cost, len(graph[u]) - 1))


def min_cost_flow(N, graph, s, t, f):
    INF = 10 ** 9
    res = 0
    h = [0] * N
    prevv = [0] * N
    preve = [0] * N
    while f > 0:
        dist = [INF] * N
        dist[s] = 0
        inqueue = [False] * N
        q = deque([s])
        while q:
            u = q.popleft()
            inqueue[u] = False
            for i, e in enumerate(graph[u]):
                if e.cap > 0 and dist[e.v] > dist[u] + e.cost + h[u] - h[e.v]:
                    dist[e.v] = dist[u] + e.cost + h[u] - h[e.v]
                    prevv[e.v] = u
                    preve[e.v] = i
                    if not inqueue[e.v]:
                        q.append(e.v)
                        inqueue[e.v] = True
        if dist[t] == INF:
            return None
        for v in range(N):
            h[v] += dist[v]
        d = f
        v = t
        while v != s:
            d = min(d, graph[prevv[v]][preve[v]].cap)
            v = prevv[v]
        f -= d
        res += d * h[t]
        v = t
        while v != s:
            e = graph[prevv[v]][preve[v]]
            e.cap -= d
            graph[v][e.rev].cap += d
            v = prevv[v]
    return res


n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]
letter_counts = Counter()
for row in grid:
    for ch in row:
        letter_counts[ch] += 1
G = (n // 2) * (m // 2)
targets = {letter: cnt // 4 for letter, cnt in letter_counts.items()}
groups = []
for i in range(n // 2):
    for j in range(m // 2):
        coords = [(i, j), (i, m - 1 - j), (n - 1 - i, j), (n - 1 - i, m - 1 - j)]
        cnt = Counter()
        for x, y in coords:
            cnt[grid[x][y]] += 1
        groups.append(cnt)
letters = sorted(targets.keys())
L = len(letters)
N_nodes = 1 + G + L + 1
s = 0
t = N_nodes - 1
graph = [[] for _ in range(N_nodes)]
for g in range(G):
    add_edge(graph, s, 1 + g, 1, 0)
for g in range(G):
    for li, letter in enumerate(letters):
        cost = 4 - groups[g].get(letter, 0)
        add_edge(graph, 1 + g, 1 + G + li, 1, cost)
for li, letter in enumerate(letters):
    add_edge(graph, 1 + G + li, t, targets[letter], 0)
flow_needed = G
result = min_cost_flow(N_nodes, graph, s, t, flow_needed)
print(result)
