from pprint import pprint

import numpy as np
import random

from constants import *


def solve(data: Data):
    prices = np.array(data.prices, dtype=np.float64)

    result: [DrainTask] = {t.id: DrainTask(t.id, {}) for t in data.tasks}

    # store drained power per minute
    powers = np.zeros(len(data.prices), dtype=np.int)
    # and number of tasks already assigned per minute
    ntasks = np.zeros(len(data.prices), dtype=np.int)

    # start with most peaky tasks
    tasks = sorted(data.tasks, key=lambda t: t.end - t.start)
    for task in tasks:
        # we can only drain from this area
        price_window = prices[task.start:task.end + 1].copy()
        width = task.end - task.start

        # fill power hunger
        filled = 0
        chosen = set()
        while filled < task.power:

            # find the cheapest index
            assert np.any(np.isfinite(price_window))
            idx = np.nanargmin(price_window) + task.start

            # we still got some power and tasks left to fill here
            assert powers[idx] < data.max_power
            assert ntasks[idx] < data.max_concurrent

            # how much power do we need and can we drain at a maximum here?
            leftover = task.power - filled
            limit = int(0.2 * data.max_power)
            amount = min(data.max_power - powers[idx], leftover, limit)

            assert amount > 0

            # okay, let's drain that amount
            powers[idx] += amount
            filled += amount
            if idx in chosen:
                # overwrite existing indexes
                existing = result[task.id].drains[idx]
                result[task.id].drains[idx] = DrainPower(idx, existing.power + amount)
            else:
                # create new indexes
                ntasks[idx] += 1
                result[task.id].drains[idx] = DrainPower(idx, amount)
                chosen.add(idx)

            if width > 100:
                price_window[idx - task.start] = np.nan

            # is this minute now exhausted?
            if powers[idx] >= data.max_power \
                    or ntasks[idx] >= data.max_concurrent:
                prices[idx] = np.nan
                price_window[idx - task.start] = np.nan

        assert filled == task.power

    # convert to list
    result = result.values()

    check_constraints(data, result, verbose=True)

    # format output
    output = "{}\n".format(len(result))
    output += "\n".join(["{} {}".format(t.id, " ".join(["{} {}".format(d.minute, d.power) for d in t.drains.values()]))
                         for t in result])
    return output


def check_constraints(data: Data, result: [DrainTask], verbose=False):
    # check per minute and max-task constraint
    powers = np.zeros(len(data.prices), dtype=np.int)
    ntasks = np.zeros(len(data.prices), dtype=np.int)
    for task in result:
        used_minutes_for_task = []
        for drain in task.drains.values():
            powers[drain.minute] += drain.power
            ntasks[drain.minute] += 1
            used_minutes_for_task.append(drain.minute)

        # assert that we do not use something twice (should really not happen)
        if len(set(used_minutes_for_task)) != len(used_minutes_for_task):
            pprint(task)
            assert len(set(used_minutes_for_task)) == len(used_minutes_for_task)

    assert len(data.prices) == powers.shape[0]

    # check electricity bill
    bill = np.sum(powers * np.rint(np.array(data.prices) * (1.0 + (powers / data.max_power))))

    if verbose:
        print("prices: {}".format(data.prices))
        print("powers: {}".format(powers.tolist()))
        print("ntasks: {}".format(ntasks.tolist()))
        print("bill: {}".format(bill))

    assert np.all(powers <= data.max_power)
    assert np.all(ntasks <= data.max_concurrent)
    assert bill <= data.max_bill


def sliding_window(arr, window_size):
    return np.convolve(arr, np.ones(window_size), mode='valid')
