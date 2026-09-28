# 未定义行为与序列点 评审清单

- 是否在同一表达式内重复修改同一标量
- 有符号运算是否可能溢出（改无符号或加检查）
- 跨类型指针强转是否经 memcpy 或 union 落地
- 是否存在未初始化读（-Wmaybe-uninitialized）

## 相关

- [细则](../knowledge/undefined-behavior.md) · [知识树](../../references/知识树/知识树.md)
