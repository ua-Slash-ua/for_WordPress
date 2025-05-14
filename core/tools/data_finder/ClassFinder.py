import importlib.util
import os
import re

from core.tools.file_manager.file_manager import FileManager
from logger.logger import CustomLogger


class ClassFinder:
    def __init__(self,start_dir,name_parentClass):
        self.start_dir = start_dir
        self.name_parentClass = name_parentClass

        self.error_log = CustomLogger().error_log  # або info_log, якщо логіка для інфо окрема
        self.file_manager = FileManager()

        self.found_classes = []

    def find_all_file_py(self):
        """
        Пошук усіх .py файлів у директорії self.start_dir (рекурсивно).
        :return: Список повних шляхів до .py файлів
        """
        py_files = []
        try:
            for root, _, files in os.walk(self.start_dir):
                for file in files:
                    if file.endswith('.py'):
                        full_path = os.path.join(root, file)
                        py_files.append(full_path)
        except Exception as e:
            self.error_log(e)
        return py_files

    def find_child_class(self):
        for file_path in self.find_all_file_py():
            with open(file_path, 'r', encoding='utf-8') as f:
                file_data = f.read()

            # regex шукає: class ClassName(BaseWpDeployer):
            pattern = rf'class\s+(\w+)\s*\(\s*{self.name_parentClass}\s*\)'
            matches = re.findall(pattern, file_data)

            if matches:
                for class_name in matches:
                    cls = self._load_class_from_file(file_path, class_name)
                    if cls:
                        self.found_classes.append(cls)

        return self.found_classes

    def _load_class_from_file(self, file_path, class_name):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, class_name):
                return getattr(module, class_name)
        return None