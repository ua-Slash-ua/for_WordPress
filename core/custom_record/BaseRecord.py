import os.path

from core.custom_file_editors.FunctionEditor import FunctionEditor
from core.custom_themes.WpBaseStructure import WpBaseStructure
from core.tools.data_finder.ClassFinder import ClassFinder
from core.tools.data_finder.data_finder import DataFinder
from core.tools.file_manager.FileContentManager import FileContentManager
from core.tools.file_manager.file_manager import FileManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class BaseRecord:
    record_type = 'base'

    def __init__(self):
        self.data_t = {}

        self.handler_path = HandlerPath()
        self.fcontent_manager = FileContentManager()
        self.file_manager = FileManager()


        self.error_log = CustomLogger().error_log
        self.base_dir = self.handler_path.base_dir
        self.path_settings_record = self.handler_path.find_file('record_config.json', self.base_dir)
        self.settings_record = self.file_manager.read_file(self.path_settings_record)

        self.data_finder = DataFinder(self.settings_record)
        self.theme_path = self.data_finder.find('theme_path', 0)

        self.template_wp_dir = self.handler_path.find_file(['templates', 'wordpress'], self.handler_path.base_dir)

        self.ts_cls = WpBaseStructure(self.theme_path)
        self.data_t['full_path'], self.data_t['part_path'] = self.get_path()


    def _get_data_template(self, path_to_file: str, phrase: str, spliter: str = '/***/'):
        try:
            file_data = self.file_manager.read_file(path_to_file)
            index_start = file_data.find(phrase) + len(phrase)
            index_end = file_data[index_start:].find(spliter) + index_start
            data_result = file_data[index_start:index_end].strip()
            return data_result

        except Exception as e:
            self.error_log(e)


    def create_php(self, file_name, data: str, ftype: str = 'admin_panel'):
        try:
            path_to_functions = os.path.join(self.theme_path, 'functions.php')
            func_editor = FunctionEditor(path_to_functions)
            for pp, fp in zip(self.data_t['part_path'], self.data_t['full_path']):
                if pp.endswith(ftype):
                    part_path = self.data_t['part_path'][pp]
                    full_path = self.data_t['full_path'][fp]
                    break
            else:
                part_path = self.data_t['part_path']['part_path_to_inc']
                full_path = self.data_t['full_path']['full_path_to_inc']
            part_path = os.path.join(str(part_path), file_name)
            full_path = os.path.join(str(full_path), file_name)

            self.file_manager.write_file(full_path, data)
            func_editor.include_in_functions(part_path, 'admin_panel')
        except Exception as e:
            self.error_log(e)

    def create_js(self, file_name, data_inc, data_func):
        try:
            full_path = self.data_t['full_path']['full_path_to_js']
            full_path = os.path.join(str(full_path), file_name)
            data_js = '\n\n'.join(data_inc)
            data_js += "\n\ndocument.addEventListener('DOMContentLoaded',function (){\n\n"
            data_js += '\n\n'.join(data_func)
            data_js += "\n\n})"
            self.file_manager.write_file(full_path, data_js)
        except Exception as e:
            self.error_log(e)

    def create_css(self, file_name, data):
        try:
            full_path = self.data_t['full_path']['full_path_to_js']
            full_path = os.path.join(str(full_path), file_name)
            data = '\n\n'.join(data)
            self.file_manager.write_file(full_path, data)
        except Exception as e:
            self.error_log(e)

    def get_path(self):
        try:
            data_full = {}
            data_part = {}
            name_inc = self.data_finder.find('path_to_inc', 0)
            name_admin_panel = self.data_finder.find('path_to_admin_panel', 0)
            name_css = self.data_finder.find('path_to_css', 0)
            name_js = self.data_finder.find('path_to_js', 0)
            name_helpers_func = self.data_finder.find('path_to_helpers_func', 0)

            full_path_to_inc = self.ts_cls.create_inc(name_inc, self.theme_path)
            full_path_to_admin_panel = self.ts_cls.create_admin_panel(name_admin_panel, full_path_to_inc)
            full_path_to_css = self.ts_cls.create_admin_panel_styles(name_css, full_path_to_admin_panel)
            full_path_to_js = self.ts_cls.create_admin_panel_scripts(name_js, full_path_to_admin_panel)
            full_path_to_helpers_func = self.ts_cls.create_helper_func(name_helpers_func, full_path_to_inc)

            data_full['full_path_to_inc'] = full_path_to_inc
            data_full['full_path_to_admin_panel'] = full_path_to_admin_panel
            data_full['full_path_to_css'] = full_path_to_css
            data_full['full_path_to_js'] = full_path_to_js
            data_full['full_path_to_helpers_func'] = full_path_to_helpers_func
            for data in data_full:
                data_new = data.replace('full_', 'part_')
                data_part[data_new] = data_full[data].replace(self.theme_path, '')

            return data_full, data_part
        except Exception as e:
            self.error_log(e)

    def create(self):
        template_class_record = self.handler_path.find_file(['core', 'custom_record'], self.base_dir)
        class_finder = ClassFinder(template_class_record, 'BaseRecord')
        record_items = self.data_finder.find('records', 0)
        child_classes = class_finder.find_child_class()
        for record in record_items:
            for cls in child_classes:
                if self.data_finder.find('record_type', 0) == cls.record_type:
                    class_example = cls(record)
                    class_example.create()


if __name__ == '__main__':
    br = BaseRecord()
    br.create()
