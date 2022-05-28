#!/bin/sh -ex

MAX_INSTALL_PATH="/Users/${USER}/Documents/Max 8/Library/ableton-ws/"
LIVE_INSTALL_PATH="/Users/${USER}/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/Imported/"

install -d "${LIVE_INSTALL_PATH}"
install -m 766 ./m4l/ableton-ws.amxd "${LIVE_INSTALL_PATH}"

install -d "${MAX_INSTALL_PATH}"
install -m 744 ./node/main.js ./node/package-lock.json ./node/package.json "${MAX_INSTALL_PATH}"

cd "${MAX_INSTALL_PATH}"

npm install
