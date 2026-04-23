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
    def __init__(self, download_path: str):
        if Path.exists(Path(download_path)):
            self.download_path = Path(download_path)
        else:
            try:
                self.download_path = Path.home() / "Downloads"
                logging.info("Путь определен автоматически")
            except FileNotFoundError:
                logging.error(f"Ошибка пути")
                sys.exit(1)

    def _scan_files(self) -> list:
        self.file_list = list()
        for i in Path(self.download_path).iterdir():
            if i.is_file():
                self.file_list.append(i)
            # maybe later
            # elif i.is_dir():
            #     for k in i.iterdir():
            #         if k.is_file():
            #             self.file_list.append(k)
            #         elif k.is_dir():
            #             FileSorter._scan_files(k)
        return self.file_list

    def _get_category(self, extension: str) -> str:
        for d_name, pref_list in file_types:
            if extension in pref_list:
                return d_name
            else:
                return "Others"

    def _create_directories(self, categories: set):
        for category in categories:
            (self.download_path / category).mkdir(exist_ok=True)

    def _move_file(self, file_path: Path, category: str):
        dest = self.download_path / category / file_path.name
        if dest.exists():
            n = 1
            while dest.exists():
                dest = Path(str(self.download_path / category / file_path.stem) + "_" + str(n) + file_path.suffix)
                n += 1
            try:
                shutil.move(file_path, dest)
            except PermissionError:
                logging.warning(f"Доступ запрещен")
                pass
            except OSError:
                logging.error(f"Файл занят другим процессом")
                pass
        else:
            try:
                shutil.move(file_path, dest)
            except PermissionError:
                logging.warning(f"Доступ запрещен")
                pass
            except OSError:
                logging.error(f"Файл занят другим процессом")
                pass

    def organize(self):
        category_set = {self._get_category(i.suffix) for i in self._scan_files()}
        self._create_directories(category_set)
        for i in self._scan_files():
            self._move_file(i, self._get_category(i.suffix))
            logging.info(
                f"Перемещен: {i.name} -> {self._get_category(i.suffix)}/{i.name}"
            )


if __name__ == "__main__":
    try:
        sorter = FileSorter(str(input("Введите путь к папке загрузок: \n")))
    except KeyboardInterrupt:
        logging.info("Надо было что нибудь ввести -_-")
        sys.exit(1)
    sorter.organize()
