# Fernrel Character Sheet

Fernrel's D&D character binder (Astral Elf Monster Slayer Ranger, level 16). It started as a claude.ai artifact (https://claude.ai/artifact/JDocx2rXRHi5dH4xPNHHmC) and runs fully on its own here, with no Claude and no internet needed.

## Open it

You need Python 3 (already installed on most Macs and Linux machines; on Windows, get it from python.org).

```sh
cd FernrelCharacterSheetDnD
python3 server.py
```

Your browser opens http://localhost:8000. Leave the terminal open while you use the sheet, and press Ctrl+C there when you're done. To use a different port: `python3 server.py 8123`.

Everything works the same as the artifact: Edit mode, HP damage and healing, trackers, short and long rests, search, and uploading art. Changes save straight into the files in this folder.

Opening `index.html` by double-clicking won't work, because the browser blocks it from loading `sheet.json`. Always start it with `server.py`.

## Files

| Path | What it is |
|---|---|
| `index.html` | The page: layout, cobblestone background, lightning, trackers, search, rests |
| `sheet.json` | All of Fernrel's data: stats, spells, features, gear, notes |
| `art/` | Uploaded character art |
| `fonts/` | Bundled copies of Alegreya, Alegreya Sans and Marcellus (SIL Open Font License), so it looks right offline |
| `server.py` | Tiny local server that shows the page and saves your edits (Python standard library only) |
| `backups/` | Created on first save. Every save keeps the previous `sheet.json` here with a date and time (newest 200 kept) |

## Undoing a mistake

Stop the server, copy the backup you want from `backups/` over `sheet.json`, and start it again.

## Keeping it safe

`sheet.json` and `art/` are the only things that change. Back up this folder (or just those two) anywhere you like, such as a USB drive or cloud storage. You can also edit `sheet.json` by hand in any text editor; it's plain JSON.

## Saving history with git

This folder is a git repository. The server saves edits to the files but doesn't commit them, so commit after a session to keep a permanent snapshot:

```sh
git add -A
git commit -m "After session 12"
```

`git log` lists your snapshots. `git diff` shows what changed since the last one. `backups/` isn't tracked, since git already keeps the history.

## The artifact and this folder

They are separate copies. Edits made on the claude.ai artifact don't show up here, and edits made here don't go back to the artifact.
