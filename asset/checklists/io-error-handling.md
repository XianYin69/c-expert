# I/O 与错误处理 评审清单

- 每个可能失败的调用是否检查返回值
- errno 是否在使用前清零并立即读取
- 错误路径是否释放全部资源
- 是否把 EOF 与真错误区分

## 相关

- [细则](../knowledge/io-error-handling.md) · [知识树](../../references/知识树/知识树.md)
