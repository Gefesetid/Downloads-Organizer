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
    file_list = list()

    def __init__(self, download_path: str):
        if Path.exists(download_path):
            self.download_path = download_path
        else:
            try:
                self.download_path = Path.home() / "Downloads"
                print("Путь определен автоматически")
            except FileNotFoundError:
                sys.exit(1)

    def scan_files(self) -> list:
        for i in Path(self.download_path).iterdir():
            if i.is_file():
                FileSorter.file_list.append(i)
            elif i.is_dir():
                print(
                    f"Обнаружена папка {i.__name__}, хотите чтобы я отсортировал ее содержимое?(Да/Нет):"
                )
                answer = input()
                if answer == "Да":
                    for k in i.iterdir():
                        if k.is_file():
                            FileSorter.file_list.append(k)
                        elif k.is_dir():
                            return FileSorter.scan_files(k)
                elif answer == "Нет":
                    pass
                else:
                    print("Введите корректный запрос:")
        return FileSorter.file_list

    def get_category(self, extension: str) -> str:
        for d_name, pref_list in file_types:
            if extension in pref_list:
                return d_name
            else:
                return "Others"

    def create_directories(self, categories: set):
        for category in categories:
            (self.download_path / category).mkdir(exist_ok=True)

    def move_file(self, file_path: Path, category: str):
        dest = self.download_path / category / file_path.name
        if dest.exists():
            n = 1
            while dest.exists():
                dest = str(dest) + "_" + str(n)
                n += 1
            try:
                shutil.move(file_path, dest)
            except PermissionError as e:
                logging.warning(f"Доступ запрещен: {e}")
                pass
            except OSError as e:
                logging.error(f"Ошибка системы: {e}")
                pass
        else:
            try:
                shutil.move(file_path, dest)
            except PermissionError as e:
                logging.warning(f"Доступ запрещен: {e}")
                pass
            except OSError as e:
                logging.error(f"Ошибка системы: {e}")
                pass

    def organize(self):
        logging.info(
            f"Перемещен: {FileSorter.move_file.file_path.name} -> {FileSorter.move_file.category}/{FileSorter.move_file.file_path.name}"
        )
