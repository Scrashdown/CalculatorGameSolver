from typing import List

MAX_SCREEN_SYMBOL_NUMBER = 6

class ScreenNumber:
    value: float = 0.0

    def __init__(self, value: float):
        self.value = value

    def __repr__(self) -> str:
        value_str = str(self.value)
        fractional_part = self.value - int(self.value)
        # Remove trailing .0 if the number has no fractional part
        if fractional_part == 0.0:
            return value_str[:-2]
        return value_str

    def length(self) -> int:
        return len(str(self))

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
            self.screen_number = None
            self.display = self.error_message
        else:
            self.screen_number = number
            self.display = str(number)

    def update(self, number: float) -> None:
        self.update(ScreenNumber(number))

    def update(self, string: str) -> None:
        try:
            self.update(float(string))
        except ValueError:
            self.screen_number = None
            self.display = self.error_message
    
    def is_valid(self) -> bool:
        return self.screen_number != None