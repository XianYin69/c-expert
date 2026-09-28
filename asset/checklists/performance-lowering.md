# 性能与底层 评审清单

- 热循环是否可向量化（无函数调用/无别名写）
- 是否 strlen/分配在循环内
- 数据布局是否 SoA/AoS 有据
- 是否用 perf/cachegrind 实测

## 相关

- [细则](../knowledge/performance-lowering.md) · [知识树](../../references/知识树/知识树.md)
