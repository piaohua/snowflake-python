#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import random

#EPOCH 时间偏移量，从2019年6月16日零点开始
EPOCH = time.mktime((2019, 6, 16, 0, 0, 0, 0, 0, 0))
#SEQUENCE_BITS 自增量占用比特
SEQUENCE_BITS = 12
#WORKERID_BITS 工作进程ID比特
WORKERID_BITS = 5
#DATACENTERID_BITS 数据中心ID比特
DATACENTERID_BITS = 5
#NODEID_BITS 节点ID比特
NODEID_BITS = DATACENTERID_BITS + WORKERID_BITS
#SEQUENCE_MASK 自增量掩码（最大值）
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
#DATACENTERID_LEFT_SHIFT_BITS 数据中心ID左移比特数（位数）
DATACENTERID_LEFT_SHIFT_BITS = WORKERID_BITS + SEQUENCE_BITS
#WORKERID_LEFT_SHIFT_BITS 工作进程ID左移比特数（位数）
WORKERID_LEFT_SHIFT_BITS = SEQUENCE_BITS
#NODEID_LEFT_SHIFT_BITS 节点ID左移比特数（位数）
NODEID_LEFT_SHIFT_BITS = DATACENTERID_BITS + WORKERID_BITS + SEQUENCE_BITS
#TIMESTAMP_LEFT_SHIFT_BITS 时间戳左移比特数（位数）
TIMESTAMP_LEFT_SHIFT_BITS = NODEID_LEFT_SHIFT_BITS
#WORKERID_MAX 工作进程ID最大值
WORKERID_MAX = -1 ^ (-1 << WORKERID_BITS)
#DATACENTERID_MAX 数据中心ID最大值
DATACENTERID_MAX = -1 ^ (-1 << DATACENTERID_BITS)
#NODEID_MAX 节点ID最大值
NODEID_MAX = -1 ^ (-1 << NODEID_BITS)

def parse(id):
    r = {}
    r['timestamp'] = id >> TIMESTAMP_LEFT_SHIFT_BITS
    r['time'] = EPOCH + (id >> TIMESTAMP_LEFT_SHIFT_BITS) / 1000.0
    r['node'] = (id >> WORKERID_LEFT_SHIFT_BITS) & (-1 ^ (-1 << NODEID_BITS))
    r['sequence'] = id & SEQUENCE_MASK
    return r

def generate(workerID, datacenterID, sleep=lambda x: time.sleep(x/1000.0)):
    assert workerID >= 0 and workerID <= WORKERID_MAX
    assert datacenterID >= 0 and datacenterID <= DATACENTERID_MAX

    timestamp = 0
    sequence = 0

    while True:
        now = long((time.time() * 1000) - (EPOCH * 1000))

        if timestamp > now:
            sleep(timestamp - now)
            continue

        if now == timestamp:
            sequence = (sequence + 1) & SEQUENCE_MASK
            if sequence == 0:
                sleep(1)
                continue
        else:
            sequence = random.randint(0, 9)
        timestamp = now
        yield ((timestamp << TIMESTAMP_LEFT_SHIFT_BITS) |
            (datacenterID << DATACENTERID_LEFT_SHIFT_BITS) |
            (workerID << WORKERID_LEFT_SHIFT_BITS) |
            sequence)

if __name__ == "__main__":
    s = generate(1, 1)
    print(s.next())
    id = s.next()
    print(parse(id))
