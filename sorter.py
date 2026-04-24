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

pin = False


class FileSorter:
    def __init__(self, download_path: str):
        if Path(download_path).exists():
            self.download_path = Path(download_path)
        else:
            self.download_path = Path.home() / "Downloads"
            logging.info("Путь определен автоматически")

    def _scan_files(self) -> list:
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

    def _get_category(self, extension: str) -> str:
        for pref_list in file_types:
            for c, extensions in pref_list.items():
                if extension in extensions:
                    return c
        return "Others"

    def _create_directories(self, categories: set):
        for category in categories:
            (self.download_path / category).mkdir(exist_ok=True)

    def _move_file(self, file_path: Path, category: str):
        dest = self.download_path / category / file_path.name
        if dest.exists():
            n = 1
            while dest.exists():
                dest = Path(f"{self.download_path / category / file_path.stem}_{n}{file_path.suffix}")
                n += 1
        try:
            shutil.move(file_path, dest)
            global pin
            pin = True
        except PermissionError:
            logging.warning(f"Доступ запрещен")
            global pin
            pin = False
            pass
        except OSError:
            logging.error(f"Файл занят другим процессом")
            global pin
            pin = False
            pass

    def organize(self):
        for i in self._scan_files():
            x = self._get_category(i.suffix.lower())
            if not (self.download_path / x).exists():
                self._create_directories({x})
            self._move_file(i, x)
            if pin:
                logging.info(
                    f"Перемещен: {i.name} -> {x}/{i.name}"
                )


if __name__ == "__main__":
    try:
        sorter = FileSorter(str(input("Введите путь к папке загрузок: \n")))
    except KeyboardInterrupt:
        logging.info("Надо было что нибудь ввести -_-")
        sys.exit(1)
    sorter.organize()
