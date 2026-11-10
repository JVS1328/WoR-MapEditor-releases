# WoR Map Editor

A map editor for **War of Rights**: move spawns, capture points and boundaries, set up Skirmish areas and their regiments, sculpt terrain, place objects, then build the map and install it into the game or push it to a server. Made by Red (Discord: jvsr).

## Download

1. Get `WoR-Map-Editor-vX.Y.Z.zip` from the [latest release](../../releases/latest).
2. Unzip it anywhere and run `WoR Map Editor.exe`. Nothing is installed.
3. The exe isn't code-signed, so the first time Windows may say "Windows protected your PC": click **More info → Run anyway**.

The editor updates itself: when a new version is out it offers it on start (**Update now**), then you reopen it. Your maps in `projects\` are never touched.

## What's in this repo

| File | What it's for |
|---|---|
| Releases | Each editor version as a zip: what new users download and what the editor's self-update installs. |
| `release.py`, `changelog.txt` | How a new version is published (below). |

## Releasing a new version (Red)

1. In `..\WoR-MapEditor` (the private source): set `VERSION` in `updater.py`, commit. Run `make_app.bat` if `launcher.cs` or the runtime changed.
2. Here: write the changes in `changelog.txt`, then

   ```
   python release.py 1.0.8 --dry-run
   python release.py 1.0.8
   ```

   It builds `WoR-Map-Editor-v1.0.8.zip`, commits the changelog, and creates the GitHub release.
