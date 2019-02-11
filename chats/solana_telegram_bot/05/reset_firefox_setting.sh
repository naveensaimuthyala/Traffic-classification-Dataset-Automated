#!/bin/bash
#FIXME  change  ~/.mozilla/firefox/wq9qht23.default-1542483635651/prefs.js
PERF_FILE=~/.mozilla/firefox/i540b272.default/prefs.js
rm -rf ~/.mozilla/firefox/Crash\ Reports/*
cp crashreporter.ini ~/.mozilla/firefox/Crash\ Reports/
sed -i '/user_pref("toolkit.startup.recent_crashes"/d' $PERF_FILE 
sed -i 's/user_pref("browser.laterrun.bookkeeping.sessionCount", 4);/user_pref("browser.laterrun.bookkeeping.sessionCount", 1);/g' $PERF_FILE
