from concurrent.futures import ThreadPoolExecutor
import time
import os


# 模拟 CPU 密集型任务
def cpu_task(x):
    s = 0
    for i in range(10**7):
        s += i * x
    return s


# 模拟 I/O 密集型任务
def io_task(x):
    time.sleep(0.5)  # 模拟 I/O 操作
    return x


# 任务类型选择：'cpu' 或 'io'
task_type = "cpu"  # 改成 'io' 看效果
task = cpu_task if task_type == "cpu" else io_task

# 测试不同 max_workers
for max_workers in [4, 8, 16, 32, 64, 128, 256, 512]:
    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(task, range(32)))  # 执行 32 个任务
    print(f"max_workers={max_workers}, time={time.time() - start:.2f} seconds")
