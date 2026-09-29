#!/bin/zsh
# Offline demonstration. Turn Wi-Fi OFF first, then run this (or double-click "Run offline demo.command").
# Every ./wiki call below is a fresh process, so the CLI is restarted after the network is gone.
# Everything printed is also saved to evidence/offline/offline-session.txt.
cd "$(dirname "$0")/.." || exit 1
export PYTHONUNBUFFERED=1
OUT=evidence/offline
mkdir -p "$OUT"

WIFI=$(networksetup -getairportpower en0 2>/dev/null)
ROUTE=$(route -n get default 2>&1 | grep -c "gateway:")
if [[ "$WIFI" == *"On"* || "$ROUTE" != "0" ]] && [[ "$1" != "--rehearsal" ]]; then
  echo "This Mac is still connected."
  echo "  $WIFI"
  echo "  default network route present: $ROUTE"
  echo "Turn Wi-Fi off (and unplug any cable or phone tether), then run this again."
  echo "To practise while online:  scripts/offline_demo.sh --rehearsal   (saved separately, never as offline evidence)"
  exit 1
fi
[[ "$1" == "--rehearsal" ]] && OUT=evidence/online && mkdir -p "$OUT"

{
  echo "DEMONSTRATION   $(date '+%Y-%m-%d %H:%M:%S %Z')"
  [[ "$1" == "--rehearsal" ]] && echo "*** RUN WHILE ONLINE (rehearsal of the same script): this is NOT offline evidence ***"
  echo
  echo "##### 0. Network state, from the operating system"
  networksetup -getairportpower en0
  echo "default route: $(route -n get default 2>&1 | grep -E 'gateway|not in table' | head -1)"
  echo "ping 1.1.1.1:  $(ping -c 1 -t 2 1.1.1.1 2>&1 | tail -1)"
  echo "github.com:    $(nc -z -G 2 github.com 443 2>&1 && echo reachable || echo unreachable)"
  echo
  echo "##### 1. ./wiki help"
  ./wiki help
  echo
  echo "##### 2. ./wiki status   (model, runtime, device, network)"
  ./wiki status
  echo
  echo "##### 3. ./wiki ingest \"vault/raw/Pac-Man DQN README.md\" --force   (local Gemma drafts the notes again)"
  ./wiki ingest "vault/raw/Pac-Man DQN README.md" --force
  echo
  echo "##### 4. ./wiki search \"row level security\"   (no model)"
  ./wiki search "row level security"
  echo
  echo "##### 5. ./wiki test   (four ask-mode questions, then the chat, search and separation checks)"
  ./wiki test --out "$OUT"
  echo
  echo "FINISHED   $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo "network at the end: $(networksetup -getairportpower en0)"
} 2>&1 | tee "$OUT/session.txt"
echo
echo "Saved to $OUT/. You can turn Wi-Fi back on now."
