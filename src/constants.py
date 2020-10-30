from collections import namedtuple

Data = namedtuple("Data", ["max_power", "max_bill", "max_concurrent", "prices", "tasks"])
Task = namedtuple("Task", ["id", "power", "start", "end"])

# output structures
DrainPower = namedtuple("DrainPower", ["minute", "power"])
DrainTask = namedtuple("DrainTask", ["id", "drains"])
