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

    def increment_numbers(self, increment: int) -> None:
        pass


class AddButton(Button):
    value: int = 0

    def __init__(self, value: int):
        assert value != 0
        self.value = value

    def __repr__(self) -> str:
        return f"+{value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        # TODO
        pass

    def increment_numbers(self, increment: int) -> None:
        assert increment > 0
        self.value += increment


class SwitchSignButton(Button):
    def __repr__(self) -> str:
        return "+/-"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        # TODO
        pass


class IncrementButtonsButton(Button):
    value: int = 0

    def __init__(self, value: int):
        assert value > 0
        self.value = value

    def __repr__(self) -> str:
        return f"[+]{value}"

    def press(self, screen: Screen, buttons: Set[Button]) -> None:
        for b in buttons:
            b.increment_numbers(self.value)