# 声明作用域与链接（declaration-linkage）

- 内部链接用 static，跨 TU 声明入头文件，定义唯一
- typedef 不引入新类型，不改变兼容规则
- 同一对象的多处 extern 声明类型须一致否则 UB
- 文件级非 static 全局符号即 ABI 暴露面

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/declaration-linkage.md)
