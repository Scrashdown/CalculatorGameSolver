from typing import List

MAX_SCREEN_SYMBOL_NUMBER = 6


class ScreenNumber:
    value: float = 0.0

    @staticmethod
    def str(value: float) -> str:
        value_str = str(value)
        # Remove trailing .0 if the number has no fractional part
        if value_str.endswith('.0'):
            value_str = value_str[:-2]
        # Remove front sign for -0 special case
        if value_str == '-0':
            value_str = value_str[1:]
        return value_str

    def __init__(self, value: float):
        self.value = float(value)

    def __repr__(self) -> str:
        return ScreenNumber.str(self.value)

    def length(self) -> int:
        return len(ScreenNumber.str(self))


class Screen:
    screen_number: ScreenNumber = None
    display: str = ""

    max_symbol_number: int = MAX_SCREEN_SYMBOL_NUMBER
    error_message: str = "ERROR"

    def __init__(self, number: ScreenNumber):
        # Set screen with number
        self.update(number)

    def update(self, number: ScreenNumber) -> None:
        # Check that the number fits
        if number.length() > self.max_symbol_number:
            self.set_error()
        else:
            self.screen_number = number
            self.display = ScreenNumber.str(number)

    def update_float(self, number: float) -> None:
        self.update(ScreenNumber(number))

    def update_str(self, string: str) -> None:
        try:
            self.update_float(float(string))
        except ValueError:
            self.set_error()

    def set_error(self) -> None:
        self.screen_number = None
        self.display = self.error_message

    def is_valid(self) -> bool:
        return self.screen_number != None
