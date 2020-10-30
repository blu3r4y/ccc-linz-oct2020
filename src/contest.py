import numpy as np
from pprint import pprint

from constants import *


def solve(data: Data):
    prices = np.array(data.prices)

    result: [DrainTask] = {t.id: DrainTask(t.id, []) for t in data.tasks}

    # store drained power per minute
    powers = np.zeros(len(data.prices), dtype=int)

    # start with most peaky tasks
    tasks = sorted(data.tasks, key=lambda t: t.end - t.start)
    for task in tasks:
        price_window = prices[task.start:task.end + 1]  # we can drain from this area

        # fill power hunger
        filled = 0
        while filled < task.power:
            cheapest_index = np.argmin(price_window) + task.start
            if powers[cheapest_index] <= data.max_power:
                # how much power do we need and can we drain at a maximum here?
                leftover = task.power - filled
                amount = min(data.max_power - powers[cheapest_index], leftover)

                # okay, let's drain it
                powers[cheapest_index] += amount
                result[task.id].drains.append(DrainPower(cheapest_index, amount))
                filled += amount

                # is this minute no exhausted?
                if powers[cheapest_index] == data.max_power:
                    prices[cheapest_index] = 1e8

    # convert to list
    result = result.values()

    # for task in data.tasks:
    #    window = prices[task.start:task.end + 1]
    #    start_id = np.argmin(window) + task.start
    #    start_times.append("{} {} {}".format(task.id, start_id, task.power))

    check_constraints(data, result, verbose=True)

    # format output
    output = "{}\n".format(len(result))
    output += "\n".join(["{} {}".format(t.id, " ".join(["{} {}".format(d.minute, d.power) for d in t.drains]))
                         for t in result])
    return output


def check_constraints(data: Data, result: [DrainTask], verbose=False):
    # check per minute constraint
    powers = np.zeros(len(data.prices), dtype=int)
    for task in result:
        for drain in task.drains:
            powers[drain.minute] += drain.power

    # check electricity bill
    bill = np.sum(powers * np.array(data.prices))

    if verbose:
        print("prices: {}".format(data.prices))
        print("powers: {}".format(powers))
        print("bill: {}".format(bill))

    assert np.all(powers <= data.max_power)
    assert bill <= data.max_bill


def sliding_window(arr, window_size):
    return np.convolve(arr, np.ones(window_size), mode='valid')
