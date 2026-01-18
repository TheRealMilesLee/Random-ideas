# -*- coding: utf-8 -*-
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPICS = ["test-topic", "test-topic-2", "test-topic-3"]  # 可按需在此列表中添加更多 topic
MAX_WORKERS = 20  # 提升并发度
SEND_INTERVAL = 0  # 发送间隔(秒)，0 表示不主动 sleep
BATCH_SIZE = 1000
TOTAL = 100000

# KafkaProducer 是线程安全的，可以在多线程中共享
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: v.encode('utf-8'),
    # 优化性能配置
    batch_size=16384,
    linger_ms=10,
    buffer_memory=33554432)

# 用于线程安全的打印
print_lock = threading.Lock()


def send_message(i):
  """线程函数：发送消息"""
  topic = random.choice(TOPICS)
  msg = "FAST MSG {}".format(i)

  # 异步发送，不阻塞
  future = producer.send(topic, msg)

  # 线程安全的打印
  with print_lock:
    print("[Producer] Thread-{} Sent to {}: {}".format(i, topic, msg))
  if SEND_INTERVAL:
    time.sleep(SEND_INTERVAL)
  return i


with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
  # 分批提交任务，避免一次性创建太多Future对象
  batch_size = BATCH_SIZE
  total = TOTAL

  for start in range(1, total, batch_size):
    end = min(start + batch_size, total)
    futures = [executor.submit(send_message, i) for i in range(start, end)]

    # 等待当前批次完成
    for future in as_completed(futures):
      try:
        future.result()
      except Exception as e:
        print("[Error] Task failed: {}".format(e))

producer.flush()
producer.close()
print("[Producer] All messages sent and producer closed.")
