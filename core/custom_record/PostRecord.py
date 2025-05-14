import os
from core.custom_record.BaseRecord import BaseRecord
from core.tools.data_finder.data_finder import DataFinder


class PostRecord(BaseRecord):
    record_type = 'post'

    def __init__(self, record):
        self.record = record
        super().__init__()

        self.record_fmanager = DataFinder(record)

        self.path_to_main_post = self.handler_path.find_file('main_post', self.template_wp_dir)

        self.record_name = self.record['record_name'].lower()
        self.record_icon = self.record['record_icon']
        self.record_smslug = f"'{self.record['record_menu']}'" if self.record['record_menu'].strip() else 'true'

        self.data_php = ['<?php\n']
        self.data_php_get = []
        self.data_php_proc = []
        self.data_css = set()
        self.data_js_functions = set()
        self.data_js_include = []

        self.part_path_js = ''
        self.part_path_css = ''

    def _replace_label(self, data: str, label, label_name='', another_data_replace=None):
        try:
            if another_data_replace is None:
                another_data_replace = {}
            data_replace = {
                'LLABEL': label_name.lower(),
                'CLABEL': label_name.capitalize(),
                'INPUT_TYPE': label,
                'INPUT_STYPE': label.replace('input_', ''),
            }
            for k in data_replace:
                if k in data:
                    data = data.replace(k, data_replace[k])
            if another_data_replace:
                for ak in another_data_replace:
                    if ak in data:
                        data = data.replace(ak, another_data_replace[ak])
            return data
        except Exception as e:
            self.error_log(e)
            return data

    def __create_input(self, label, label_names):
        try:
            data = []
            path_to_input_post = self.handler_path.find_file('input_post', self.template_wp_dir)
            input_data = self._get_data_template(path_to_input_post, 'DATA_INPUT')
            input_get = self._get_data_template(path_to_input_post, 'GET_INPUT')
            input_proc = self._get_data_template(path_to_input_post, 'PROCESS_INPUT')
            input_class = self._get_data_template(path_to_input_post, 'CONCLASS_INPUT')
            data.append(f'          <div class="{self._replace_label(input_class, label)}">')
            for label_name in label_names:
                if label == 'input_checkbox':
                    input_data = self._get_data_template(path_to_input_post, 'DATA_CHECKBOX_INPUT')
                    input_proc = self._get_data_template(path_to_input_post, 'PROCESS_CHECKBOX_INPUT')

                data.append(self._replace_label(input_data, label, label_name))
                self.data_php_proc.append(self._replace_label(input_proc, label, label_name))
                self.data_php_get.append(self._replace_label(input_get, label, label_name))
            data.append('\n           </div>')

            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_textarea(self, label, label_names):
        try:
            data = []
            path_to_textarea_post = self.handler_path.find_file('textarea_post', self.template_wp_dir)
            textarea_data = self._get_data_template(path_to_textarea_post, 'DATA_TEXTAREA')
            textarea_get = self._get_data_template(path_to_textarea_post, 'GET_TEXTAREA')
            textarea_proc = self._get_data_template(path_to_textarea_post, 'PROCESS_TEXTAREA')
            textarea_class = self._get_data_template(path_to_textarea_post, 'CONCLASS_TEXTAREA')
            data.append(f'          <div class="{self._replace_label(textarea_class, label)}">')
            for label_name in label_names:
                data.append(self._replace_label(textarea_data, label, label_name))
                self.data_php_proc.append(self._replace_label(textarea_proc, label, label_name))
                self.data_php_get.append(self._replace_label(textarea_get, label, label_name))
            data.append('\n           </div>')

            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_img(self, label, label_names):
        try:
            data = []
            l_n = []
            path_to_img_post = self.handler_path.find_file('img_post', self.template_wp_dir)
            img_link_data = self._get_data_template(path_to_img_post, 'DATA_IMG_LINK')
            img_link_get = self._get_data_template(path_to_img_post, 'GET_IMG_LINK')
            img_link_proc = self._get_data_template(path_to_img_post, 'PROCESS_IMG_LINK')
            img_link_class = self._get_data_template(path_to_img_post, 'CONCLASS_IMG_LINK')
            img_link_func = self._get_data_template(path_to_img_post, 'IMG_LINK_FUNCTIONS')
            img_link_inc = self._get_data_template(path_to_img_post, 'IMG_LINK_INC')
            self.data_js_functions.add(img_link_func)
            data.append(f'          <div class="{self._replace_label(img_link_class, label)}">')
            for label_name in label_names:
                l_n.append(label_name)
                data.append(self._replace_label(img_link_data, label, label_name))
                self.data_php_proc.append(self._replace_label(img_link_proc, label, label_name))
                self.data_php_get.append(self._replace_label(img_link_get, label, label_name))
            data.append('\n           </div>')
            self.data_js_include.append(img_link_inc.replace('DATA_IMG_LINK_VALUES', f"', '".join(l_n)))
            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_svg(self, label, label_names):
        try:
            data = []
            l_n = []
            path_to_img_post = self.handler_path.find_file('img_post', self.template_wp_dir)
            svg_data = self._get_data_template(path_to_img_post, 'DATA_SVG')
            svg_get = self._get_data_template(path_to_img_post, 'GET_SVG')
            svg_proc = self._get_data_template(path_to_img_post, 'PROCESS_SVG')
            svg_class = self._get_data_template(path_to_img_post, 'CONCLASS_SVG')
            svg_func = self._get_data_template(path_to_img_post, 'SVG_FUNCTIONS')
            svg_inc = self._get_data_template(path_to_img_post, 'SVG_INC')
            self.data_js_functions.add(svg_func)
            data.append(f'          <div class="{self._replace_label(svg_class, label)}">')
            for label_name in label_names:
                l_n.append(label_name)
                data.append(self._replace_label(svg_data, label, label_name))
                self.data_php_proc.append(self._replace_label(svg_proc, label, label_name))
                self.data_php_get.append(self._replace_label(svg_get, label, label_name))
            data.append('\n           </div>')
            self.data_js_include.append(svg_inc.replace('DATA_SVG_VALUES', f"', '".join(l_n)))
            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_video(self, label, label_names):
        try:
            data = []
            l_n = []
            path_to_video_post = self.handler_path.find_file('video_post', self.template_wp_dir)
            video_data = self._get_data_template(path_to_video_post, 'DATA_VIDEO')
            video_get = self._get_data_template(path_to_video_post, 'GET_VIDEO')
            video_proc = self._get_data_template(path_to_video_post, 'PROCESS_VIDEO')
            video_class = self._get_data_template(path_to_video_post, 'CONCLASS_VIDEO')
            video_func = self._get_data_template(path_to_video_post, 'VIDEO_FUNCTIONS')
            video_inc = self._get_data_template(path_to_video_post, 'VIDEO_INC')
            self.data_js_functions.add(video_func)
            data.append(f'          <div class="{self._replace_label(video_class, label)}">')
            for label_name in label_names:
                l_n.append(label_name)
                data.append(self._replace_label(video_data, label, label_name))
                self.data_php_proc.append(self._replace_label(video_proc, label, label_name))
                self.data_php_get.append(self._replace_label(video_get, label, label_name))
            data.append('\n           </div>')
            self.data_js_include.append(video_inc.replace('DATA_VIDEO_VALUES', f"', '".join(l_n)))
            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_points(self, label, label_names):
        try:
            data = []
            l_n = []
            path_to_point_post = self.handler_path.find_file('point_post', self.template_wp_dir)
            point_data = self._get_data_template(path_to_point_post, 'DATA_POINTS')
            point_get = self._get_data_template(path_to_point_post, 'GET_POINTS')
            point_proc = self._get_data_template(path_to_point_post, 'PROCESS_POINTS')
            point_class = self._get_data_template(path_to_point_post, 'CONCLASS_POINTS')
            point_func = self._get_data_template(path_to_point_post, 'POINTS_FUNCTIONS')
            point_inc = self._get_data_template(path_to_point_post, 'POINTS_INC')
            self.data_js_functions.add(point_func)
            data.append(f'          <div class="{self._replace_label(point_class, label)}">')
            for label_name in label_names:
                l_n.append(label_name)
                data.append(self._replace_label(point_data, label, label_name))
                self.data_php_proc.append(self._replace_label(point_proc, label, label_name))
                self.data_php_get.append(self._replace_label(point_get, label, label_name))
            data.append('\n           </div>')
            self.data_js_include.append(point_inc.replace('DATA_POINTS_VALUES', f"', '".join(l_n)))
            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def __create_table(self, label, tables):
        try:
            data = []
            data_js_inc = []

            path_to_table_post = self.handler_path.find_file('table_post', self.template_wp_dir)
            table_data = self._get_data_template(path_to_table_post, 'DATA_TABLE')
            table_input_data = self._get_data_template(path_to_table_post, 'DATA_INPUT_TABLE')
            table_textarea_data = self._get_data_template(path_to_table_post, 'DATA_TEXTAREA_TABLE')
            table_get_data = self._get_data_template(path_to_table_post, 'GET_TABLE')
            table_proc_data = self._get_data_template(path_to_table_post, 'PROCESS_TABLE')
            table_cls_data = self._get_data_template(path_to_table_post, 'CONCLASS_TABLE')
            table_func_data = self._get_data_template(path_to_table_post, 'TABLE_FUNCTIONS')
            table_inc_data = self._get_data_template(path_to_table_post, 'TABLE_INC')
            self.data_js_functions.add(table_func_data)
            data.append(f'          <div class="{self._replace_label(table_cls_data, label)}">')
            for table in tables:
                data_label_table = []
                data_head_table = []
                table_name = list(table.keys())[0]
                table_labels = table[table_name]
                self.data_php_proc.append(self._replace_label(table_proc_data, label, table_name))
                self.data_php_get.append(self._replace_label(table_get_data, label, table_name))
                for label in table_labels:
                    replace_data = {
                        'LINLABEL': label.lower(),
                        'CINLABEL': label.capitalize()
                    }
                    if str(label).endswith('_'):
                        data_label_table.append(
                            self._replace_label(table_textarea_data, '', table_name, replace_data))
                    else:
                        data_label_table.append(
                            self._replace_label(table_input_data, '', table_name, replace_data))
                    data_head_table.append(f'<th>{label.capitalize()}</th>')

                replace_data = {
                    'LABELTABLE': '\n'.join(data_label_table),
                    'HEADTABLE': '\n'.join(data_head_table)
                }
                data.append(
                    self._replace_label(table_data, '', table_name, replace_data))


                data_js_inc.append(f"{{'{table_name}':['{"','".join(table_labels)}']}}")
                print(table_name)
                print(table_labels)
            data.append('\n           </div>')
            self.data_js_include.append(table_inc_data.replace('DATA_TABLE_VALUES', ',\n'.join(data_js_inc)))

            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def _get_labels_render(self, labels):

        try:
            data = []
            for k in labels:
                if not labels[k]:
                    continue
                if str(k).startswith('input'):
                    data.append(self.__create_input(k, labels[k]))
                elif str(k).startswith('img_link'):
                    data.append(self.__create_img(k, labels[k]))
                elif str(k).startswith('img_svg'):
                    data.append(self.__create_svg(k, labels[k]))
                elif str(k).startswith('point'):
                    data.append(self.__create_points(k, labels[k]))
                elif str(k).startswith('video'):
                    data.append(self.__create_video(k, labels[k]))
                elif str(k).startswith('table'):
                    data.append(self.__create_table(k, labels[k]))
                elif str(k).startswith('textarea'):
                    data.append(self.__create_textarea(k, labels[k]))

            data = '\n'.join(data)
            return data
        except Exception as e:
            self.error_log(e)
            return ''

    def _get_tab_render(self, tab_items):
        tab_data_main = ''
        data_tab_head = []
        data_tab_content = []
        tab_names_list = []
        try:
            path_to_tab_post = self.handler_path.find_file('tab_post', self.template_wp_dir)
            path_to_js_post = self.handler_path.find_file('js_post', self.template_wp_dir)
            path_to_css_post = self.handler_path.find_file('css_post', self.template_wp_dir)
            if len(tab_items) > 1:
                self.data_js_functions.add(self._get_data_template(path_to_js_post, 'TAB FUNCTIONS'))
                self.data_css.add(self._get_data_template(path_to_css_post, 'TAB STYLES'))

                tab_data_ac_head = self._get_data_template(path_to_tab_post, 'TAB ACTIVE HEAD')
                tab_data_head = self._get_data_template(path_to_tab_post, 'TAB HEAD')
                tab_data_ac_content = self._get_data_template(path_to_tab_post, 'TAB ACTIVE BODY')
                tab_data_content = self._get_data_template(path_to_tab_post, 'TAB BODY')
                status_active = True
                for tab in tab_items:
                    name = tab['tab_name']
                    tab_names_list.append(f"'{name}'")
                    if status_active:
                        dth_line = tab_data_ac_head.replace('L_TNAME', name.lower()).replace('C_TNAME',
                                                                                             name.capitalize())
                        dtc_line = tab_data_ac_content.replace('L_TNAME', name.lower()).replace('C_TNAME',
                                                                                                name.capitalize())
                        status_active = False
                    else:
                        dth_line = tab_data_head.replace('L_TNAME', name.lower()).replace('C_TNAME',
                                                                                          name.capitalize())
                        dtc_line = tab_data_content.replace('L_TNAME', name.lower()).replace('C_TNAME',

                                                                                             name.capitalize())
                    dtc_line = dtc_line.replace('T_CONTENT', self._get_labels_render(tab['tab_items']))
                    data_tab_head.append(dth_line)
                    data_tab_content.append(dtc_line)

                self.data_js_include.append(
                    self._get_data_template(path_to_js_post, 'TAB INCLUDE').replace('DATA_TAB_VALUES',
                                                                                    ','.join(tab_names_list)))
                tab_data_main = self._get_data_template(path_to_tab_post, 'TAB MAIN')
                tab_data_main = tab_data_main.replace('TAB_HEAD', '\n'.join(data_tab_head))
                tab_data_main = tab_data_main.replace('TAB_BODY', '\n'.join(data_tab_content))

            else:
                tab_data_main = self._get_labels_render(tab_items[0]['tab_items'])
            return tab_data_main
        except Exception as e:
            self.error_log(e)

    def _post_record_replacer(self, data: list):
        data = '\n\n'.join(data)
        try:
            data_replace = {
                'L_RNAME': self.record_name,
                'C_RNAME': self.record_name.capitalize(),
                'RICON': self.record_icon,
                'RSUBMSLUG': self.record_smslug,
                'PATH_CSS': self.part_path_css.replace('\\', '/'),
                'PATH_JS': self.part_path_js.replace('\\', '/'),
            }
            for k in data_replace:
                if k in data:
                    data = data.replace(k, data_replace[k])
            return data
        except Exception as e:
            self.error_log(e)
            return data

    def _post_mb_register_replacer(self, phrase, mb_item):
        data = self._get_data_template(self.path_to_main_post, phrase)
        mb_name = mb_item['mb_name']
        mb_position = mb_item['mb_position']
        mb_priority = mb_item['mb_priority']
        try:
            data_replace = {
                'L_MBNAME': mb_name.lower(),
                'C_MBNAME': mb_name.capitalize(),
                'MB_POSITION': mb_position,
                'MB_PRIORITY': mb_priority,
            }
            for k in data_replace:
                if k in data:
                    data = data.replace(k, data_replace[k])
            return data
        except Exception as e:
            self.error_log(e)
            return data

    def _post_mb_render_replacer(self, phrase, mb_item):
        self.data_php_get = []
        mb_name = mb_item['mb_name']
        data = self._get_data_template(self.path_to_main_post, phrase)
        data_render = self._get_tab_render(mb_item['mb_items'])
        data_inc = '\n'.join(self.data_php_get)
        try:
            data_replace = {
                'L_MBNAME': mb_name.lower(),
                'DATA_LABEL_RENDER': data_render if data_render else '"None"',
                'DATA_LABEL_INC': data_inc if data_inc else '"None"',

            }
            for k in data_replace:
                if k in data:
                    data = data.replace(k, data_replace[k])
            return data
        except Exception as e:
            self.error_log(e)
            return data

    def add_main_other_data(self, phrase_list: list):
        try:
            for phrase in phrase_list:
                data_str = self._get_data_template(self.path_to_main_post, phrase)
                if phrase == 'INCLUDE_LABEL':
                    data_str = data_str.replace('DATA_LABEL', ',\n'.join(self.data_php_proc))
                self.data_php.append(data_str)
        except Exception as e:
            self.error_log(e)

    def create_meta_boxes(self, meta_boxes):
        for mb_item in meta_boxes:
            mb_register = self._post_mb_register_replacer('REGISTER_META_BOX', mb_item)
            mb_render = self._post_mb_render_replacer('RENDER_META_BOX', mb_item)
            self.data_php.append(mb_register)
            self.data_php.append(mb_render)

    def create(self):
        self.add_main_other_data(['CREATE_POST_TYPE', 'REGISTER_REST_API_META_FIELDS'])
        self.create_meta_boxes(self.record['record_items'])
        self.add_main_other_data(['INCLUDE_LABEL'])
        name_php = f'ap_{self.record_name}.php'
        name_js = f'{self.record_name}_script.js'
        name_css = f'{self.record_name}_style.css'
        self.part_path_js = os.path.join(str(self.data_t['part_path']['part_path_to_js']), name_js)
        self.part_path_css = os.path.join(str(self.data_t['part_path']['part_path_to_css']), name_css)
        self.add_main_other_data(['SAVE_META_FIELDS', 'INCLUDE_SCRIPTS_AND_STYLES'])
        self.data_php = self._post_record_replacer(self.data_php)
        self.create_php(name_php, self.data_php, 'admin_panel')
        self.create_js(name_js, self.data_js_functions, self.data_js_include)
        self.create_css(name_css, self.data_css)
