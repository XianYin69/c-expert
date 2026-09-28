# 工具与静态分析（tooling-static-analysis）

- 告警基线 -Wall -Wextra -Wpedantic 起步，逐步加严至 -Werror
- ASan/UBSan/TSan/MSan 互斥，须分目标构建
- 静态工具报的是候选非结论：blocking 须可复现
- MSan 需全程序插桩，否则假阴性

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/tooling-static-analysis.md)
