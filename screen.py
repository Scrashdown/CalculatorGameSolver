from typing import List, Tuple

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


class Portal:
    # Start and end of the portal, in indexes starting from the RIGHT of the screen
    exit: int
    entrance: int
    screen_width: int

    def __init__(self, entrance: int, exit: int, screen_width: int):
        assert exit > 0 and entrance > exit
        assert screen_width > 0 and exit < screen_width and entrance < screen_width
        self.exit = exit
        self.entrance = entrance
        self.screen_width = screen_width

    def transform(self, number: ScreenNumber) -> ScreenNumber:
        number_len = number.length()
        # If no digit enters the portal, do nothing
        if self.entrance > number_len:
            return number

        # If the number is to be transformed but not whole,
        # set error
        if not number.value.is_integer():
            return None

        # Remove digit, and add it to the part between the entrance (inclusive) and the exit (inclusive)
        # TODO: how to manage sign?
        screen_repr: str = ScreenNumber.str(number)

        # Workaround for problem with negative slicing and 0 end of slice
        start_rest = -self.exit + 1

        leading = screen_repr[:-self.entrance]
        sucked = screen_repr[-self.entrance]
        receiver = screen_repr[-self.entrance+1:start_rest] if start_rest < 0 else screen_repr[-self.entrance+1:]
        rest = screen_repr[start_rest:] if start_rest < 0 else ''

        new_number_str = leading + ScreenNumber.str(int(sucked) + float(receiver)) + rest
        new_number = ScreenNumber(float(new_number_str))

        # Call recursively
        return self.transform(new_number)


class Screen:
    screen_number: ScreenNumber = None
    display: str = ""
    portal: Portal = None

    max_symbol_number: int = MAX_SCREEN_SYMBOL_NUMBER
    error_message: str = "ERROR"

    def __init__(self, number: ScreenNumber, portal: Tuple[int] = None):
        # Set screen with number
        self.update(number)
        # Create portal if both arguments are valid
        if portal is not None:
            self.portal = Portal(portal[0], portal[1], self.max_symbol_number)

    def update(self, number: ScreenNumber) -> None:
        # Check that the number fits
        if number.length() > self.max_symbol_number:
            self.set_error()
            return

        # Use portal if there is one
        if self.portal is None:
            self.screen_number = number
        else:
            self.screen_number = self.portal.transform(number)
            # Set ERROR if the transformation fails
            if self.screen_number is None:
                self.set_error()
                return
        self.display = ScreenNumber.str(self.screen_number)

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
