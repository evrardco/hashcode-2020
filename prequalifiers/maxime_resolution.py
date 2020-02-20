def get_data(input_filepath):
    f = open(input_filepath, "r")
    max_slices = int(f.readline().rstrip("\n").split(" ")[0])
    pizzas = f.readline().rstrip("\n").split(" ")
    pizzas = [int(i) for i in pizzas]
    return pizzas, max_slices


def solve(pizzas, max_slices):
    slice_count = 0
    for i in range(len(pizzas) - 1, -1, -1):
        if (slice_count + pizzas[i] <= max_slices):
            slice_count += pizzas[i]

    return slice_count


# like 'solve' but cycle through the 'pizza' list and compare
def solve_better(pizzas, max_slices):
    length = len(pizzas)
    best_slice_count = 0
    best_pizzas_to_buy = []
    for i in range(length):
        slice_count = 0
        pizzas_to_buy = []

        iter_count = 0
        while iter_count < length:
            idx = i % length
            if (slice_count + pizzas[idx] <= max_slices):
                slice_count += pizzas[idx]
                pizzas_to_buy.append(idx)
            i -= 1
            iter_count += 1

        if slice_count > best_slice_count:
            best_slice_count = slice_count
            best_pizzas_to_buy = pizzas_to_buy

        if best_slice_count == max_slices:
            break

    # best_pizzas_to_buy.sort()
    return best_pizzas_to_buy, best_slice_count


def list_check_no_dups(list):
    return len(list) == len(set(list))


if __name__ == '__main__':
    inputs = [
        "a_example.in",
        "b_small.in",
        "c_medium.in",
        "d_quite_big.in",
        "e_also_big.in"
    ]
    for i in inputs:
        pizzas, max_slices = get_data(i)
        pizzas_to_buy, slice_count = solve_better(pizzas, max_slices)
        if list_check_no_dups(pizzas_to_buy):
            print("{}:\t{}".format(i, slice_count))
        else:
            print("{}:\tFAILED: pizza duplicates found".format(i))
