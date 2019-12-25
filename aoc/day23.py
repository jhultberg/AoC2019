from .intcode import run
from collections import deque
from itertools import count
from copy import deepcopy
import threading
from queue import Queue


class Network:
    def __init__(self, program, no_dics):
        self.program = program
        self.no_dics = no_dics
        self.dics = {}
        self.queues = {}

    def run_dics(self, nat_mode=False):
        q = Queue()
        nat = None
        latest = None
        for i in range(self.no_dics):
            self.queues[i] = deque([i])
            self.dics[i] = threading.Thread(target=self.dic, args=(i, q))
        for _, dic in self.dics.items():
            dic.start()

        for i in count():
            idle = True
            for _, que in self.queues.items():
                if que:
                    idle = False
            if i != 0 and idle:
                if latest and nat[1] == latest[1]:
                    return latest[1]
                latest = nat
                self.queues[0].append(nat)

            item = q.get()
            address = item[0]
            x = item[1]
            y = item[2]
            if address == 255:
                if not nat_mode:
                    return y
                nat = (x, y)
                continue

            self.queues[address].append((x, y))

    def dic(self, i, queue):
        d = run(deepcopy(self.program), move(self.queues[i]))
        while True:
            try:
                address = next(d)
                x = next(d)
                y = next(d)
                queue.put((address, x, y))
            except StopIteration:
                print("fail", i)
            finally:
                queue.task_done()


def move(queue):
    while True:
        if len(queue) == 0:
            yield -1
        else:
            if isinstance(queue[0], tuple):
                yield queue[0][0]
                yield queue[0][1]
                queue.popleft()
            else:
                yield queue.popleft()


def solve(path):
    with open(path) as f:
        input = f.read().rstrip().split(",")
    program = []
    for instruction in input:
        program.append(int(instruction))

    a = Network(program, 50).run_dics()
    b = Network(program, 50).run_dics(nat_mode=True)

    return (a, b)
