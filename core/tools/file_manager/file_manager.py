import json

from logger.logger import CustomLogger


class FileManager:
    def __init__(self):
        self.error_log = CustomLogger().error_log

    def read_file(self, path_to_file: str):
        if path_to_file.endswith('.json'):
            return self.read_json(path_to_file)
        else:
            return self.read_other(path_to_file)

    def read_json(self, path_to_file: str):
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            self.error_log(e)
            return None

    def read_other(self, path_to_file: str):
        try:
            with open(path_to_file, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            self.error_log(e)
            return None

    def write_file(self, path_to_file: str, data, ftype = 'w'):
        if path_to_file.endswith('.json'):
            self.write_json(path_to_file, data, ftype)
        else:
            self.write_other(path_to_file, data, ftype)

    def write_json(self, path_to_file, data, ftype):
        try:
            with open(path_to_file, ftype, encoding='utf-8') as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            self.error_log(e)
    def write_other(self, path_to_file, data, ftype):
        try:
            with open(path_to_file, ftype, encoding='utf-8') as file:
                file.write(data)
        except Exception as e:
            self.error_log(e)
