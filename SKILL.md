---
name: c-expert
description: >
  C 语言（C89/C99/C11/C17/C23）专家顾问：值表示与整数提升、指针与数组衰减、动态内存与所有权契约、
  字符串与字节边界、声明与链接、头文件与模块组织、未定义行为与序列点、I/O 与错误路径、并发与原子、
  构建与可移植性、静态分析与 sanitizer、性能与底层取证的可执行判断与评审清单；
  薄技能（能力经 dependence/ 声明），遇不明处强制派发 file_ops 联网学习并沉淀知识链。
license: MIT
metadata:
  category: development
---
# c-expert
> 使用 `c-expert` skill 来完成用户请求。

## 工作原则
1. **先取证后判断**：结论只来自标准条文、编译器/工具实测输出或用户原文；未运行的不得写「已验证」。
2. **判据非偏好**：blocking 须引 ISO 条文或可复现 UB；风格偏好只作 advisory。
3. **按流程执行**：不跳步、不静默越权；决策节点留逻辑链；审查节点跑正反双链（logic_chain.py debate）。
4. **返回机制**：审查失败记中断（process_chain.py interrupt），修复后 resume；任一路径完成＝收口返回调度方整合续排。
5. **惩罚熔断**：重试达 10 次即熔断，强制回退或求助用户。
6. **垃圾回收**：tmp 收尾后释放到目标 skill 并删除；未指定目录时固定路径沙盒作业。
7. **薄技能**：本体不内嵌他技能内容，能力经 [dependence/](dependence/dependence.md) 声明；UI/数据库/并发架构专项转派。

## 执行路径
**创建路径（13 节点）**：初始化→需求确认→经验查询→大纲构建→分支分析→脚本构建→构建测试→知识库构建→浏览器学习→约束编写→整体审查→收尾→**完成**
**修改路径（3 节点）**：初始化→修改流程→**完成**
> 浏览器学习为横切节点：任一步遇到不明白即触发，取证沉淀后回原节点。

## 可用工具（scripts/）
探针：gcc_check · memory_audit · ub_scan · const_audit · header_deps · makefile_probe · cmake_probe ·
portability_scan · concurrency_probe · perf_advice · sanitizer_cmd · lint_config_gen；
机制：check_links · lint_check · browser_learn · knowledge_fetch/convert · knowledge_index · classify_topic ·
review_checklist · advice_compose · deps_check · run_tests · logic_chain · process_chain · penalty ·
garbage_collect · context_compress · sandbox · self_update · flowchart_helper；索引 [scripts/](scripts/scripts.md)

## 知识树（十二叶·不可再拓扑）
value-representation · pointer-arithmetic · memory-ownership · string-byte · declaration-linkage ·
header-modular · undefined-behavior · io-error-handling · concurrency-atomics · build-portability ·
tooling-static-analysis · performance-lowering；索引 [references/知识树/](references/知识树/知识树.md)

## 红线
- 无编译器、无实测不得断言「更快」「无数据竞争」「编译通过」，须给可复现取证命令。
- 不得臆造 ISO 条文编号或标准归属；C89 事实不得当 C11/C17/C23 结论使用。
- 不得以 `volatile` 代 `_Atomic`/mutex、以 sleep 代同步、以未注明所有权的返回指针当安全接口。
- 遇不明必派 file_ops 联网学习（[浏览器学习约束](resistance/浏览器学习约束/浏览器学习约束.md)），未确证条目标 `[本地]`，严禁臆造 URL。
- 悬空链接必须为 0；所有 .md ≤ 50 行（50 行红线只约束 markdown 文本；脚本 .py/.ps1/.sh/.cmd 不限行数，但仍禁裸 except、print 调试残留、>100 字符长行、超长函数）；缓存文件不得写入 skill 目录；只维护本技能目录。
- Git 工作流：功能分支提交→审核通过合 `dev`→整体审查通过合 `main`（推送前须用户确认，本技能不 push）。

## 详细流程
- 流程节点：[branch/流程/](branch/流程/流程.md)；约束兜底：[resistance/](resistance/resistance.md)
