"""Publishes a new WoR Map Editor version to this repo's GitHub releases (what the editor's self-update reads).

First, in ..\\WoR-MapEditor: set VERSION in updater.py, commit, and run make_app.bat if launcher.cs or the
runtime changed. Then write this version's changes in changelog.txt and, here:

    python release.py 1.0.8 --dry-run     builds the zip and checks everything, uploads nothing
    python release.py 1.0.8               publishes

The zip is one WoR-MapEditor/ folder: the editor's git-tracked files, WoR Map Editor.exe and runtime/.
"""
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "WoR-MapEditor"
REPO = "JVS1328/WoR-MapEditor-releases"


def run(*cmd, cwd=HERE):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main(version, dry):
    sys.path.insert(0, str(SRC))
    import updater
    problems = []
    if updater.VERSION != version:
        problems.append(f"updater.py says VERSION = {updater.VERSION}, not {version}. Set it and commit.")
    if run("git", "status", "--porcelain", cwd=SRC).stdout.strip():
        problems.append("WoR-MapEditor has uncommitted changes; they would ship. Commit or stash them.")
    exe, rt = SRC / "WoR Map Editor.exe", SRC / "runtime"
    if not exe.exists() or not (rt / "pythonw.exe").exists():
        problems.append("Missing WoR Map Editor.exe or runtime\\. Run make_app.bat in WoR-MapEditor.")
    notes = (HERE / "changelog.txt").read_text(encoding="utf-8") if (HERE / "changelog.txt").exists() else ""
    if not notes.strip() or "WRITE WHAT CHANGED" in notes:
        problems.append("Write this version's changes in changelog.txt first.")
    if run("gh", "release", "view", f"v{version}", "--repo", REPO).returncode == 0:
        problems.append(f"v{version} already exists on {REPO}. Pick a new version number.")
    for p in problems:
        print("WARNING:", p)
    if problems and not dry:
        raise SystemExit("Fix the warnings above first.")

    files = [SRC / f for f in run("git", "ls-files", cwd=SRC).stdout.splitlines()] + [exe] + sorted(p for p in rt.rglob("*") if p.is_file() and p.suffix != ".pyc")  # .pyc: this PC's bytecode cache
    zpath = HERE / f"WoR-Map-Editor-v{version}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("WoR-MapEditor/projects/", "")  # where the user's maps go
        for f in files:
            if f.is_file():
                z.write(f, "WoR-MapEditor/" + f.relative_to(SRC).as_posix())
    print(f"WoR Map Editor v{version} | {len(files)} files | zip {zpath.stat().st_size / 2 ** 20:.1f} MB")
    if dry:
        return print("Dry run: nothing uploaded.")

    for cmd in (("git", "add", "changelog.txt"), ("git", "commit", "-q", "-m", f"Release v{version}", "--allow-empty"), ("git", "push", "-q")):
        if run(*cmd).returncode:
            raise SystemExit(f"{' '.join(cmd)} failed; nothing was released.")
    r = run("gh", "release", "create", f"v{version}", str(zpath), "--repo", REPO, "--title", f"WoR Map Editor {version}",
            "--notes-file", str(HERE / "changelog.txt"))
    if r.returncode:
        raise SystemExit(f"Upload failed ({r.stderr.strip()}). Delete the half-made release v{version} on GitHub and run this again.")
    print(f"Published v{version}. Running editors offer it on their next start.")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1 or not all(x.isdigit() for x in args[0].split(".")):
        raise SystemExit(__doc__)
    main(args[0], "--dry-run" in sys.argv)
