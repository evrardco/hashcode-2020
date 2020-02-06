import sys
dict_a = {}

def find_sol(pivot_b, pizzas, W):
    count = 0
    p_count = 0

    for i in range(len(pizzas) - 1, pivot_b, -1):

        if count + pizzas[i] > W:
            break
        count += pizzas[i]
        p_count += 1
        
    best = (count, p_count)

    pivot_a = 0 #index du premier qui depasse
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
        return (count + bigger_count, p_count + bigger_p_count)
    count = 0
    p_count = 0
    for i in range(pivot_a, 1, -1):
        if bigger_count + count + pizzas[i] > W:
            break
        count += pizzas[i]
        p_count += 1
    dict_a[pivot_a] = (count, p_count)
    return (count + bigger_count, p_count + bigger_p_count)

def compute_sol(pivot_b, pizzas, W):
    best = (0, 0)
    while pivot_b < len(pizzas):
        if pivot_b % 100 == 0:
            print(f"progress: {pivot_b}/{len(pizzas)}")
        new_sol = find_sol( pivot_b, pizzas, W)
        #print(new_sol)
        best = new_sol if best[0] <= new_sol[0] else best
        pivot_b += 1
        #print(f"pivot_b={pivot_b}")
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
    bigger_count = 0 #slices prises aux pizzas les plus grandes
    i = 0
    while bigger_count + pizzas_reversed[i] < slices:
        bigger_count = bigger_count + pizzas_reversed[i]
        i = i + 1

    pivot_b = i

    res = compute_sol(pivot_b, pizzas, slices)
    print(res)
    # pivot = j
    # best = (i, bigger_count)
    # while pivot >= 0:
    #     pivot = pivot - 1
    #     print(f"trying pivot={pivot}")
    #     k = pivot
    #     count = bigger_count

    #     while count + pizzas[k] < slices:
    #         count = count + pizzas[k]
    #         k = k - 1
    #     print(f"found sol={count}")
    #     if count > best[1]:
    #         best = (i + (pivot - k), count)
    # print(best)


# def printknapSack(W, wt, val, n):
#     K = [[0 for w in range(W + 1)]
#          for i in range(n + 1)]

#     # Build table K[][] in bottom
#     # up manner
#     for i in range(n + 1):
#         for w in range(W + 1):
#             if i == 0 or w == 0:
#                 K[i][w] = 0
#             elif wt[i - 1] <= w:
#                 K[i][w] = max(val[i - 1]
#                               + K[i - 1][w - wt[i - 1]],
#                               K[i - 1][w])
#             else:
#                 K[i][w] = K[i - 1][w]

#     # stores the result of Knapsack
#     res = K[n][W]

#     w = W
#     for i in range(n, 0, -1):
#         if res <= 0:
#             break
#         # either the result comes from the
#         # top (K[i-1][w]) or from (val[i-1]
#         # + K[i-1] [w-wt[i-1]]) as in Knapsack
#         # table. If it comes from the latter
#         # one/ it means the item is included.
#         if res == K[i - 1][w]:
#             continue
#         else:

#             # This item is included.
#             print(wt[i - 1])

#             # Since this weight is included
#             # its value is deducted
#             res = res - val[i - 1]
#             w = w - wt[i - 1]

# wt = [1 for i in range(len(pizzas))]
# n = len(pizzas)

# printknapSack(slices, wt, pizzas, n)