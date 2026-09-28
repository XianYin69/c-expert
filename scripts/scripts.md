# scripts（脚本索引）
统一入口 `python -B scripts/<name>.py ...`；写盘类默认 `--dry-run`/预览，执行须显式 `--yes`。

## C 专用探针（12）
| 脚本 | 职责 | 用法 |
|---|---|---|
| gcc_check.py | 编译器发现 + `-fsyntax-only` 告警基线；无编译器降级 | `gcc_check.py a.c --std c11 [--probe]` |
| memory_audit.py | 分配/释放配对、NULL 检查、双重释放、所有权移交 | `memory_audit.py a.c b.c` |
| ub_scan.py | UB 目录：序列点、溢出、移位、别名、字面量写、负下标 | `ub_scan.py a.c --top 40` |
| const_audit.py | const/restrict 契约与指针位置语义 | `const_audit.py a.c --api` |
| header_deps.py | 包含图、guard、循环包含、未用头（IWYU） | `header_deps.py <root>` |
| makefile_probe.py | 制表符配方、.PHONY、-std/-Wall 基线 | `makefile_probe.py Makefile` |
| cmake_probe.py | C_STANDARD、GLOB、全局目录污染、sanitizer 档 | `cmake_probe.py CMakeLists.txt` |
| portability_scan.py | 方言特性越界、POSIX/MSVC 专有、字长假设 | `portability_scan.py a.c --std c11` |
| concurrency_probe.py | 锁配对、cond 谓词、volatile 代原子、sleep 代同步 | `concurrency_probe.py a.c` |
| perf_advice.py | strlen/分配/IO/别名/布局启发式（须实测） | `perf_advice.py a.c` |
| sanitizer_cmd.py | 生成 ASan/UBSan/TSan/LSan/MSan 可执行命令 | `sanitizer_cmd.py --kind ubsan --run` |
| lint_config_gen.py | .clang-tidy + cppcheck 参数 + 告警基线 | `lint_config_gen.py --out . --std c11` |

## 机制脚本（19）
check_links（悬空链接=0）· lint_check（≤50 行/坏味道）· browser_learn（派 file_ops 取证）·
knowledge_fetch / knowledge_convert（文献抓取与摘要）· knowledge_index / classify_topic（知识叶检索）·
review_checklist / advice_compose（清单与交付组装）· deps_check（依赖自检）· run_tests（构建测试）·
logic_chain（add/debate/verify）· process_chain（save/interrupt/resume）· penalty（熔断计数）·
garbage_collect（tmp 回收）· context_compress（上下文压缩）· sandbox（沙盒）· self_update（自更新）·
flowchart_helper（流程草稿对齐）

## 相关
- [SKILL.md](../SKILL.md) · [构建测试节点](../branch/流程/构建测试/构建测试.md)
