"""Saved outputs: evidence cards a reader can inspect without rerunning the model."""
import json
import platform
import shutil
import subprocess
import time

from . import config, model


def _run(*cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=15).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def device():
    """Device specs read from the operating system."""
    page = 4096
    free_pages = 0
    for line in _run("vm_stat").splitlines():
        if line.startswith(("Pages free", "Pages inactive", "Pages speculative")):
            free_pages += int(line.split(":")[1].strip().rstrip("."))
    gpus = [l.split(":", 1)[1].strip() for l in _run("system_profiler", "SPDisplaysDataType").splitlines()
            if "Chipset Model" in l or "VRAM" in l]
    mem = _run("sysctl", "-n", "hw.memsize")
    return {"os": f"macOS {_run('sw_vers', '-productVersion')}", "machine": platform.machine(),
            "cpu": _run("sysctl", "-n", "machdep.cpu.brand_string"),
            "cpu_cores": _run("sysctl", "-n", "hw.physicalcpu"),
            "ram_gb": round(int(mem) / 2**30) if mem.isdigit() else None,
            "available_memory_gb": round(free_pages * page / 2**30, 1),
            "gpu": gpus, "free_disk_gb": round(shutil.disk_usage(str(config.ROOT)).free / 2**30, 1),
            "python": platform.python_version()}


def stamp():
    """Fields every evidence file carries: when, which model, and whether the internet was reachable."""
    try:
        ident = model.identity()
    except model.ModelUnavailable as exc:
        ident = {"model": config.MODEL, "error": str(exc).splitlines()[0]}
    network = model.network_state()
    return {"recorded_at": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "execution": "local", "network": network,
            "internet_reachable": not network["offline"], "model": ident, "memory": model.memory()}


def save(directory, name, record, markdown):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{name}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (directory / f"{name}.md").write_text(markdown, encoding="utf-8")
    return directory / f"{name}.md"
