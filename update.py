import logging
import os

from aseprite_ini import Aseini

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('update')

project_root_dir = os.path.dirname(__file__)
assets_dir = os.path.join(project_root_dir, 'assets')


def main():
    en_file_path = os.path.join(assets_dir, 'en.ini')
    strings_en = Aseini.pull_strings('main')
    strings_en.save(en_file_path)
    logger.info("Update strings: 'en.ini'")

    zh_hans_file_path = os.path.join(assets_dir, 'zh-hans.ini')
    strings_zh_hans = Aseini.load(zh_hans_file_path)
    strings_zh_hans.patch(Aseini.pull_strings_by_url('https://hosted.weblate.org/download/aseprite/aseprite/zh_Hans/'))
    strings_zh_hans.save(zh_hans_file_path, strings_en)
    logger.info("Update strings: 'zh-hans.ini'")

    translated, total = strings_zh_hans.coverage(strings_en)
    progress = translated / total
    finished_emoji = '🚩' if progress == 1 else '🚧'
    print(f'progress: {translated} / {total} ({progress:.2%} {finished_emoji})')


if __name__ == '__main__':
    main()
