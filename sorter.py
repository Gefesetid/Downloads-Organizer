import shutil  # imports
from pathlib import Path
import logging
import sys
import argparse
import csv
from datetime import datetime

logging.basicConfig(  # logging config
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

file_types = [  # extensions
    {"Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"]},
    {"Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".md"]},
    {"Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]},
    {"Executables": [".exe", ".msi", ".deb", ".dmg", ".apk"]},
    {"Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".csv"]},
]


def get_args():  # arguments for controlling the program passed at launch (optional, there are defaults)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", default="Downloads")
    parser.add_argument("-r", "--recursive", action="store_true", help="Do it for recursive")
    parser.add_argument("-dr", "--dry_run", action="store_true", help="Do it for preview")
    parser.add_argument("-u", "--undo", action="store_true", help="Save it in log")
    return parser.parse_args()


args = get_args()  # for working with arguments


class FileSorter:  # the sorting class itself
    def __init__(self, download_path: str = None, recursive=False, dry_run=False, undo=False):
        self.recursive = recursive  # - \
        self.dry_run = dry_run  # -------> argument defaults
        self.undo = undo  # ----------- /
        self.pin = False  # default for enabling move logs
        self.path_c = []  # future list of paths
        if download_path:
            if Path(download_path).exists():
                self.download_path = Path(download_path)  # saving the passed path to the argument
            else:
                logging.error("Specified folder does not exist:")
                sys.exit(1)
        elif not download_path:
            if (Path.home() / "Downloads").exists():  # checking for existence of Downloads folder
                self.download_path = Path.home() / "Downloads"  # auto-detecting path to Downloads
                logging.info("Folder detected automatically")
            else:
                logging.error("Standard Downloads folder not found")
                sys.exit(1)
        for i in file_types:
            for x, k in i.items():
                b = self.download_path / x
                self.path_c.append(b)  # creating a list of paths to category folders

    def scan_files(self) -> list:
        file_list = list()
        if self.recursive:  # checking for the passed argument - enabling recursion
            for file in self.download_path.rglob('*'):  # recursively retrieves everything from downloads (files, folders...)
                if file.is_file() and not any(file.is_relative_to(k) for k in self.path_c):
                    # ^ checking if the item is a file and not in any category folder
                    file_list.append(file)
        else:
            for file in self.download_path.glob('*'):  # same but without recursion
                if file.is_file() and not any(file.is_relative_to(k) for k in self.path_c):
                    file_list.append(file)
        return file_list

    def get_category(self, extension: str) -> str:  # determining the category by the passed extension
        for pref_list in file_types:
            for c, extensions in pref_list.items():
                if extension in extensions:
                    return c
        return "Miscellaneous"

    def move_file(self, file_path: Path, category: str):
        rel_src = file_path.relative_to(self.download_path)  # relative path to file
        self.moved = False  # default of successful move confirmation
        self.rel_src = rel_src  # moving rel_src to self for convenience
        dest = self.download_path / category / rel_src  # determining the destination path for the file
        if dest.exists():
            n = 1
            while dest.exists():  # resolving name conflict
                dest = Path(f"{self.download_path / category / rel_src.parent / rel_src.stem}_{n}{rel_src.suffix}")
                n += 1
        self.rel_dest = dest.relative_to(self.download_path)  # relative final destination for the file
        if not self.dry_run:  # if dry_run mode is not enabled
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)  # creating the folder recursively for the file
                shutil.move(file_path, dest)  # moving the file
                self.moved = True  # confirmation flag
                self.pin = True  # flag for logs
            except PermissionError:
                logging.warning(f"Permission denied")
                self.pin = False
                self.moved = False
            except OSError:
                logging.error(f"File is in use by another process")
                self.pin = False
                self.moved = False
        else:  # if dry_run is enabled
            self.pin = True
            self.moved = False

    def undo_org(self):  # class operation in undo mode
        if Path('history.log').exists():
            with open("history.log", "r", encoding='utf-8', newline='') as file:  # opening the log in read mode
                reader = csv.reader(file)  # line-by-line iterator from the file
                read_list = reversed([[Path(x) for x in y] for y in reader if y[0] != "Time"])
                # ^ iterator of reversed reader

                for row in read_list:
                    if row[-1].is_file():
                        row[1].parent.mkdir(parents=True, exist_ok=True)  # creating folder for reverse move
                        shutil.move(row[-1], row[1])  # reverse move
                    else:
                        logging.error(
                            f"Failed to rollback: {row[-1].relative_to(self.download_path)} -> {row[1].relative_to(self.download_path)}")

        else:
            logging.error("Move history is empty")
        Path("history.log").unlink(missing_ok=True)  # deleting the log file after successful reverse move

    def organize(self):  # standard class operation
        if not Path('history.log').exists():  # writing headers to file
            with open("history.log", "a", encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(("Time", "Moved from", "Moved to"))
        for file in self.scan_files():  # taking a file from the list
            category = self.get_category(file.suffix.lower())  # calculating the category
            self.move_file(file, category)  # moving
            if self.pin:  # logging to terminal for informativeness
                logging.info(
                    f"Moved: {self.rel_src} -> {self.rel_dest}"
                )
            if self.moved == True and not self.dry_run:  # if moved and not in dry_run mode
                with open("history.log", "a", encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)  # writing to the move history logs
                    writer.writerow((datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), self.download_path / self.rel_src,
                                     self.download_path / self.rel_dest))


if __name__ == "__main__":  # launch
    sorter = FileSorter(download_path=args.path, recursive=args.recursive, dry_run=args.dry_run, undo=args.undo)
    if args.undo:  # calling the appropriate module depending on the mode
        sorter.undo_org()
    else:
        sorter.organize()
