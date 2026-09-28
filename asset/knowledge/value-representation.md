# 类型与值表示（value-representation）

- 整数值域实现定义：查 limits.h，勿假设 32 位
- 整数提升：小于 int 者先提升，结果符号随提升后类型
- sizeof 为编译期常量；sizeof(void) 非法
- 对齐与填充决定布局，也是原子无锁的前提

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/value-representation.md)
