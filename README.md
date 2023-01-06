# Elliptic Curve

Учебный проект реализующий сложение точек на эллептической кривой и
произведение точки на скаляр.

Все операции проводятся на двумя типами полей:
- Конечное поле с характеристикой 2
- Кольцо вычетов по модулю

## Установка
### Из исходников:
```
cd project_path
pip3 install -e '.'
```

### С помощью wheel:
```
cd wheel_dir_path
pip3 install elliptic_curve-0.0.1-py3-none-any.whl
```

NOTE: Версия может отличаться от примера в README

## Как пользоваться:
После установки в консоле станет доступна команда `elliptic-curve`

Для получения справки:
```
elliptic-curve --help
```

Для запуска скрипта:
```
elliptic-curve --src <input_dir> --dst <output_dir>
```

Также можно определить систему счисления для всех выходных файлов с помощью опции `--base`:
```
elliptic-curve --src <input_dir> --dst <output_dir> --base 2
```

Доступны следующие системы счисления: 2, 8, 10. 16

## Формат входного файла

NOTE: формат описывает значения **по-строчно**

### Кольцо вычетов по модулю
```
Z_p
p  # порядок поля
a  # параметр эллиптической кривой
b  # параметр эллиптической кривой
a (x1, y1) (x2, y2)  # сложение двух точек
m <scalar> (x1, y1)  # умножение точки на число
```
### Конечно поле
```
GF(2^m)
p | m: <степень>  # порядок - неприводимый многочлен или степень неприводимого многочлена
a1  # параметр эллиптической кривой
a2  # параметр эллиптической кривой
a3  # параметр эллиптической кривой
a4  # параметр эллиптической кривой
a5  # параметр эллиптической кривой
a (x1, y1) (x2, y2)  # сложение двух точек
m <scalar> (x1, y1)  # умножение точки на число
```
Для конечно поля порядок - неприводимый многочлен, также можно его не указывать,
 а задать лишь степень, тогда скрипт сам возьмет нужный неприводимый многочлен

### Форматы чисел

Все числа могут быть заданы с разной системой счисления. Для указания системы счисления
необходимо указать ее с помощью префикса:
- `0x` - 16-ная
- `0b` - 2-ная
- `0o` - 8-ная
- без префикса - 10-ная

### Примеры
Смотреть в папке examples

## Формат выходного файла
Выходной файл будет содержать результаты на строки-задания (например, `a (1, 2) (2, 1)`)
из входного файла

Для сложения выходная строка будет: `(x1, y1) + (x2, y2) = (x3, y3)`
Для умножения выходная строка будет: `<scalar> * (x2, y2) = (x3, y3)`

NOTE: система счисления выходного файла может быть определена с помошью опции `--base`.
Если опция не будет указана, то система счисления подберется на основе входного файла по
принципу наиболее часто встречаемой системы счисления входа

# Запуск тестов

```
pip install pytest  # установка системы тестирования
pytest ./tests  # запуск
```