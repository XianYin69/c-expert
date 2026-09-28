"""concurrency_probe.py — C 并发取证：pthread/C11 原子的锁配对、条件变量谓词、共享标志原子性、内存序。"""
import re, sys, argparse

RX = [
    ("blocking", r"\bvolatile\s+\w+\s*\*?\s*\w+\s*;", "volatile 作跨线程同步（应 _Atomic / mutex）"),
    ("blocking", r"\bwhile\s*\(\s*!\s*\w+\s*\)\s*;\s*$", "忙等自旋无原子/无退避"),
    ("blocking", r"\bpthread_cond_wait\s*\([^)]*\)\s*;\s*\}", "cond_wait 未在谓词循环内（丢唤醒）"),
    ("blocking", r"\bsleep\s*\(\s*\d+\s*\)", "以 sleep 代同步（时序假设非保证）"),
    ("major", r"\bpthread_mutex_lock\s*\(", "加锁：须核对该路径上所有 return/break 是否解锁"),
    ("major", r"\bpthread_create\s*\([^,]+,[^,]+,\s*NULL\s*\)", "detach 状态未设：join 缺失即资源泄漏"),
    ("major", r"\batomic_(load|store)\s*\([^)]*\)", "默认 memory_order_seq_cst：放宽须写明理由"),
    ("major", r"\b(strtok|rand|localtime|gmtime|gethostbyname)\s*\(", "非线程安全函数"),
    ("minor", r"\bpthread_mutexattr_(settype|init)\b", "锁类型未设（默认非递归/非检错）"),
    ("minor", r"\bint\s+\w+\s*=\s*0\s*;\s*/\*.*thread", "共享计数器无原子/锁注释即疑数据竞争"),
]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src", nargs="+")
    ap.add_argument("--std", default="c11"); a = ap.parse_args()
    n = 0
    for f in a.src:
        txt = open(f, encoding="utf-8", errors="replace").read()
        for i, l in enumerate(txt.splitlines(), 1):
            if l.strip().startswith(("//", "*", "/*")):
                continue
            for sev, pat, why in RX:
                if re.search(pat, l):
                    print(f"{f}:{i} [{sev}] {why}\n    | {l.strip()[:72]}"); n += 1
        lk = len(re.findall(r"pthread_mutex_lock",
            txt)); ul = len(re.findall(r"pthread_mutex_unlock", txt))
        if lk != ul:
            print(f"{f} [blocking] lock={lk} unlock={ul} 不配对（早退路径漏解锁即死锁）"); n += 1
    print(f"[concurrency_probe] 命中={n}；结论须以 -fsanitize=thread 实测复现后方可断言")
    return 0

if __name__ == "__main__":
    sys.exit(main())
