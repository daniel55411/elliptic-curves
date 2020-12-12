from argparse import ArgumentParser

from src.app import run_on_directory
from src.settings import setup_logging


arg_parse = ArgumentParser(
    description=(
        'Скрипт для сложения точек эллиптической кривой. '
        'Подробно о формате входных файлов смотреть в документацию. '
        'Документация находится в репозитории проекта в README.md'
    ),
)
arg_parse.add_argument('--src', help='Входная директория')
arg_parse.add_argument('--dst', help='Выходная директория')
arg_parse.add_argument(
    '--base',
    help='Основание системы счисления выходных файлов. Доступные: 2, 8, 10, 16',
    type=int,
    default=None,
)


def main():
    setup_logging()
    options = arg_parse.parse_args()
    run_on_directory(
        src_directory=options.src,
        dst_directory=options.dst,
        base=options.base,
    )


if __name__ == '__main__':
    main()
