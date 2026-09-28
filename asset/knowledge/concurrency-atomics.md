# 并发与原子（concurrency-atomics）

- 共享可变状态须锁或 _Atomic，volatile 不保证原子性与顺序
- 条件变量等待必在谓词循环内（防丢唤醒与虚假唤醒）
- 内存序放宽（relaxed）须写明理由，默认 seq_cst
- 信号处理函数只可调用 async-signal-safe 函数

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/concurrency-atomics.md)
