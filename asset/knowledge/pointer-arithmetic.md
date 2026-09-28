# 指针与数组（pointer-arithmetic）

- 数组在表达式中衰减为指针，sizeof 与取地址例外
- one-past 指针可参与运算但不可解引用
- 指针相减限同数组，结果类型 ptrdiff_t
- void* 在 C 中可隐式双向转换（C++ 需显式）

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/pointer-arithmetic.md)
