from .intcode import run
from collections import deque
from itertools import count
from pprint import pprint
from copy import deepcopy
import threading
from queue import Queue


class Network:
    def __init__(self, program, no_dics):
        self.program = program
        self.no_dics = no_dics
        self.dics = {}
        self.queues = {}

    def run_dics(self):
        q = Queue()
        for i in range(self.no_dics):
            self.queues[i] = deque([i])
            self.dics[i] = threading.Thread(target=self.dic, args=(i, q))
        for _, dic in self.dics.items():
            dic.start()

        for i in count():
            item = q.get()
            address = item[0]
            x = item[1]
            y = item[2]
            if address == 255:
                # for thread in self.dics.items():
                #    print("hjkh")
                #    thread[1].join()
                return y
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

    return (a, None)
