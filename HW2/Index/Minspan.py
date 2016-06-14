import sys
import copy

def rangeWindow(positions):
    pointers = {}

    for w, pos in positions.iteritems():
        pointers[w] = [0, len(pos)]

    if len(pointers) == 1:
        return 100

    minspan = 10000
    while not windowsEnded(pointers) and len(checkWindow(pointers)) > 1:
        active_pointers = checkWindow(pointers)
        values = get_values(active_pointers, positions)
        min_key = min(values, key=values.get)
        max_key = max(values, key=values.get)
        new_minspan = positions[max_key][pointers[max_key][0]] - positions[min_key][pointers[min_key][0]]
        if new_minspan < minspan:
            minspan = new_minspan
        pointers[min_key][0] += 1
    return minspan


def windowsEnded(pointers):
    for w, lst in pointers.iteritems():
        if lst[0] + 1 != lst[1]:
            return False
    return True


def get_values(pointers, positions):
    values = {}
    for w, lst in pointers.iteritems():
        values[w] = positions[w][lst[0]]

    return values


def checkWindow(pointers):
    copy_ptrs = copy.deepcopy(pointers)
    for w, lst in pointers.iteritems():
        if lst[0] + 1 == lst[1]:
            del copy_ptrs[w]

    return copy_ptrs


# positions = {'pudding': [1,3,6,9], 'pops':[4,8,16,21], 'cheap': [0,5,10,15]}
# print rangeWindow(positions)
