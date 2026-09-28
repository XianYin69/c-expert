# dependence（依赖声明）
本技能**不内嵌**其他技能正文；能力一律经声明获取。每行一条 `名称 | 类型 | 来源`，
类型为 skill|software|repo。SMS 安装时对本目录条目与本体做同样检查与净化
（trust 标注·未审/隔离拒装·仓库下载须网络授权）。
```
file_ops             | skill    | local:skill_manage_system
code-guidelines      | skill    | local
pavedpath-code       | skill    | local
ui-design            | skill    | local
database-management  | skill    | local
concurrency-design   | skill    | local
python               | software | system
git                  | software | system
```
## 用途映射
| 依赖 | 承担能力 | 触发节点 |
|---|---|---|
| file_ops | 联网检索/取页（ff_lite.py search/fetch）、文件读写 | 浏览器学习 · 知识库构建 · 经验查询 |
| code-guidelines | 命名/注释/复杂度/评审通用准则 | 脚本构建 · 整体审查 |
| pavedpath-code | 已验证实现范式与脚手架 | 脚本构建 · 重构建议（输出交付） |
| ui-design | 界面/交互专项判断（本技能不自行装 UI） | 分支分析（转派） |
| database-management | 存储/查询/迁移专项（转派，不内嵌） | 分支分析（转派） |
| concurrency-design | 并发架构设计专项；本技能只出 C 语言级取证 | 分支分析（转派） · concurrency-atomics |
| python | 运行 `scripts/` 探针与机制脚本 | 构建测试 · 整体审查 · 收尾 |
| git | 功能分支→dev→main 工作流 | 初始化 · 收尾 |
## 派发约定
- 跨技能只传「意图 + 参数」，由对方在其目录内执行；禁止直接 import 他技能模块。
- 例：`file_ops: search "C11 7.22.2 malloc 返回值" → fetch <url>`，本技能不复制其实现。
## 边界
- 依赖缺失：记 `process_chain.py interrupt` 并报告缺项，禁止伪造能力继续。
- 增删依赖须走 [update 审批流](../update/update.md) 并记 CHANGELOG。
- 自检：`python -B scripts/deps_check.py`（逐项验证本地可达）。
## 相关
- [resistance](../resistance/resistance.md) · [薄技能依赖约束](../resistance/薄技能依赖约束/薄技能依赖约束.md)
