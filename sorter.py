import shutil
from pathlib import Path
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

file_types = [
    {"Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"]},
    {"Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".md"]},
    {"Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]},
    {"Executables": [".exe", ".msi", ".deb", ".dmg", ".apk"]},
    {"Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".csv"]},
]


class FileSorter:
    def __init__(self, download_path: str = None):
        self.pin = False
        if download_path:
            if Path(download_path).exists():
                self.download_path = Path(download_path)
            else:
                logging.error("Указанная папка не существует:")
                sys.exit(1)
        elif not download_path:
            if (Path.home() / "Downloads").exists():
                self.download_path = Path.home() / "Downloads"
                logging.info("Папка определена автоматически")
            else:
                logging.error("Стандартная папка Downloads не найдена")
                sys.exit(1)

    def scan_files(self) -> list:
        file_list = list()
        for i in self.download_path.iterdir():
            if i.is_file():
                file_list.append(i)
            # maybe later
            # elif i.is_dir():
            #     for k in i.iterdir():
            #         if k.is_file():
            #             self.file_list.append(k)
            #         elif k.is_dir():
            #             FileSorter._scan_files(k)
        return file_list

    def get_category(self, extension: str) -> str:
        for pref_list in file_types:
            for c, extensions in pref_list.items():
                if extension in extensions:
                    return c
        return "Miscellaneous"

    def create_directories(self, categories: set):
        for category in categories:
            (self.download_path / category).mkdir(exist_ok=True)

    def move_file(self, file_path: Path, category: str):
        dest = self.download_path / category / file_path.name
        if dest.exists():
            n = 1
            while dest.exists():
                dest = Path(f"{self.download_path / category / file_path.stem}_{n}{file_path.suffix}")
                n += 1
        try:
            self.dest = dest
            shutil.move(file_path, dest)
            self.pin = True
        except PermissionError:
            logging.warning(f"Доступ запрещен")
            self.pin = False
            pass
        except OSError:
            logging.error(f"Файл занят другим процессом")
            self.pin = False
            pass

    def organize(self):
        for i in self.scan_files():
            x = self.get_category(i.suffix.lower())
            if not (self.download_path / x).exists():
                self.create_directories({x})
            self.move_file(i, x)
            if self.pin:
                logging.info(
                    f"Перемещен: {i.name} -> {x}/{self.dest.name}"
                )


if __name__ == "__main__":
    try:
        sorter = FileSorter(str(input("Введите путь к папке загрузок: \n")))
    except KeyboardInterrupt:
        logging.info("Надо было что нибудь ввести -_-")
        sys.exit(1)
    sorter.organize()
