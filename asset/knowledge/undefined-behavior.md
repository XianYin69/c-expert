# 未定义行为与序列点（undefined-behavior）

- UB 使编译器可假设其不发生：优化后症状随机且难复现
- 同一标量在相邻序列点闲多次修改即 UB
- 有符号溢出是 UB，无符号回绕是定义行为
- 违反严格别名型的指针强转读值即 UB

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/undefined-behavior.md)
