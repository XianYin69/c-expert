"""lint_config_gen.py — 生成 C 静态分析配置：.clang-tidy + cppcheck 参数 + 编译器告警基线。"""
import argparse, os, sys

TIDY = """---
Checks: >
  -*,clang-diagnostic-*,bugprone-*,cert-*,misc-*,portability-*,readability-*,
  -readability-magic-numbers,-readability-identifier-length
WarningsAsErrors: 'bugprone-*,cert-*,clang-diagnostic-*,portability-*'
HeaderFilterRegex: '.*'
CheckOptions:
  - key: cert-err33-c.AssignedOnlyReturnValueFunctions
    value: malloc;calloc;realloc;fopen;pthread_create
---
"""
CPPCHECK = ["--enable=all", "--std=c11", "--error-exitcode=1", "-j", "4",
            "--suppress=missingIncludeSystem", "--suppress=unusedFunction",
            "--inline-suppr", "-I", "include"]
GCC_FLAGS = ["-Wall", "-Wextra", "-Wpedantic", "-Wshadow", "-Wconversion", "-Wcast-qual",
             "-Wwrite-strings", "-Wstrict-prototypes", "-Wmissing-prototypes",
             "-Werror=implicit-function-declaration", "-Werror=return-type",
                 "-fsanitize=address,undefined"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="."); ap.add_argument("--std", default="c11")
    ap.add_argument("--dry-run", action="store_true"); a = ap.parse_args()
    tidy = TIDY.replace("c11", a.std)
    cpp = "cppcheck " + " ".join(x.replace("--std=c11",
        "--std=" + a.std) for x in CPPCHECK) + " SRC"
    if a.dry_run:
        print("[DRY-RUN] 将写 .clang-tidy / cppcheck.txt / flags.mk 到 " + a.out); return 0
    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, ".clang-tidy"), "w", encoding="utf-8", newline="\n").write(tidy)
    open(os.path.join(a.out, "cppcheck.txt"), "w", encoding="utf-8", newline="\n").write(cpp + "\n")
    open(os.path.join(a.out, "flags.mk"), "w", encoding="utf-8", newline="\n").write(
        "WARN_FLAGS = " + " ".join(GCC_FLAGS) + "\n")
    print(f"[OK] {a.out}: .clang-tidy + cppcheck.txt + flags.mk（{len(GCC_FLAGS)} 项告警基线）")
    print("note: clang-tidy 需 compile_commands.json（cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=ON）")
    return 0

if __name__ == "__main__":
    sys.exit(main())
