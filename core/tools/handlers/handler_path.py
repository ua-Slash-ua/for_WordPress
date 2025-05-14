import os

from logger.logger import CustomLogger


import os
from logger.logger import CustomLogger

class HandlerPath:
    def __init__(self):
        self.error_log = CustomLogger().error_log
        self.base_dir = self.find_base_dir()


    @staticmethod
    def find_current_dir():
        """Повертає директорію, де знаходиться скрипт."""
        return os.path.dirname(os.path.abspath(__file__))

    def find_base_dir(self):
        """Шукає base_dir у поточній директорії та її батьківських папках."""
        current_dir = self.find_current_dir()
        base_dirs = ['core', 'logger']
        max_depth = 10

        for _ in range(max_depth):
            for sub_dir in base_dirs:
                potential_base_dir = os.path.join(current_dir, sub_dir)
                if os.path.isdir(potential_base_dir):
                    return current_dir
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        return None

    def find_file(self, file_name, base_dir: str):
        if isinstance(file_name, str):
            return self.find_file_by_name(file_name, base_dir)
        elif isinstance(file_name, list):
            return self.find_path_by_parts(file_name, base_dir)
        else:
            raise TypeError("file_name має бути рядком або списком рядків")

    def find_file_by_name(self, file_name: str, base_dir: str):
        for root, dirs, files in os.walk(base_dir):
            for f in files:
                if f.startswith(file_name):
                    return os.path.join(root, f)
            for d in dirs:
                if d.startswith(file_name):
                    return os.path.join(root, d)
        self.error_log(f" Файл або папку не знайдено, що починається з: {file_name}")
        return None

    def find_path_by_parts(self, path_parts: list, base_dir: str):
        """
        Шукає вкладений шлях, наприклад ['wordpress', 'environment_wordpress-6.8'], у дереві підкаталогів.
        """
        for root, dirs, files in os.walk(base_dir):
            current_path = root
            found = True

            for i, part in enumerate(path_parts):
                current_path = os.path.join(current_path, part)
                if not os.path.exists(current_path):
                    found = False
                    break
                if i < len(path_parts) - 1 and not os.path.isdir(current_path):
                    found = False
                    break

            if found:
                return current_path

        self.error_log(f" Шлях не знайдено: {'/'.join(path_parts)}")
        return None



if __name__ == '__main__':
    hp = HandlerPath()
    print(hp.base_dir)