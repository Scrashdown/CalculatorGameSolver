from abc import ABC, abstractmethod
from typing import Set
from screen import Screen, ScreenNumber


class Button(ABC):
    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def press(self, screen: Screen, buttons) -> None:
        pass

    @abstractmethod
    def increment_numbers(self, increment: int) -> None:
        pass


class NoNumButton(Button):
    def increment_numbers(self, increment: int) -> None:
        pass


class OneNumButton(Button):
    value: int

    def increment_numbers(self, increment: int) -> None:
        self.value += increment


class TwoNumButton(Button):
    value1: int
    value2: int

    def increment_numbers(self, increment: int) -> None:
        self.value1 += increment
        self.value2 += increment


class AddSubButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"+{value}" if value > 0 else f"-{-value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        new_value: float = screen.screen_number.value + self.value
        screen.update(new_value)


class MulButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"x{self.value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        new_value: float = screen.screen_number.value * self.value
        screen.update(new_value)


class DivButton(OneNumButton):
    def __init__(self, value: int):
        assert value != 0
        self.value = value

    def __repr__(self) -> str:
        return f"/{self.value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        new_value: float = screen.screen_number.value / self.value
        screen.update(new_value)


class SwitchSignButton(NoNumButton):
    def __repr__(self) -> str:
        return "+/-"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        new_value: float = -screen.screen_number.value
        screen.update(new_value)


class PowerButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"x^{self.value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        new_value: float = screen.screen_number.value ** self.value
        screen.update(new_value)


class ReplaceButton(TwoNumButton):
    def __init__(self, src: int, dst: int):
        self.value1 = src
        self.value2 = dst

    def __repr__(self) -> str:
        return f"{self.value1} -> {self.value2}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        # TODO: make sure it follows the game's behaviour
        # For now, use str.replace on the screen's str representation
        # After it replaces one substring, continues on the *modified* result
        screen_repr: str = str(screen.screen_number)
        src_repr: str = str(self.value1)
        dst_repr: str = str(self.value2)

        new_screen_repr = screen_repr.replace(src_repr, dst_repr)
        screen.update(new_screen_repr)


class ConcButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        # TODO: what if the screen number, or concatenated number contain a dot?
        # TODO: what if the concatenated number contains a sign?
        # Concatenate number on the right
        new_screen_repr = str(screen.screen_number) + str(self.value)
        screen.update(new_screen_repr)


class IncrementButtonsButton(Button):
    value: int = 0

    def __init__(self, value: int):
        self.value = value

    def __repr__(self) -> str:
        return f"[+]{value}" if value > 0 else f"[-]{-value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        for b in buttons:
            b.increment_numbers(self.value)