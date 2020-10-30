import numpy as np
from pprint import pprint

from constants import *


def solve(data: Data):
    prices = np.array(data.prices)

    result: [DrainTask] = {t.id: DrainTask(t.id, []) for t in data.tasks}

    # store drained power per minute
    powers = np.zeros(len(data.prices), dtype=int)
    # and number of tasks already assigned per minute
    ntasks = np.zeros(len(data.prices), dtype=int)

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
                ntasks[cheapest_index] += 1
                result[task.id].drains.append(DrainPower(cheapest_index, amount))
                filled += amount

                # is this minute now exhausted?
                if powers[cheapest_index] == data.max_power \
                        or ntasks[cheapest_index] == data.max_concurrent:
                    prices[cheapest_index] = 1e8  # ... make sure this price is never chosen again

    # convert to list
    result = result.values()

    check_constraints(data, result, verbose=True)

    # format output
    output = "{}\n".format(len(result))
    output += "\n".join(["{} {}".format(t.id, " ".join(["{} {}".format(d.minute, d.power) for d in t.drains]))
                         for t in result])
    return output


def check_constraints(data: Data, result: [DrainTask], verbose=False):
    # check per minute and max-task constraint
    powers = np.zeros(len(data.prices), dtype=int)
    ntasks = np.zeros(len(data.prices), dtype=int)
    for task in result:
        for drain in task.drains:
            powers[drain.minute] += drain.power
            ntasks[drain.minute] += 1

    # check electricity bill
    bill = np.sum(powers * np.array(data.prices))

    if verbose:
        print("prices: {}".format(data.prices))
        print("powers: {}".format(powers))
        print("ntasks: {}".format(ntasks))
        print("bill: {}".format(bill))

    assert np.all(powers <= data.max_power)
    assert np.all(ntasks <= data.max_concurrent)
    assert bill <= data.max_bill


def sliding_window(arr, window_size):
    return np.convolve(arr, np.ones(window_size), mode='valid')
