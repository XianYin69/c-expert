# 构建与可移植性 评审清单

- 是否声明 C_STANDARD/-std 与 C_EXTENSIONS
- 是否用 file(GLOB) 收集源码
- 全局 include_directories/link_libraries 是否污染目标
- sanitizer 与调试档是否可切换

## 相关

- [细则](../knowledge/build-portability.md) · [知识树](../../references/知识树/知识树.md)
