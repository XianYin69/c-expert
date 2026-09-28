# 动态分配与所有权 评审清单

- malloc/calloc/realloc/strdup 是否逐一配对 free
- 是否双重释放或释放非堆地址
- 早退路径是否释放全部已获资源
- 是否以 ASan/valgrind 实测泄漏

## 相关

- [细则](../knowledge/memory-ownership.md) · [知识树](../../references/知识树/知识树.md)
