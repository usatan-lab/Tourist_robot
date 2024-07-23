from colorama import Fore, Style, init

import os
import string

def get_template_dir_path():
    template_dir_path = None
    try:
        import settings
        template_dir_path = getattr(settings, 'TEMPLATE_PATH', None)
    except ImportError:
        pass

    if not template_dir_path:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        template_dir_path = os.path.join(base_dir,'templates')

    return template_dir_path
class NoTemplateError(Exception):
    pass

def find_template(temp_file):
    template_dir_path = get_template_dir_path()
    temp_file_path = os.path.join(template_dir_path,temp_file)
    if not os.path.exists(temp_file_path):
        raise NoTemplateError('Could not find {}'.format(temp_file))
    return temp_file_path

def get_template(template_file_path, color=None):
    template = find_template(template_file_path)
    with open(template, 'r', encoding='utf-8') as template_file:
        contents = template_file.read()
        contents = contents.rstrip(os.linesep)
        pattern_length = 60
        pattern = '*-*-' * (pattern_length // 5)
        if pattern_length % 5 != 0:
            pattern += '*-*-*'[:(pattern_length % 5) * 2]
        contents = '{splitter}{sep}{contents}{sep}{splitter}{sep}'.format(
            contents=contents, splitter=pattern, sep=os.linesep)
        if color:
            color_code = getattr(Fore, color.upper(), Fore.RESET)
            contents = color_code + contents + Style.RESET_ALL

        return string.Template(contents)