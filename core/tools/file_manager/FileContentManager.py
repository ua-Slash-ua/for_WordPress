import os
import pathlib
import shutil

from logger.logger import CustomLogger


class FileContentManager:
    def __init__(self):
        self.error_log = CustomLogger().error_log

    def create_folder(self, base_path:str, folder_name:str, exist_ok:bool = False):
        try:
            full_path_to_folder = os.path.join(base_path,folder_name)
            os.makedirs(full_path_to_folder,exist_ok=exist_ok)
            self.error_log(f'Папка {folder_name} за шляхом {full_path_to_folder} створена!')
            return full_path_to_folder
        except Exception as e:
            self.error_log(e)

    def delete_path(self, path: str, delete_self: bool = False, starts_with: str = ''):
        """
        Видаляє файл, вміст папки або окремі елементи в папці, які починаються з заданого рядка.

        :param path: Шлях до файлу або папки.
        :param delete_self: Якщо True — видаляє саму папку.
        :param starts_with: Якщо задано — видаляються тільки елементи, що починаються з цього рядка.
        """
        try:
            if not os.path.exists(path):
                return self.error_log(f' Шлях не знайдено: {path}')

            if os.path.isfile(path) or os.path.islink(path):
                if starts_with == '' or os.path.basename(path).startswith(starts_with):
                    os.remove(path)
                    return self.error_log(f' Файл або лінк видалено: {path}')
                else:
                    return self.error_log(f' Файл не відповідає умові starts_with="{starts_with}": {path}')

            if delete_self and starts_with == '':
                shutil.rmtree(path)
                return self.error_log(f' Папка з вмістом видалена: {path}')

            deleted_any = False
            for entry in os.scandir(path):
                name = entry.name
                if starts_with and not name.startswith(starts_with):
                    continue

                if entry.is_file() or entry.is_symlink():
                    os.remove(entry.path)
                    deleted_any = True
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
                    deleted_any = True

            if starts_with:
                return self.error_log(
                    f' Видалено елементи в папці {path}, які починаються з "{starts_with}"'
                    if deleted_any else
                    f' Не знайдено елементів у {path}, які починаються з "{starts_with}"'
                )

            if delete_self:
                shutil.rmtree(path)
                return self.error_log(f' Папка з вмістом видалена: {path}')
            else:
                return self.error_log(f' Вміст папки очищено: {path}')

        except Exception as e:
            self.error_log(e)

    def is_larger_than(self, path: str, size_bytes: int, reverse: bool = False) -> bool:
        """
        Перевіряє, чи розмір файлу/папки більший за заданий розмір.

        :param path: Шлях до файлу або папки
        :param size_bytes: Розмір у байтах, з яким порівнювати
        :param reverse: Якщо True — перевіряє, чи менший за size_bytes
        :return: True або False
        """
        try:
            if not os.path.exists(path):
                self.error_log(f'[is_larger_than] Шлях не існує: {path}')
                return False

            total_size = 0

            if os.path.isfile(path):
                total_size = os.path.getsize(path)
            elif os.path.isdir(path):
                for dirpath, dirnames, filenames in os.walk(path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        if os.path.isfile(fp):
                            total_size += os.path.getsize(fp)

            result = total_size < size_bytes if reverse else total_size > size_bytes
            return result

        except Exception as e:
            self.error_log(e)
            return False

    def copy_files(self, src: str, dst: str, parent: bool = False):
        """
        Копіює файли з src у dst. Якщо parent=True — копіюється також сама src-папка як підпапка.

        :param src: шлях до вихідної папки
        :param dst: шлях до папки призначення
        :param parent: чи включати саму папку src у копіювання
        """
        try:
            if not os.path.exists(src):
                return self.error_log(f"Шлях не знайдено: {src}")

            if parent:
                folder_name = os.path.basename(os.path.normpath(src))
                dst = os.path.join(dst, folder_name)

            shutil.copytree(src, dst, dirs_exist_ok=True)
            self.error_log(f"Файли успішно скопійовано з {src} до {dst}")

        except Exception as e:
            self.error_log(e)