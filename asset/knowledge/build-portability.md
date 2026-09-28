# 构建与可移植性（build-portability）

- 显式 -std= 锁方言，否则随编译器默认漂移
- 配方行须制表符；伪目标须登记 .PHONY
- 平台专有 API 须隔离在适配层并条件编译
- 交叉编译须固定 sysroot 与 triple，勿依赖宿主头

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/build-portability.md)
