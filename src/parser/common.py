def parse_int(number_str: str) -> int:
    base = 10

    if number_str.startswith('0x'):
        base = 16

    if number_str.startswith('0b'):
        base = 2

    if number_str.startswith('0o'):
        base = 8

    return int(number_str, base)
