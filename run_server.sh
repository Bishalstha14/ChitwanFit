#!/bin/bash
# Detached launcher for ChitwanFit. Spawns the server in its own session
# with all file descriptors detached, then exits immediately so the tool
# that called this script can return right away.
cd /home/codio/workspace/build-lab || exit 1
setsid python3 app.py > /tmp/chitwanfit.log 2>&1 < /dev/null &
disown
