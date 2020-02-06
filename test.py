import sys
dict_a = {}

def find_sol(pivot_b, pizzas, W, offset=0):
    count = 0
    p_count = 0

    for i in range(len(pizzas) - 1 , pivot_b, -1):

        if count + pizzas[i] > W:
            break
        count += pizzas[i]
        p_count += 1
        

    pivot_a = 0 #index du premier qui depasse
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
        new_sol = find_sol( pivot_b, pizzas, W)
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
        helper(W - candidate[0], subarray[::candidate[2]], depth + 1, candidate[0], best)
    return helper(max_W, pizzas, 0, 0, best)
    

        

if __name__ == "__main__":

    path = sys.argv[1]
    slices = None
    pizzas = None
    with open(path) as f:
        slices = int(f.readline().split(' ')[0])
        pizzas = f.readline().rstrip().split(' ')
    pizzas = [int(p) for p in pizzas]
    pizzas_reversed = sorted(pizzas, key=lambda x: -x)
    bigger_count = 0 #slices prises aux pizzas les plus grandes
    i = 0
    while bigger_count + pizzas_reversed[i] < slices:
        bigger_count = bigger_count + pizzas_reversed[i]
        i = i + 1

    pivot_b = i

    res = compute_sol(pivot_b, pizzas, slices)
    #res = rec_sol(slices, pizzas)
    print(res)
