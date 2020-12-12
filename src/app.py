import glob
import logging
import os.path
from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor

from src.output import FormattersRegistry
from src.output import IntFormatter
from src.output import PointFormatter
from src.output import PolynomialFormatter
from src.output import TaskConfigFormatter
from src.output import TaskResultFormatter
from src.parser.input_stream import INT_BASE_METRIC
from src.parser.input_stream import Parser


logger = logging.getLogger(__name__)

parser = Parser()
registry = FormattersRegistry()
int_formatter = IntFormatter()
polynomial_formatter = PolynomialFormatter(int_formatter)
point_formatter = PointFormatter(registry)
task_config_formatter = TaskConfigFormatter(
    point_formatter=point_formatter,
    int_formatter=int_formatter,
)
task_result_config = TaskResultFormatter(
    task_config_formatter=task_config_formatter,
    point_formatter=point_formatter,
)

registry.register(int_formatter)
registry.register(polynomial_formatter)
registry.register(point_formatter)
registry.register(task_config_formatter)
registry.register(task_result_config)


def _get_most_common_base():
    return INT_BASE_METRIC.most_common()[0][0]


def _check_error(future: Future):
    if future.exception() is not None:
        logger.error('Ошибка: %s', str(future.exception()).strip())


def run(filename: str, dst_directory: str):
    input_f = open(filename, 'r')
    filename = os.path.basename(filename)

    config = parser.parse(input_lines=iter(input_f))
    logger.info('Считал конфигурацию у файла %s. Начинаю построение таск раннера...', filename)
    task_runner = config.build_runner()
    formatter_context = {'base': _get_most_common_base()}
    logger.info(
        'В файле %s числа будут переведены в основание %d',
        filename, formatter_context['base'],
    )

    with open(os.path.join(dst_directory, filename), 'w') as output_f:
        logger.info('Таск раннер начал работу для файла %s', filename)

        for task_result in task_runner.run(config.task_configs):
            task_result_str = task_result_config.format(task_result, formatter_context)
            output_f.write(task_result_str + os.linesep)

    logger.info('Таск раннер завершил все подсчеты. Все результаты записаны в файл %s', filename)


def run_on_directory(src_directory: str, dst_directory: str):
    logger.info(
        'Запустилась обработка директории %s',
        os.path.abspath(src_directory),
    )

    with ThreadPoolExecutor() as executor:
        pattern = os.path.join(src_directory, '*.txt')

        for filename in glob.iglob(pattern):
            logger.info('Начал подсчет для файла %s', filename)
            future = executor.submit(run, filename, dst_directory)
            future.add_done_callback(_check_error)

    logger.info('Завершил работу со всеми файлами')
    logger.info(
        'Для просмотра результатов перейдите в каталог %s',
        os.path.abspath(dst_directory),
    )
