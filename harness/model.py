"""The only file that talks to the model. Local Gemma through the Ollama HTTP API on 127.0.0.1."""
import json
import socket
import time
import urllib.error
import urllib.request

from . import config


class ModelUnavailable(RuntimeError):
    """The local runtime or the model could not be reached."""


def _request(path, body=None, timeout=900):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(config.OLLAMA_URL + path, data=data, headers={"Content-Type": "application/json"})
    try:
        return urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:200]
        if exc.code == 404:
            raise ModelUnavailable(
                f"The local runtime is running but model '{config.MODEL}' is not downloaded.\n"
                f"  While online, run:  ollama pull {config.MODEL}") from exc
        raise ModelUnavailable(f"The local runtime returned an error ({exc.code}): {detail}") from exc
    except (urllib.error.URLError, ConnectionError, socket.timeout) as exc:
        raise ModelUnavailable(
            f"Cannot reach the local model runtime at {config.OLLAMA_URL}.\n"
            "  Start it with:  ollama serve   (or open the Ollama app)\n"
            "  search still works without the model.") from exc


def chat(messages, *, max_tokens=300, temperature=0.2, purpose="", stream_to=None):
    """Send messages to local Gemma. Returns (text, stats). Thinking is switched off: this model
    otherwise spends its output budget on hidden reasoning and can return an empty reply."""
    body = {"model": config.MODEL, "messages": messages, "think": False, "stream": stream_to is not None,
            "keep_alive": config.KEEP_ALIVE,
            "options": {"temperature": temperature, "num_predict": max_tokens, "num_ctx": config.NUM_CTX}}
    started = time.time()
    with _request("/api/chat", body) as resp:
        if stream_to is None:
            final = json.load(resp)
            text = final["message"]["content"]
        else:
            parts, final = [], {}
            for line in resp:
                if not line.strip():
                    continue
                piece = json.loads(line)
                delta = piece.get("message", {}).get("content", "")
                if delta:
                    parts.append(delta)
                    stream_to.write(delta)
                    stream_to.flush()
                if piece.get("done"):
                    final = piece
            text = "".join(parts)
    stats = {
        "purpose": purpose,
        "wall_seconds": round(time.time() - started, 2),
        "load_seconds": round(final.get("load_duration", 0) / 1e9, 2),
        "prompt_tokens": final.get("prompt_eval_count", 0),
        "output_tokens": final.get("eval_count", 0),
        "prompt_tokens_per_s": round(final.get("prompt_eval_count", 0) / max(final.get("prompt_eval_duration", 0) / 1e9, 1e-9), 1),
        "output_tokens_per_s": round(final.get("eval_count", 0) / max(final.get("eval_duration", 0) / 1e9, 1e-9), 1),
    }
    _log({"at": time.strftime("%Y-%m-%dT%H:%M:%S"), **stats, "messages": messages, "reply": text})
    return text.strip(), stats


def _log(record):
    config.LOGS.mkdir(parents=True, exist_ok=True)
    with open(config.LOGS / "model_calls.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def identity():
    """Exact model and runtime identity, read from the runtime rather than typed by hand."""
    info = {"model": config.MODEL, "execution": "local", "runtime": "Ollama", "endpoint": config.OLLAMA_URL}
    with _request("/api/version", timeout=10) as resp:
        info["runtime_version"] = json.load(resp).get("version")
    with _request("/api/show", {"model": config.MODEL}, timeout=30) as resp:
        details = json.load(resp).get("details", {})
    info.update(quantization=details.get("quantization_level"), parameter_size=details.get("parameter_size"),
                family=details.get("family"), file_format=details.get("format"))
    with _request("/api/tags", timeout=10) as resp:
        for entry in json.load(resp).get("models", []):
            if entry.get("name") == config.MODEL:
                info["digest"] = entry.get("digest", "")[:12]
                info["size_on_disk_gb"] = round(entry.get("size", 0) / 1e9, 2)
    info["context_tokens_used"] = config.NUM_CTX
    return info


def memory():
    """Memory the loaded model occupies right now, as the runtime reports it."""
    try:
        with _request("/api/ps", timeout=10) as resp:
            for entry in json.load(resp).get("models", []):
                if entry.get("name") == config.MODEL:
                    size, vram = entry.get("size", 0), entry.get("size_vram", 0)
                    return {"loaded_gb": round(size / 1e9, 2), "in_gpu_gb": round(vram / 1e9, 2),
                            "processor": "100% CPU" if not vram else f"{round(100 * vram / max(size, 1))}% GPU"}
    except ModelUnavailable:
        pass
    return {"loaded_gb": None, "in_gpu_gb": None, "processor": "not loaded"}


def network_state(timeout=1.5):
    """Is this machine connected? Read from the operating system, because a per-app firewall can block or allow a
    probe regardless of the real connection. 'offline' needs all three signals to agree."""
    import subprocess

    def run(*cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout
        except (OSError, subprocess.SubprocessError):
            return ""

    wifi = "On" if "On" in run("networksetup", "-getairportpower", "en0") else "Off"
    route = "gateway:" in run("route", "-n", "get", "default")
    probe = False
    for host, port in (("1.1.1.1", 443), ("8.8.8.8", 53), ("9.9.9.9", 443)):
        try:
            socket.create_connection((host, port), timeout=timeout).close()
            probe = True
            break
        except OSError:
            continue
    return {"wifi_power": wifi, "default_route": route, "outside_host_answered": probe,
            "offline": not route and not probe}


def internet_reachable():
    state = network_state()
    return not state["offline"]


def banner():
    try:
        ident = identity()
        model_line = f"{ident['model']} ({ident.get('quantization')}) on {ident['runtime']} {ident.get('runtime_version')}"
    except ModelUnavailable:
        model_line = f"{config.MODEL} (runtime not reachable)"
    state = network_state()
    net = "OFFLINE (Wi-Fi off, no network route)" if state["offline"] else f"connected (Wi-Fi {state['wifi_power']})"
    return f"model: {model_line} · execution: local · network: {net}"
