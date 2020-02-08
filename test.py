import sys
from collections import deque
import itertools as iter
import functools 
import math
from queue import PriorityQueue
from array import *
DICT_ACCESSES = 0
COLLS = 0
def naive_solver(slices, pizzas):
    used, unused = [], []
    count = 0
    pivot = 0

    for i in range(len(pizzas) - 1, 0, -1):
        if count + pizzas[i] > slices:
            break
        count = count + pizzas[i]
        pivot = i
        used.append(i)
    
    for i in range(0, pivot):
        if count + pizzas[i] > slices:
            break
        count = count + pizzas[i]
        used.append(i)
    
    for i in range(len(pizzas)):
        if i not in used:
            unused.append(i)
    
    return (count, used, unused)
    
class Node:
    def __init__(self, state, depth, best):
        self.depth = depth
        self.state = state
        self.best = best
        self.pizzas = pizzas

    def expand(self):
        for next in self.state.successors():
            yield Node(next, self.depth + 1, max(next.count, self.best))
    
    def __lt__(self, other):
        return self.state.count < other.state.count


class State:

    def __init__(self, count, used, unused, pizzas, goal):
        self.used = used
        self.unused = unused
        self.count = count
        self.swapped_in = []
        self.swapped_out = []
        self.pizzas = pizzas
        self.goal = goal
        self.biggest_unused = len(unused) - 1
        
    def successors(self):
        for i in range(len(pizzas) - 1, 0, -1):
            if self.can_remove(i):
                yield self.remove_pizza(i)
            if self.can_add(i):
                yield self.add_pizza(i)    

    def can_remove(self, i):

        return ((i in self.used and i not in self.swapped_out) or i in self.swapped_in) and self.count - self.pizzas[i] > 0

    def remove_pizza(self, i):

        s = State(self.count - self.pizzas[i], self.used, self.unused, self.pizzas, self.goal)
        s.swapped_in = array('I', self.swapped_in)
        s.swapped_out = array('I', self.swapped_out)
        if i in s.swapped_in:
            s.swapped_in.remove(i)
        else:
            s.swapped_out.append(i)
        return s
    
    def can_add(self, i):

        return ((i in self.unused and i not in self.swapped_in) or i in self.swapped_out) and self.count + self.pizzas[i] <= self.goal

    def add_pizza(self, i):
        s = State(self.count + self.pizzas[i], self.used, self.unused, self.pizzas, self.goal)
        s.swapped_in = self.swapped_in.__copy__()
        s.swapped_out = self.swapped_out.__copy__()
        if i in s.swapped_out:
            s.swapped_out.remove(i)
        else:
            s.swapped_in.append(i)
        return s
         

    def __hash__(self):
        global DICT_ACCESSES
        DICT_ACCESSES = DICT_ACCESSES + 1
        return hash(self.count)
    
    def __eq__(self, other):
        global COLLS
        COLLS += 1
        return set(self.swapped_in) == set(other.swapped_in) and set(self.swapped_out) == set(other.swapped_out)


def best_first_graph_search(root, objective, f, max_depth=1000):
    global COLLS, DICT_ACCESSES
    best = root.state
    fringe = PriorityQueue()
    fringe.put((f(root), root))


    explored_set = {}
    for i in range(len(pizzas)):
        explored_set[i] = False
    for i in range(len(pizzas)):
        del explored_set[i]
    iterations = 0
    while not fringe.empty():
        iterations += 1
        h_val, n = fringe.get(0)
        if iterations % (100) == 0:
            print( f"best is {best.count}")
            print(f"current is {n.state.count}")
            print(f"Collision rate: {COLLS/DICT_ACCESSES}")
            DICT_ACCESSES = 0
            COLLS = 0
        if n.state in explored_set:
            continue
        if n.best == objective:
            return n
        best = n.state if n.state.count > best.count else best
        if n.depth < max_depth:
            for node in n.expand():
                if node.state.count == objective:
                    return node
                fringe.put((f(node), node))
        
        explored_set[n.state] = True
    return best


if __name__ == "__main__":

    path = sys.argv[1]
    slices = None
    pizzas = None
    with open(path) as f:
        slices = int(f.readline().split(' ')[0])
        pizzas = f.readline().rstrip().split(' ')
    pizzas = array('I', [int(p) for p in pizzas])
    pizzas_reversed = sorted(pizzas, key=lambda x: -x)
    bigger_count = 0  # slices prises aux pizzas les plus grandes
    i = 0
    while bigger_count + pizzas_reversed[i] < slices:
        bigger_count = bigger_count + pizzas_reversed[i]
        i = i + 1

    pivot_b = i

    l = []
    count = 0
    def evaluate(state):
        
        filtered = filter(lambda el: el not in state.swapped_in, state.unused)
        s = sum(filtered) + sum(state.unused)
        dist = (slices - state.count)
        return 0 if dist == 0 else dist + s

    def fun(node):
        return node.depth + evaluate(node.state)

    naive_sol = naive_solver(slices, pizzas)
    count = naive_sol[0] 
    used = sorted(naive_sol[1])
    unused = sorted(naive_sol[2])
    root = Node(State(count, used, unused, pizzas, slices), 0, naive_sol[0])

    # count = 0
    # used = [0]
    # unused = [i for i in range(1, len(pizzas))]
    # root = Node(State(count, used, unused, pizzas, slices), 0, naive_sol[0])


    print(l)
    
    print(best_first_graph_search(root, slices, fun, max_depth=15).state.count)
    #print(res.count)
