# I/O 与错误处理（io-error-handling）

- stdio 出错返回随函数各异：读用 EOF/ferror，写用短写计数
- errno 仅在出错时被置，成功调用后其值不定须先清
- 错误路径统一 goto fail 集中清理（Linux 内核风格）
- 返回值约定须在头文件写明（0 成功 or 指针）

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/io-error-handling.md)
