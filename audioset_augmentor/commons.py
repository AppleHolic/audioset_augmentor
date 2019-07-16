import multiprocessing
import time
from typing import Callable, List, Any


def do_multiprocess(worker_func: Callable, inputs: List[Any], num_proc: int = None,
                    delay: float = 0.0, multiply: int = 1):

    # declare pool
    num_proc = num_proc if num_proc else multiprocessing.cpu_count() // 2

    with multiprocessing.Pool(num_proc) as pool:
        for i in range(0, len(list(inputs)), num_proc * multiply):
            # chunk 로 나누기.
            start_idx, end_idx = i, i + num_proc * multiply
            # multi-processing 으로 worker 실행.
            pool.map(worker_func, inputs[start_idx:end_idx])
            print('{}/{}\t{}() processed.'.format(i + 1, len(inputs), worker_func.__name__))

            if delay:
                time.sleep(delay)
