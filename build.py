import json
import logging
import os
import shutil
import zipfile

from aseprite_ini import Aseini

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('build')

project_root_dir = os.path.dirname(__file__)
assets_dir = os.path.join(project_root_dir, 'assets')
build_dir = os.path.join(project_root_dir, 'build')
outputs_dir = os.path.join(build_dir, 'outputs')
releases_dir = os.path.join(build_dir, 'releases')


def main():
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(outputs_dir)
    os.makedirs(releases_dir)

    strings_en = Aseini.load(os.path.join(assets_dir, 'en.ini'))
    strings_zh_hans = Aseini.load(os.path.join(assets_dir, 'zh-hans.ini'))
    for section_name, section in strings_zh_hans.items():
        for key, value in section.items():
            if '\\n' in value:
                value = value.replace('\\n', '\n')
                value = f'<<<END\n{value}\nEND'
                strings_zh_hans[section_name][key] = value
    zh_hans_old_file_path = os.path.join(outputs_dir, 'zh-hans.ini')
    strings_zh_hans.save(zh_hans_old_file_path, strings_en)
    logger.info("Make old format strings: 'zh-hans.ini'")

    package_json_file_path = os.path.join(assets_dir, 'package.json')
    with open(package_json_file_path, 'r', encoding='utf-8') as file:
        package_info: dict = json.loads(file.read())

    package_name: str = package_info['name']
    package_version: str = package_info['version']
    extension_file_path = os.path.join(releases_dir, f'{package_name}-v{package_version}.aseprite-extension')
    with zipfile.ZipFile(extension_file_path, 'w') as file:
        file.write(package_json_file_path, 'package.json')
        file.write(zh_hans_old_file_path, 'zh-hans.ini')
    logger.info('Make Extension')


if __name__ == '__main__':
    main()
