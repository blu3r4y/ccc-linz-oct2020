import os
from pprint import pprint

from contest import solve
from constants import *


def load(data):
    max_power = int(data[0])
    max_bill = int(data[1])
    n = int(data[2])
    m = int(data[3 + n])

    prices = list(map(int, data[3:n + 3]))
    tasks = [
        Task(id=int(e.split()[0]),
             power=int(e.split()[1]),
             start=int(e.split()[2]),
             end=int(e.split()[3]))
        for e in data[n + 4:n + 4 + m]
    ]

    return Data(max_power=max_power,
                max_bill=max_bill,
                prices=prices,
                tasks=tasks)


if __name__ == "__main__":
    level, quests = 4, 5
    for q in range(0, quests + 1):
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
            pprint(result)

            with open(output_file, 'w+') as fo:
                fo.write(result)
