import os
from pprint import pprint

from contest import solve
from constants import *


def load(data):
    max_power = int(data[0])
    max_bill = int(data[1])
    max_concurrent = int(data[2])
    n = int(data[3])
    m = int(data[4 + n])

    prices = list(map(int, data[4:n + 4]))
    tasks = [
        Task(id=int(e.split()[0]),
             power=int(e.split()[1]),
             start=int(e.split()[2]),
             end=int(e.split()[3]))
        for e in data[n + 5:n + 5 + m]
    ]

    return Data(max_power=max_power,
                max_bill=max_bill,
                max_concurrent=max_concurrent,
                prices=prices,
                tasks=tasks)


if __name__ == "__main__":
    level, quests = 6, 5
    for q in range(5, quests + 1):
        if q == 0:
            q = "example"

        input_file = r'..\data\level{0}\level{0}_{1}.in'.format(level, q)
        output_file = os.path.splitext(input_file)[0] + ".out"

        with open(input_file, 'r') as fi:
            data = load(fi.read().splitlines())
            pprint(data)

            print("=== Input {}".format(q))
            print("======================")

            result = solve(data)
            # pprint(result)

            with open(output_file, 'w+') as fo:
                fo.write(result)
