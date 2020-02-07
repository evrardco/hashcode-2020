import sys
from collections import deque
import itertools as iter
import functools 
dict_a = {}
def find_sol(pivot_b, pizzas, W, offset=0):
    count = 0
    p_count = 0

    for i in range(len(pizzas) - 1, pivot_b, -1):

        if count + pizzas[i] > W:
            break
        count += pizzas[i]
        p_count += 1

    pivot_a = 0  # index du premier qui depasse
    best = (count, p_count, pivot_a)
    while pivot_a <= pivot_b - 1 and pivot_a < len(pizzas) and count + pizzas[pivot_a] < W:
        pivot_a += 1
    while pivot_a >= 0:
        new_sol = find_sol_smaller(pivot_a, pizzas, W, count, p_count)
        best = new_sol if best[0] <= new_sol[0] else best
        pivot_a -= 1
    return best
    # return find_sol_smaller(pivot_a, pizzas, W, count, p_count)


def find_sol_smaller(pivot_a, pizzas, W, bigger_count, bigger_p_count):
    if pivot_a in dict_a:
        count, p_count = dict_a[pivot_a]
        return (count + bigger_count, p_count + bigger_p_count, pivot_a)
    count = 0
    p_count = 0
    for i in range(pivot_a, 1, -1):
        if bigger_count + count + pizzas[i] > W:
            break
        count += pizzas[i]
        p_count += 1
    dict_a[pivot_a] = (count, p_count)
    return (count + bigger_count, p_count + bigger_p_count, pivot_a)


def compute_sol(pivot_b, pizzas, W):
    best = (0, 0, 0)
    while pivot_b < len(pizzas):
        if pivot_b % 128 == 0:
            print(f"progress: {pivot_b}/{len(pizzas)}")
        new_sol = find_sol(pivot_b, pizzas, W)
        best = new_sol if best[0] <= new_sol[0] else best
        pivot_b += 1
    return best


def rec_sol(max_W, pizzas):
    best = (0, 0, 0)
    max_depth = 10

    def helper(W, subarray, depth, prev_count, best):
        if depth == max_depth:
            return best
        pivot_b = len(subarray) - 1
        count = 0
        while count + subarray[pivot_b] < W:
            count = count + subarray[pivot_b]
            pivot_b -= 1
        print(pivot_b)
        candidate = compute_sol(pivot_b, pizzas, W)
        best = candidate if best[0] < candidate[0] else best
        print(best)
        print(candidate)
        helper(W - candidate[0], subarray[::candidate[2]],
               depth + 1, candidate[0], best)
    return helper(max_W, pizzas, 0, 0, best)


def naive_solver(slices, pizzas):
    used, unused = [], []
    count = 0
    pivot = 0

    for i in range(len(pizzas) - 1, 0, -1):
        if count + pizzas[i] > slices:
            break
        count = count + pizzas[i]
        pivot = i
        used.append(pizzas[i])
    
    for i in range(0, pivot):
        if count + pizzas[i] > slices:
            break
        count = count + pizzas[i]
        used.append(pizzas[i])
    
    for i in range(len(pizzas)):
        if i not in used:
            unused.append(pizzas[i])
    
    return (count, used, unused)
    
class Node:
    def __init__(self, state, depth, best):
        self.depth = 0
        self.state = state
        self.best = best

    def expand(self):
        for next in self.state.successors():
            yield Node(next, self.depth + 1, max(next.count, self.best))


class State:

    def __init__(self, count, used, unused):
        self.used = used
        self.unused = unused
        self.count = count

    def successors(self):

        for i in range(len(self.used)):
            for j in range(len(self.unused)):
                yield self.swap(i, j)

    def swap(self, i, j):
        s = State(self.count, [x for x in self.used], [x for x in self.unused])
        s.count -= s.used[i]
        s.unused.append(s.used[i])
        del(s.used[i])

        s.count += s.unused[j]
        s.used.append(s.unused[j])
        del(s.unused[j])

        return s
    def __hash__(self):
        return hash(functools.reduce(lambda x, y: x + y, self.used))
    
    def __eq__(self, other):
        s1 = functools.reduce(lambda x, y: x + y, self.used)
        s1 += functools.reduce(lambda x, y: x + y, self.unused)
        s2 = functools.reduce(lambda x, y: x + y, other.used)
        s2 += functools.reduce(lambda x, y: x + y, other.unused)
        return s1 == s2


def bfs(root, objective, max_depth=1000):

    best = root
    fringe = deque([root])

    depth = 0

    explored_set = {}
    while fringe:
        n = fringe.pop()
        if n in explored_set:
            continue
        if n.best == objective:
            return n
        best = n if n.best > best.best else best
        print(n.depth)
        if n.depth < max_depth:
            fringe.extend(n.expand())
            depth = depth + 1
        else:
            explored_set[n] = n.best
            print("added to explored_set")
    return best
        


if __name__ == "__main__":

    path = sys.argv[1]
    slices = None
    pizzas = None
    with open(path) as f:
        slices = int(f.readline().split(' ')[0])
        pizzas = f.readline().rstrip().split(' ')
    pizzas = [int(p) for p in pizzas]
    pizzas_reversed = sorted(pizzas, key=lambda x: -x)
    bigger_count = 0  # slices prises aux pizzas les plus grandes
    i = 0
    while bigger_count + pizzas_reversed[i] < slices:
        bigger_count = bigger_count + pizzas_reversed[i]
        i = i + 1

    pivot_b = i

    # res = compute_sol(pivot_b, pizzas, slices)
    # #res = rec_sol(slices, pizzas)
    naive_sol = naive_solver(slices, pizzas)
    res = bfs(Node(State(*naive_sol), 0, naive_sol[0]), slices)
    print(res.count)
