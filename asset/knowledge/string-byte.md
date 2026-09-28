# 字符串与字节操作（string-byte）

- 字符串以 NUL 终止，缓冲区容量须为长度 +1
- snprintf 返回欲写长度，≥容量即截断须处理
- memcpy 区域重叠为 UB，重叠须 memmove
- 字符分类函数入参须可转 unsigned char 或 EOF

## 相关

- [知识树](../../references/知识树/知识树.md) · [评审清单](../checklists/string-byte.md)
