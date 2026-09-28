# references（知识库索引）
本目录只存**摘要与出处**，不存受版权保护的正文。来源标注两类：
- `[联网]`＝经 file_ops 的 ff_lite 检索/取页确证（取证时间 2026-09-29，豆瓣读书 subject 页与 google.github.io）。
- `[本地]`＝模型既有常识，**未经联网确证**，禁止当作已验证事实引用，禁止附 URL。

## C 语言权威书目（与知识叶映射）
| 领域 | 条目 | 来源 |
|---|---|---|
| 语言基础 | [C程序设计语言 K&R 第2版](语言基础/c-programming-language-kr2.md) · [C Primer Plus 第6版](语言基础/c-primer-plus-6e.md) · [C语言参考手册](语言基础/c-reference-manual-harbison.md) · [C语言本质 / Modern C](语言基础/c-essence-modern-c.md) | [联网] |
| 工程实践 | [C和指针](工程实践/c-and-pointers-reek.md) · [C陷阱与缺陷](工程实践/c-traps-and-pitfalls.md) · [Google 风格指南](工程实践/google-style-guide.md) | [联网] |
| 算法 | [编程珠玑 第2版修订版](算法/programming-pearls-2e.md) | [联网] |
| 底层模型 | [深入理解计算机系统 CSAPP 第3版](底层模型/csapp-3e.md) · [编码：隐匿在计算机软硬件背后的语言](底层模型/code-petzold.md) | [联网] |
| 系统编程 | [UNIX环境高级编程 APUE 第3版](系统编程/apue-3e.md) | [联网] |

## 知识树（十二叶）
- [知识树索引](知识树/知识树.md)：叶 → `asset/knowledge/`（细则）与 `asset/checklists/`（评审清单）

## 确证计数（本次构建）
- [联网] 确证条目：**11**（豆瓣 subject 页 10 + google.github.io 1）
- [本地] 未确证条目：**0**（候选清单全部确证；`cguide.html` 实测 404，故不引用该 URL）

## 专项能力索引（外置薄技能·只引用不内嵌）
并发架构 → concurrency-design；编码规范 → code-guidelines；已验证范式 → pavedpath-code；
UI → ui-design；数据库 → database-management；文件与联网取证 → file_ops。
声明见 [dependence/](../dependence/dependence.md)。

## 取证方法（本环境可达性）
`python -B scripts/browser_learn.py --query "<书名>" --out tmp/learn`
境外源（en.cppreference.com / wikipedia / archive.org）在本环境 WinError 10060 不可达；
优先 book.douban.com（含 `j/subject_suggest?q=` 接口）、google.github.io、知乎、github.io 中文镜像。
≥4 词英文书名会被搜索引擎切成词典页 → 改用中文书名、`单词+出版社`，或直接查豆瓣 suggest 接口。

## 相关
- [resistance](../resistance/resistance.md) · [知识库构建](../branch/流程/知识库构建/知识库构建.md)
- [浏览器学习约束](../resistance/浏览器学习约束/浏览器学习约束.md)
