from core.tools.file_manager.FileContentManager import FileContentManager
from core.tools.handlers.handler_path import HandlerPath
from logger.logger import CustomLogger


class WpBaseStructure:
    def __init__(self, theme_path):
        self.error_log = CustomLogger().error_log
        self.fcontent_manager = FileContentManager()
        self.handler_path = HandlerPath()
        self.theme_path = theme_path


    def __create_folder(self, parent_folder, folder_name, label):
        try:
            isFolder = self.handler_path.find_file(folder_name, parent_folder)
            if not isFolder:
                isFolder = self.fcontent_manager.create_folder(parent_folder, folder_name)
                self.error_log(f'Папку < {folder_name}({label}) > створено!')
            else:
                self.error_log(f'Папка < {folder_name}({label}) > уже існує!')
            return isFolder
        except Exception as e:
            self.error_log(e)

    def create_inc(self, folder_name='inc', parent_folder=None):
        if not parent_folder:
            parent_folder = self.theme_path
        label = 'inc'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_admin_panel(self, folder_name='admin_panel', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_inc()
        label = 'admin_panel'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_admin_panel_scripts(self, folder_name='ap_scripts', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_admin_panel()
        label = 'ap_scripts'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_admin_panel_styles(self, folder_name='ap_styles', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_admin_panel()
        label = 'ap_styles'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_helper_func(self, folder_name='helper_func', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_inc()
        label = 'helper_func'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_endpoint(self, folder_name='endpoint', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_inc()
        label = 'endpoint'
        return self.__create_folder(parent_folder, folder_name, label)

    def create_custom_label(self, folder_name='custom_label', parent_folder=None):
        if not parent_folder:
            parent_folder = self.create_inc()
        label = 'custom_label'
        return self.__create_folder(parent_folder, folder_name, label)

    def base_deploy(self, isReturn=False):
        path_inc = self.create_inc(parent_folder=self.theme_path)
        path_ap = self.create_admin_panel(parent_folder=path_inc)
        path_hf = self.create_helper_func(parent_folder=path_inc)
        path_ep = self.create_endpoint(parent_folder=path_inc)
        path_cf = self.create_custom_label(parent_folder=path_inc)
        path_ap_script = self.create_admin_panel_scripts(parent_folder=path_ap)
        path_ap_styles = self.create_admin_panel_styles(parent_folder=path_ap)
        if isReturn:
            return [path_inc, path_ap, path_hf, path_ep, path_ap_script, path_ap_styles,path_cf]
