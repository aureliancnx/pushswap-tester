import os
import glob
import time
import math
import random
import subprocess

tests_ko = 0
tests_ok = 0
tests = 0

def get_output(numbers):
    args = ['../push_swap']
    [args.append(str(i)) for i in numbers]
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    line = proc.stdout.read()
    line = line.decode("utf-8")[:-1]
    return line

def rotate(l, n):
    return l[n:] + l[:n]

def sort_swap(arr, px, py):
    arr[px], arr[py] = arr[py], arr[px]

def pop_insert(arr, arr1):
    arr1.insert(0, arr[0])
    del arr[0]

def sort_check(output, numbers):
    la = [i for i in numbers]
    lb = []
    actions = output.split(' ')
    acts = ['sa', 'sb', 'sc', 'pa', 'pb', 'ra', 'rb', 'rr', 'rra', 'rrb', 'rrr']
    for act in actions:
        if act == 'sa': sort_swap(la, 0, 1)
        if act == 'sb': sort_swap(lb, 0, 1)
        if act == 'sc': sort_swap(la, 0, 1), sort_swap(lb, 0, 1)
        if act == 'pa': pop_insert(lb, la)
        if act == 'pb': pop_insert(la, lb)
        if act == 'ra': la = rotate(la, 1)
        if act == 'rb': lb = rotate(lb, 1)
        if act == 'rr': la, lb = rotate(la, 1), rotate(lb, 1)
        if act == 'rra': la = rotate(la, -1)
        if act == 'rrb': lb = rotate(lb, -1)
        if act == 'rrr': la, lb = rotate(la, -1), rotate(lb, -1)
        if act != '' and not act in acts:
            print('WEIRD ACTION: "{0}"'.format(act))
            return 0
    if sorted(la) != la:
        return 0
    return 1

def check(test_name, numbers):
    global tests
    global tests_ko
    global tests_ok
    tm = time.time()
    if len(numbers) > 10000:
        return
    try:
        output = get_output(numbers)
    except:
        print("\033[0;36mTest: {:>65s} | \033[0mNUMBERS = {:-8.0f} | \033[0;31mCRASHED\033[0m".format(test_name, len(numbers)))
        tests_ko += 1
        tests += 1
        return
    tm = time.time() - tm
    actions = len(output.split(' '))
    actions = 0 if len(output) < 2 else actions
    numb = actions / len(numbers)
    o_npow = pow(len(numbers), 2)
    o_nlog = len(numbers) * math.log(len(numbers))
    o_nlog = 1 if o_nlog < 1 else o_nlog * 15
    k_lvl = 3 if actions > pow(len(numbers), 2) else 2 if actions > o_nlog else 1
    status = "?"
    sorted = sort_check(output, numbers)
    if k_lvl == 3:
        status = "\033[0;31mNOT OPTIMIZED! O(n^2) x{0}".format(actions / pow(len(numbers), 2))
    elif k_lvl == 2:
        status = "\033[0;33mNOT OPTIMIZED ENOUGH! O(nlog(n)) x{0}".format(round(actions / o_nlog, 2))
    else:
        status = "\033[0;32mOPTIMIZED"
    if not sorted:
        status = "\033[0;31mNOT SORTED!!!"
    print("\033[0;36mTest: {:>65s} | \033[0mNUMBERS = {:-8.0f} | ACTIONS = {:-8.0f} | {:4.2f}s | {:s}\033[0m".format(test_name, len(numbers), actions, tm, status))
    if sorted and k_lvl == 1:
        tests_ko += 1
    else:
        tests_ok += 1
    tests += 1

def check_unsorted_r():
    ncounts = [1, 2, 10, 50, 100, 500, 1000, 2000, 5000, 10000]
    for sz in ncounts:
        for i in range(0, 5):
            nmb = []
            r = 0
            while r != sz:
                rd = random.randrange(1, 99999999)
                if rd in nmb:
                    continue
                nmb.append(rd)
                r += 1
            check("", nmb)

def check_batch_file(file_name):
    content = open(file_name).read()
    content = content.split(' ')
    nm = [int(i) for i in content]
    test_name = file_name.replace("tests-batch/", "").split('.')[0]
    check(test_name, nm)

def check_batch():
    for files in glob.glob('tests-batch/*'):
        check_batch_file(files)

def main():
    check_batch()
    check_unsorted_r()
    if tests_ko > 0:
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
