from concurrent.futures import ThreadPoolExecutor
import time


def cpu_task(x):
    s = 0
    for i in range(10**7):
        s += i * x
    return s


task_type = "cpu"

if task_type == "cpu":
    task = cpu_task

for max_workers in [4, 8, 16, 32, 64, 128, 256, 512]:
    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(task, range(32)))
    print(f"max_workers={max_workers}, time={time.time() - start:.2f} seconds")
