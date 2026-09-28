# 动态分配与所有权（memory-ownership）

- 每个分配须有唯一所有者与释放点，接口注明移交/借用
- realloc 失败不得覆盖原指针，先入临时变量
- 所有权移交后原持有者禁止再 free
- 分配失败即走错误路径，禁止解引用 NULL

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/memory-ownership.md)
