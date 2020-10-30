import numpy as np


def solve(data):
    prices = data["prices"]

    start_times = []

    for task in data["tasks"]:
        window = prices[task.start:task.end + 1]
        start_id = np.argmin(window) + task.start
        start_times.append("{} {} {}".format(task.id, start_id, task.power))

    return "{}\n".format(len(start_times)) + "\n".join(start_times)


def sliding_window(arr, window_size):
    windows = np.convolve(arr, np.ones(window_size), mode='valid')
    return windows
