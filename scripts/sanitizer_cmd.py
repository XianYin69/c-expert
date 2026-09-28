"""sanitizer_cmd.py — 生成可执行的 C sanitizer 编译+运行命令（ASan/UBSan/TSan/LSan/MSan）。"""
import argparse

G = {
    "gcc": {"asan": "-fsanitize=address -fno-omit-frame-pointer -g",
            "ubsan": "-fsanitize=undefined -fno-sanitize-recover=all -g",
            "tsan": "-fsanitize=thread -pie -fPIE -g",
            "lsan": "-fsanitize=leak -g",
            "msan": "-fsanitize=memory -fno-omit-frame-pointer -g"},
    "clang": {"asan": "-fsanitize=address -fno-omit-frame-pointer -g",
              "ubsan": "-fsanitize=undefined -fno-sanitize-recover=all -g",
              "tsan": "-fsanitize=thread -fPIE -g",
              "lsan": "-fsanitize=leak -g",
              "msan": "-fsanitize=memory -fsanitize-memory-track-origins -g"},
    "msvc": {"asan": "/fsanitize=address /Zi /Od",
        "ubsan": "/fsanitize=address /Zi  (MSVC 无 UBSan：用 clang-cl)",
             "tsan": "MSVC 无 TSan：改 clang-cl -fsanitize=thread",
                 "lsan": "/fsanitize=address /Zi (ASan 覆盖泄漏)",
             "msan": "MSVC 无 MSan：改 clang-cl -fsanitize=memory"},
}
ENV = {"asan": "ASAN_OPTIONS=detect_leaks=1:abort_on_error=1",
       "ubsan": "UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1",
       "tsan": "TSAN_OPTIONS=halt_on_error=1:second_deadlock_stack=1",
       "lsan": "LSAN_OPTIONS=verbosity=1", "msan": "MSAN_OPTIONS=print_stacktrace=1"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="asan", choices=sorted(G["gcc"]))
    ap.add_argument("--compiler", default="gcc", choices=["gcc", "clang", "cl"])
    ap.add_argument("--src", default="main.c"); ap.add_argument("--std", default="11")
    ap.add_argument("--run", action="store_true"); ap.add_argument("--extra", default="")
    a = ap.parse_args()
    key = {"gcc": "gcc", "clang": "clang", "cl": "msvc"}[a.compiler]
    flags = G[key][a.kind]
    if a.compiler == "cl":
        print(f"cl /std:c{a.std} {flags} {a.extra} {a.src} /Fe:app.exe")
        print(f"REM {ENV.get(a.kind, '')}")
        if a.run: print("app.exe")
    else:
        print(f"{a.compiler} -std=c{a.std} -O1 -g {flags} {a.extra} {a.src} -o app -lpthread")
        print(f"# env: {ENV.get(a.kind, '')}")
        if a.run: print(f"{ENV.get(a.kind, '')} ./app")
    print("# note: ASan/TSan/MSan 互斥，须分别建目标；MSan 需全程序插桩否则假阴性")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
