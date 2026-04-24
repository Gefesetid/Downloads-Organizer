# Downloads Organizer

A command-line tool that automatically sorts files in your Downloads folder by type.
It creates categorized subfolders and moves files into them with duplicate name handling.

## What problem it solves
Your Downloads folder becomes a dumping ground. This tool brings order by grouping
hundreds of files into meaningful categories in seconds.

## Features
- Organizes files by extension into predefined categories (Images, Documents, Archives, etc.)
- Works with the default system Downloads folder or any custom path
- Handles duplicate file names by appending a copy suffix instead of overwriting
- Robust error handling: skips files that are in use and gives clear messages
- Logging with timestamps and severity levels

## Requirements
- Python 3.8 or higher (developed with 3.12)
- No external libraries – uses only the Python standard library (`pathlib`, `shutil`, `logging`)

## Installation and Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/Gefesetid/downloads-organizer.git
   cd downloads-organizer
2. Set up a virtual environment (recommended)
    ```bash
    python -m venv .venv
    source .venv/bin/activate      # Linux / macOS
    .venv\Scripts\activate         # Windows
3. Run the sorter
      ```bash
      python sorter.py
The script will ask for a path. Press Enter to use the default system Downloads folder.
If the folder does not exist, it exits with an error message.

### Example

(.venv) PS C:\Users\User\PycharmProjects\pythonProject2> python sorter.py
Введите путь к папке загрузок:
2026-04-24 21:59:48,948 - INFO - Папка определена автоматически
2026-04-24 21:59:48,979 - INFO - Перемещен: 1.12Firewolfv1.74.zip -> Archives/1.12Firewolfv1.74.zip
2026-04-24 21:59:48,980 - INFO - Перемещен: 4000_Essential_English_Words_all_books_en-en.apkg -> Miscellaneous/4000_Essential_English_Words_all_books_en-en.apkg
...
After execution, your Downloads folder will contain organized subfolders:
Images, Documents, Archives, Executables, Code, Miscellaneous.

### Sorting categories
- Images: .jpg, .jpeg, .png, .gif, .bmp, .svg, .webp

- Documents: .pdf, .docx, .doc, .txt, .xlsx, .pptx, .md

- Archives: .zip, .rar, .7z, .tar, .gz

- Executables: .exe, .msi, .deb, .dmg, .apk

- Code: .py, .js, .html, .css, .json, .xml, .csv

- Miscellaneous: everything else

### Error handling

- If the given folder does not exist, the program prints an error and exits with code 1.

- Files that are open in another program (e.g., a Word document) are skipped with a warning,
never causing a crash.

### License
MIT
