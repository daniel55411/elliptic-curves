from argparse import ArgumentParser

from src.app import run_on_directory
from src.settings import setup_logging


arg_parse = ArgumentParser()
arg_parse.add_argument('--src', help='Входная директория')
arg_parse.add_argument('--dst', help='Выходная директория')


def main():
    setup_logging()
    options = arg_parse.parse_args()
    run_on_directory(
        src_directory=options.src,
        dst_directory=options.dst,
    )


if __name__ == '__main__':
    main()
