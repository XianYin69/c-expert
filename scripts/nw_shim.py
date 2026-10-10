"""nw_shim.py — 技能侧静默子进程垫片（批41 F4·缺口 G3）：SMS 本体有 no_window.py 统一封装，
但技能目录是各自独立的仓、不共享 sys.path，被派发执行时裸 subprocess 仍弹命令行窗口
（实测 2026-10-10 技能面 106 处命中）。本垫片优先复用本体封装（按 env SMS_ROOT／SMS_SKILL
→ %LOCALAPPDATA%\\SMS\\skills\\smsystem-suit 定位本体 skill/scripts），本体不可达时自备
同口径合并：CREATE_NO_WINDOW＋STARTUPINFO(SW_HIDE)，调用点已有 creationflags 只 OR 不丢。
用法：import nw_shim as nw → nw.run(...)／nw.Popen(...)（sms_detach=True 保 DETACHED 语义）；
确需可见控制台处保留裸调用并在其上两行内加 `# sms-visible` 标记（审计白名单口径不变）。
"""
import os
import subprocess

CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
BODY = r"C:\Users\User\AppData\Local\SMS\skills\smsystem-suit"


def _body_scripts():
    """本体 skill/scripts 目录（存在 no_window.py 者）；找不到回 ""。"""
    import sys
    for v in (os.environ.get("SMS_ROOT"), os.environ.get("SMS_SKILL"), BODY):
        p = os.path.join(v or "", "skill", "scripts")
        if os.path.isfile(os.path.join(p, "no_window.py")):
            if p not in sys.path:
                sys.path.insert(0, p)
            return p
    return ""


try:
    if _body_scripts():
        import no_window as _NW
    else:
        _NW = None
except Exception:
    _NW = None


def _si():
    si = subprocess.STARTUPINFO()
    try:
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0
    except Exception:
        pass
    return si


def _kw(kw, detach=False):
    """本地兜底：合并已有 creationflags（绝不丢失）＋隐藏窗口。"""
    if os.name != "nt":
        kw.pop("sms_detach", None)
        return kw
    f = int(kw.get("creationflags") or 0)
    f |= (DETACHED_PROCESS | CREATE_NO_WINDOW) if detach else CREATE_NO_WINDOW
    kw["creationflags"] = f
    kw.setdefault("startupinfo", _si())
    kw.pop("sms_detach", None)
    return kw


def _go(nm, a, kw):
    if _NW is not None:
        return getattr(_NW, nm)(*a, **kw)      # 本体封装在＝原样交它（口径逐字一致）
    return getattr(subprocess, nm)(*a, **_kw(kw, bool(kw.get("sms_detach"))))


def run(*a, **kw):
    return _go("run", a, kw)


def Popen(*a, **kw):
    return _go("Popen", a, kw)


def selftest():
    import sys
    code = "import ctypes;print('CONSOLE=%s' % (ctypes.windll.kernel32.GetConsoleWindow()))"
    p = run([sys.executable, "-B", "-c", code], capture_output=True, text=True)
    out = (p.stdout or p.stderr or "").strip()
    return {"rc": p.returncode, "body_wrapper": _NW is not None, "silent": "CONSOLE=0" in out}


if __name__ == "__main__":
    import json
    print(json.dumps(selftest(), ensure_ascii=False))
