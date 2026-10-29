#!/usr/bin/env bash
# Applies MyWallet's native customisations to the generated Android project:
#   - launcher icon (from App.png via android-res/)
#   - FileSaver plugin ("choose where to save" for backups / exports)
#   - portrait orientation
# Run it right after `npx cap add android` (the GitHub workflow does this for you).
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d android ] || { echo "ERROR: android/ folder not found. Run 'npx cap add android' first."; exit 1; }

RES=android/app/src/main/res
JAVA=android/app/src/main/java/com/mywallet/app
MAN=android/app/src/main/AndroidManifest.xml

# 1) icons: remove the template's default launcher icons, then copy ours
rm -f "$RES"/mipmap-*/ic_launcher*.png "$RES"/mipmap-anydpi-v26/ic_launcher*.xml
cp -r android-res/. "$RES"/

# 2) native plugin + MainActivity that registers it
mkdir -p "$JAVA"
cp android-src/FileSaverPlugin.java android-src/MainActivity.java "$JAVA"/

# 3) portrait only (matches manifest.webmanifest)
if ! grep -q 'android:screenOrientation' "$MAN"; then
  sed -i -E 's/<activity([[:space:]]|$)/<activity android:screenOrientation="portrait"\1/' "$MAN"
fi

# 4) sanity checks: fail the build early instead of shipping a half-customised app
grep -q 'screenOrientation="portrait"' "$MAN"               || { echo "ERROR: portrait not applied"; exit 1; }
grep -q 'registerPlugin(FileSaverPlugin.class)' "$JAVA/MainActivity.java" || { echo "ERROR: plugin not registered"; exit 1; }
[ -f "$RES/mipmap-xxxhdpi/ic_launcher_foreground.png" ]     || { echo "ERROR: icons missing"; exit 1; }
[ -f "$RES/mipmap-anydpi-v26/ic_launcher.xml" ]             || { echo "ERROR: adaptive icon missing"; exit 1; }
echo "MyWallet Android customisations applied."
