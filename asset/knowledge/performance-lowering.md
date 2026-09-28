# 性能与底层（performance-lowering）

- 别名限制（restrict）是向量化前提，未标即保守生成
- 缓存局部性优先于微优化：先测后改
- 内联与优化等级由编译器决定，手工 inline 建议非保证
- 任何「更快」结论须附计数器数据

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/performance-lowering.md)
