class ParserError(Exception):
    def __init__(self, number: int, reason: str):
        super().__init__(f'Ошибка в строке: {number}, причина: "{reason}"')
