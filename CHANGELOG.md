# CHANGELOG
本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与语义化版本。

## 0.1.0 - 2026-09-29
### Added
- **流程复刻**：`branch/流程/` 按 general-programming 复刻为创建路径 13 节点
  （初始化→需求确认→经验查询→大纲构建→分支分析→脚本构建→构建测试→知识库构建→
  浏览器学习→约束编写→整体审查→收尾→完成）＋修改路径 3 节点（初始化→修改流程→完成）。
- **知识库**：`references/` 十二叶知识树索引 + 11 条 C 权威书目，全部经 file_ops
  `ff_lite.py` 联网确证（豆瓣读书 subject 页与 suggest 接口、google.github.io，取证 2026-09-29）；
  `[本地]` 未确证条目 0 条。实测 `google.github.io/styleguide/cguide.html` 返回 404，
  故只引用现行可达的 `cppguide.html` 并在条目内注明。
- **脚本**：`scripts/` 12 个 C 专用探针 + 19 个机制脚本，全部 py_compile 通过并实跑 rc=0；
  无 C 编译器环境下 `gcc_check.py` 按红线降级为 SKIP+ADVISORY，不谎称已编译验证。
- **约束**：`resistance/` 齐备——浏览器学习约束（遇不明强制派 file_ops 检索学习后再答）、
  薄技能依赖约束、git 工作流约束、审查约束、约束部分、沙盒机制、
  垃圾回收/上下文压缩/逻辑链/过程链存取/惩罚五大机制。
- **依赖声明**：`dependence/dependence.md` 薄技能只引用不内嵌
  （file_ops|skill|local:skill_manage_system、code-guidelines、pavedpath-code、ui-design、
  database-management、concurrency-design、python|software|system、git|software|system）＋用途映射表。
- **资产**：`asset/knowledge/`（12 叶细则）、`asset/checklists/`（12 叶评审清单）、
  `asset/knowledge_tree.json` 机读索引。
- **许可**：MIT `LICENSE`（技能目录、tmp 各一份）＋ `.gitignore`（tmp/ 与 IDE 目录）。

### Notes
- 本次构建未执行 `git push`、未创建远端仓库（由调度方统一推送）。
- 已知限制：本环境 PATH 无 gcc/clang，编译类结论一律标注为未实测。
