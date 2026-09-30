#!/bin/zsh
# OFFLINE DEMONSTRATION LAUNCHER
#   1. Turn Wi-Fi OFF (menu bar).      2. Double-click this file.
#   3. When it says so, take a screenshot of this window:  Cmd+Shift+4, then Space, then click the window.
#   4. Turn Wi-Fi back ON and press Return. It rebuilds the README and publishes the evidence.
cd "$(dirname "$0")" || exit 1
START=$(date +%s)
printf '\033]0;Ledger offline demonstration\007'
clear
scripts/offline_demo.sh || { echo; echo "Press Return to close."; read; exit 1; }

echo
echo "════════════════════════════════════════════════════════════════════════"
echo " OFFLINE RUN COMPLETE.  $(networksetup -getairportpower en0)"
echo " NOW: take a screenshot of this window (Cmd+Shift+4, Space, click it)."
echo " THEN: turn Wi-Fi back ON and press Return here."
echo "════════════════════════════════════════════════════════════════════════"
read

# pick up screenshots taken during the run (from the folder macOS saves them to; Desktop unless changed)
SHOTDIR=$(defaults read com.apple.screencapture location 2>/dev/null)
SHOTDIR=${SHOTDIR/#\~/$HOME}
[ -d "$SHOTDIR" ] || SHOTDIR=$HOME/Desktop
n=0
for shot in "$SHOTDIR"/Screenshot*.png(N) "$SHOTDIR"/Screen\ Shot*.png(N); do
  if [ "$(stat -f %m "$shot")" -ge "$START" ]; then
    n=$((n+1)); cp "$shot" "evidence/offline/offline-run-$n.png"; echo "added screenshot: evidence/offline/offline-run-$n.png"
  fi
done
[ "$n" -eq 0 ] && echo "No new screenshot found in $SHOTDIR. The text transcript is still saved."

echo "Waiting for the network to come back..."
for i in {1..60}; do
  route -n get default 2>/dev/null | grep -q "gateway:" && break
  sleep 2
done
python3 scripts/build_readme.py
git add -A
git commit -q -m "Offline demonstration: ingestion, four ask tests and mode checks with Wi-Fi off" && echo "committed"
echo
echo "Committed on this Mac, not published yet. The assessments are written against these offline answers first."
echo "Go back to Claude and say: done, push it"
echo; echo "Press Return to close."; read
