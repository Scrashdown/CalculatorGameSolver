from abc import ABC, abstractmethod
from typing import List
from screen import Screen, ScreenNumber


class Button(ABC):
    # Must be populated with each action in __init__
    actions = []

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def increment_numbers(self, increment: int) -> None:
        pass

    class Action(ABC):
        def __init__(self, button):
            self.button = button

        @abstractmethod
        def __repr__(self) -> str:
            pass

        @abstractmethod
        def __call__(self, screen: Screen, buttons) -> None:
            pass


class NoNumButton(Button):
    def increment_numbers(self, increment: int) -> None:
        pass


class OneNumButton(Button):
    value: int

    def increment_numbers(self, increment: int) -> None:
        # If the value is negative, it actually is decremented
        self.value += (increment if self.value >= 0 else -increment)


class TwoNumButton(Button):
    value1: int
    value2: int

    def increment_numbers(self, increment: int) -> None:
        self.value1 += (increment if self.value1 >= 0 else -increment)
        self.value2 += (increment if self.value2 >= 0 else -increment)


class AddSubButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"+{self.value}" if self.value > 0 else f"-{-self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return AddSubButton(int(repr))

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            new_value: float = screen.screen_number.value + self.button.value
            screen.update_float(new_value)


class MulButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"x{self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return MulButton(int(repr[1:]))

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            new_value: float = screen.screen_number.value * self.button.value
            screen.update_float(new_value)


class DivButton(OneNumButton):
    def __init__(self, value: int):
        assert value != 0
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"/{self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return DivButton(int(repr[1:]))

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            new_value: float = screen.screen_number.value / self.button.value
            screen.update_float(new_value)


class SwitchSignButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "+/-"

    @staticmethod
    def instantiate(_) -> Button:
        return SwitchSignButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            new_value: float = -screen.screen_number.value
            screen.update_float(new_value)


class PowerButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"x^{self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return PowerButton(int(repr[2:]))

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            new_value: float = screen.screen_number.value ** self.button.value
            screen.update_float(new_value)


# TODO: TwoNum or NoNum?
class ReplaceButton(TwoNumButton):
    def __init__(self, src: str, dst: str):
        self.value1 = src
        self.value2 = dst
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"{self.value1} => {self.value2}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        start, end = repr.split('=>')
        return ReplaceButton(start.strip(), end.strip())

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            # TODO: make sure it follows the game's behaviour
            # For now, use str.replace on the screen's str representation
            # After it replaces one substring, continues on the *modified* result
            screen_repr: str = ScreenNumber.str(screen.screen_number)
            src_repr: str = self.button.value1
            dst_repr: str = self.button.value2

            # Yield error if screen number is not whole
            if not screen.screen_number.value.is_integer():
                screen.set_error()
            else:
                new_screen_repr = screen_repr.replace(src_repr, dst_repr)
                screen.update_str(new_screen_repr)


class ConcButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return ConcButton(int(repr))

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            # TODO: can the concatenated number have a dot or a sign?

            # If the screen number contains a sign or a dot, yield error
            if not screen.screen_number.value.is_integer():
                screen.set_error()
            else:
                # Concatenate number on the right
                new_screen_repr = (ScreenNumber.str(screen.screen_number.value) +
                                   ScreenNumber.str(self.button.value))

                screen.update_str(new_screen_repr)


class MirrorButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "MIRROR"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return MirrorButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            # ERROR if the number is not whole
            # If the number has a minus sign, do not concatenate the sign

            screen_repr = ScreenNumber.str(screen.screen_number.value)
            # Reverse and concatenate
            new_screen_repr = screen_repr + screen_repr[::-1]
            # If the number was negative, a trailing - was added, remove it
            if screen.screen_number.value < 0:
                new_screen_repr = new_screen_repr[:-1]
            # If the number had a dot originally, it will be duplicated
            # thereby creating an invalid float repr. which will be caught
            # by Screen.update()
            screen.update_str(new_screen_repr)


class RightShiftButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "<<"

    @staticmethod
    def instantiate(_) -> Button:
        return RightShiftButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            if not screen.screen_number.value.is_integer():
                screen.set_error()
            else:
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                if screen_repr.startswith('-') and len(screen_repr) < 3:
                    new_screen_repr = '0'
                elif len(screen_repr) < 2:
                    new_screen_repr = '0'
                else:
                    new_screen_repr = screen_repr[:-1]
                screen.update_str(new_screen_repr)


class ReverseButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "Reverse"

    @staticmethod
    def instantiate(_) -> Button:
        return ReverseButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            if not screen.screen_number.value.is_integer():
                # Yield error if the number is not whole
                screen.set_error()
                return
            elif screen.screen_number.value >= 0:
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                # Reverse screen number
                new_screen_repr = screen_repr[::-1]
            else:
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                # Reverse without taking the sign, but keep it
                new_screen_repr = '-' + screen_repr[:0:-1]
            screen.update_str(new_screen_repr)


class SumButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "SUM"

    @staticmethod
    def instantiate(_) -> Button:
        return SumButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            if not screen.screen_number.value.is_integer():
                # Yield error if the number is not whole
                screen.set_error()
            else:
                # Compute sum of digits and keep sign
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                sign = 1 if screen.screen_number.value >= 0 else -1
                digits = screen_repr if sign == 1 else screen_repr[1:]
                digit_sum: int = sum(map(int, digits))
                screen.update_float(float(sign * digit_sum))


class RSLButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "Shift <"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return RSLButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            # TODO: what happens with dot

            if not screen.screen_number.value.is_integer():
                # Yield error if the number is not whole
                screen.set_error()
            else:
                # Keep sign in front
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                sign = 1 if screen.screen_number.value >= 0 else -1
                digits = screen_repr if sign == 1 else screen_repr[1:]
                shifted = ('' if sign == 1 else '-') + digits[1:] + digits[0]
                screen.update_str(shifted)


class RSRButton(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "Shift >"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return RSRButton()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            # TODO: what happens with dot

            if not screen.screen_number.value.is_integer():
                # Yield error if the number is not whole
                screen.set_error()
            else:
                # Keep sign in front
                screen_repr = ScreenNumber.str(screen.screen_number.value)
                sign = 1 if screen.screen_number.value >= 0 else -1
                digits = screen_repr if sign == 1 else screen_repr[1:]
                shifted = ('' if sign == 1 else '-') + digits[-1] + digits[:-1]
                screen.update_str(shifted)


class IncrementButtonsButton(OneNumButton):
    def __init__(self, value: int):
        self.value = value
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return f"[+] {self.value}" if self.value > 0 else f"[- {-self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return IncrementButtonsButton(int(repr[3:]))

    def increment_numbers(self, increment: int) -> None:
        # Do not increment oneself
        pass

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return
            for b in buttons:
                b.increment_numbers(self.button.value)


class MemButton(OneNumButton):
    def __init__(self):
        self.value = None
        self.actions = [self.StoreAction(self), self.RecallAction(self)]

    def __repr__(self) -> str:
        return "MEM - " if self.value is None else f"MEM {self.value}"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return MemButton()

    def increment_numbers(self, increment: int) -> None:
        # TODO: verify this button can be incremented
        if self.value is not None:
            self.value += increment

    class StoreAction(Button.Action):
        def __repr__(self) -> str:
            return "STORE"

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            # Load value into button
            self.button.value = ScreenNumber.str(screen.screen_number.value)

    class RecallAction(Button.Action):
        def __repr__(self) -> str:
            if self.button.value is None:
                # TODO: think more about what happens in this case
                return "RCL -"
            return f"RCL {self.button.value}"

        def __call__(self, screen: Screen, buttons) -> None:
            if self.button.value is None or screen.screen_number is None:
                return
            # TODO: can the concatenated number have a dot or a sign?

            # If the screen number contains a sign or a dot, yield error
            if not screen.screen_number.value.is_integer():
                screen.set_error()
            else:
                # Concatenate number on the right
                new_screen_repr = (ScreenNumber.str(screen.screen_number.value) +
                                   ScreenNumber.str(self.button.value))

                screen.update_str(new_screen_repr)


class Inv10Button(NoNumButton):
    def __init__(self):
        self.actions = [self.Action(self)]

    def __repr__(self) -> str:
        return "Inv10"

    @staticmethod
    def instantiate(repr: str) -> Button:
        return Inv10Button()

    class Action(Button.Action):
        def __repr__(self) -> str:
            return str(self.button)

        def __call__(self, screen: Screen, buttons) -> None:
            if screen.screen_number is None:
                return

            # TODO: what happens with dot?

            screen_repr = ScreenNumber.str(screen.screen_number.value)
            new_screen_repr = ''.join([ (str(10 - int(d)) if d.isdigit() and int(d) > 0 else d) for d in screen_repr ])
            screen.update_str(new_screen_repr)


# Add your new class here too
# TODO: accept floats?
button_regex = {
    AddSubButton: r'[+-][1-9][0-9]*',
    MulButton: r'x-?[1-9][0-9]*', # TODO: Allow x0?
    DivButton: r'/-?[1-9][0-9]*',
    SwitchSignButton: r'\+/-',
    PowerButton: r'x\^[1-9][0-9]*', # TODO: Allow ^0?
    ReplaceButton: r'-?[0-9]+ *=> *-?[0-9]+',
    ConcButton: r'[0-9]+', # TODO: Allow e.g. 01?
    MirrorButton: r'MIRROR',
    SumButton: r'SUM',
    RightShiftButton: r'<<',
    ReverseButton: r'Reverse',
    RSLButton: r'Shift <',
    RSRButton: r'Shift >',
    IncrementButtonsButton: r'\[\+\] [1-9][0-9]*', # TODO: Allow < 0 increment?
    MemButton: r'STORE',
    Inv10Button: r'Inv10'
}
