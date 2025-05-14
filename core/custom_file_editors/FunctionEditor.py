import os.path

from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class FunctionEditor:
    def __init__(self, path_fo_func):
        self.path_fo_func = path_fo_func

        self.handler_path = HandlerPath()
        self.file_manager = FileManager()
        self.error_log = CustomLogger().error_log
        self.template_wp_dir = self.handler_path.find_file(['templates', 'wordpress'], self.handler_path.base_dir)


    def include_in_functions(self, part_path, ctype = 'admin_panel'):

        try:
            data_func = self.file_manager.read_file(self.path_fo_func)
            start_path = 'THEME_PATH' if 'THEME_PATH' in data_func else 'get_template_directory()'
            inc_line = f"require {start_path} . '{part_path}';"
            if part_path not in data_func:
                if ctype in data_func:
                    index_start = data_func.find(f'{ctype}')
                    index_start = data_func[index_start:].find('//') + index_start
                    index_start = data_func[:index_start].rfind(';')+1
                    data_func = data_func[:index_start] + f'\n{inc_line}\n' + data_func[index_start:]
                    self.file_manager.write_file(self.path_fo_func,data_func)
                else:
                    print('-')
                    self.file_manager.write_file(self.path_fo_func, inc_line, ftype = 'a+')
                self.error_log(f'< {part_path} > підключено у < functions.php >', 'forget')
            else:
                self.error_log(f'< {part_path} > уже підключено у < functions.php >')
        except Exception as e:
            self.error_log(e)

    def get_func_content(self):
        try:
            data_list =[]
            path_to_fit = self.handler_path.find_file('func_content.txt', self.template_wp_dir)
            data_str = self.file_manager.read_file(path_to_fit)
            data_list.append(data_str)
            for d in self.get_all_include():
                data_list.append(d)
            return data_list
        except Exception as e:
            self.error_log(e)
            return ['<?php\n']

    def get_all_include(self):
        try:
            path_to_fit = self.handler_path.find_file('func_inc_types.txt', self.template_wp_dir)
            data_str = self.file_manager.read_file(path_to_fit)
            data_list = [inc.strip() for inc in data_str.split('\n') if str(inc.strip()).startswith('// Include')]
            return data_list
        except Exception as e:
            self.error_log(e)
            return []


if __name__ == '__main__':
    pass
