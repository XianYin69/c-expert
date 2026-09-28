# 并发与原子 评审清单

- 锁的加/解锁是否路径配对（含早退）
- 是否以 sleep 代同步
- 原子操作内存序是否有依据
- pthread_create 返回值与 join/detach 是否处理

## 相关

- [细则](../knowledge/concurrency-atomics.md) · [知识树](../../references/知识树/知识树.md)
