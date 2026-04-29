# Downloads Organizer

A command-line utility that automatically sorts files in your  
Downloads folder (or any specified directory) by type.  
It creates categorized subfolders and moves files into them,  
handling duplicate names safely.

## What problem it solves
Your Downloads folder becomes a dumping ground. This tool brings order  
by grouping hundreds of files into meaningful categories in seconds,  
with support for recursive scanning, dry-run preview, and full undo.

## Features
- Organizes files by extension into predefined categories (Images, Documents, Archives, etc.)
- Works with the default system Downloads folder or any custom path (`-p/--path`)
- Recursive scanning (`-r/--recursive`) – processes nested folders
- Dry-run mode (`-dr/--dry_run`) – previews changes without touching files
- Undo last operation (`-u/--undo`) – reverses all moves using the history log
- Handles duplicate file names by appending a copy suffix instead of overwriting
- Robust error handling: skips files that are in use or inaccessible, with clear messages
- Logging with timestamps and severity levels (console + history log)

## Requirements
- Python 3.8 or higher (developed with 3.12)
- No external libraries – uses only the Python standard library (`pathlib`, `shutil`, `logging`, `csv`)

## Installation and Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd downloads-organizer
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Linux / macOS
   .venv\Scripts\activate         # Windows
   ```

3. **Run the sorter**
   ```bash
   python sorter.py [options]
   ```

### Command-line arguments


| Flag | Long form | Description |
| :--- | :--- | :--- |
| `-p` | `--path` | Path to the folder to organize (default: Downloads) |
| `-r` | `--recursive` | Scan folders recursively |
| `-dr` | `--dry_run` | Show what would be moved without actually moving |
| `-u` | `--undo` | Reverse the last organization (uses history.log) |

If run without arguments, the script uses the Downloads folder in the current working directory.  
If that folder does not exist, it attempts to auto-detect the system Downloads folder.

### Examples
**Basic usage (current Downloads folder)**
```bash
python sorter.py
```

**Custom folder, recursive, dry-run**
```bash
python sorter.py -p /home/user/MyDownloads -r -dr
```

**Undo the last organization**
```bash
python sorter.py -u
```

### Example output
```text
2026-04-24 21:59:48,948 - INFO - Folder detected automatically
2026-04-24 21:59:48,979 - INFO - Moved: 1.12Firewolfv1.74.zip -> Archives/1.12Firewolfv1.74.zip
2026-04-24 21:59:48,980 - INFO - Moved: 4000_Essential_English_Words_all_books_en-en.apkg -> Miscellaneous/4000_Essential_English_Words_all_books_en-en.apkg
...
```

After execution, the target folder will contain organized subfolders:  
**Images, Documents, Archives, Executables, Code, Miscellaneous.**

### Sorting categories
- **Images:** .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp
- **Documents:** .pdf, .docx, .doc, .txt, .xlsx, .pptx, .md
- **Archives:** .zip, .rar, .7z, .tar, .gz
- **Executables:** .exe, .msi, .deb, .dmg, .apk
- **Code:** .py, .js, .html, .css, .json, .xml, .csv
- **Miscellaneous:** everything else

## Undo mechanism
When files are moved, a `history.log` file is created (or appended) recording each move.  
The `-u` flag reads this log, reverses all recorded moves in reverse order,  
and then deletes the log file. If no log exists, an error is shown.

Useful if you accidentally ran the sorter on the wrong folder or want to restore the previous state.

## Error handling
- If the specified folder does not exist, the program prints an error and exits with code 1.
- Files that are open in another program or lack permissions are skipped with a warning.
- The dry-run mode allows you to safely check what would happen.

## License
MIT
