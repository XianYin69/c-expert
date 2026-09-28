# 头文件与模块组织（header-modular）

- 每个头自包含且带 guard，guard 名与路径唯一
- 只包含直接依赖（IWYU），不得指望间接包含
- 指针/引用型依赖用前置声明降耦合
- 导出结构体布局即 ABI，改动须版本化

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/header-modular.md)
