"""gcc_check.py — C 语法/编译检查：发现 gcc/clang/cc，跑 -fsyntax-only；无编译器则降级。"""
import os, shutil, subprocess, sys, argparse
CAND = ["gcc", "clang", "cc", "tcc"]
EXTRA = [r"C:\msys64\mingw64\bin", r"C:\mingw64\bin", r"C:\Program Files\LLVM\bin",
         r"C:\TDM-GCC-64\bin", r"C:\Strawberry\c\bin"]
def find(prefer=""):
    for c in ([prefer] if prefer else []) + CAND:
        if shutil.which(c):
            return shutil.which(c)
    for d in EXTRA:
        for c in CAND:
            f = os.path.join(d, c + ".exe")
            if os.path.isfile(f):
                return f
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="*"); ap.add_argument("--std", default="c11")
    ap.add_argument("--cc", default=""); ap.add_argument("--pedantic", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--probe", action="store_true")
    a = ap.parse_args(); cc = find(a.cc)
    if a.probe:
        print("[probe] compiler =", cc or "未检出（gcc/clang/cc 不在 PATH）")
        return 0 if cc else 3
    if not a.src:
        print("usage: gcc_check.py <file.c ...> [--std c11]", file=sys.stderr)
        return 2
    fl = ["-std=" + a.std, "-Wall", "-Wextra", "-Werror=implicit-function-declaration"]
    fl += (["-pedantic"] if a.pedantic else []) + ["-fsyntax-only"]
    if not cc:
        print("[SKIP] 未检出 C 编译器；禁止在无实测下断言「编译通过」。")
        print("[ADVISORY] 取证命令: gcc " + " ".join(fl + a.src))
        print("[LOCAL] 降级取证：ub_scan / memory_audit / header_deps 取文本证据。")
        return 0
    if a.dry_run:
        print("[DRY-RUN] " + cc + " " + " ".join(fl + a.src)); return 0
    rc = 0
    for f in a.src:
        r = subprocess.run([cc] + fl + [f], capture_output=True, text=True)
        print("--- %s :: rc=%s" % (f, r.returncode))
        print((r.stdout + r.stderr).strip() or "(no diagnostics)")
        rc = rc or r.returncode
    print("[OK] compiler=%s 结论=%s" % (cc, "通过" if rc == 0 else "有诊断须复跑"))
    return rc

if __name__ == "__main__":
    sys.exit(main())
