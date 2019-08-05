# CalculatorGameSolver
Solver for Calculator: the Game

## Game description
The game is made of a multitude of levels. In each level you have a number
on the screen of a calculator, some buttons, a goal number to be reached,
and the maximum allowed number of moves required for passing the level.

## Screen
Can contain any positive, negative decimal number, with or without decimal point
as long as its exact representation fits on the screen. Can also display `ERROR`
if it can't display a number.

**TODO:**
* Check if this is true
* Check the maximum numbers of symbols (appears to be 6, check thoroughly)
* Check if the minus sign and decimal point are counted in the number of displayed symbols

## Maximum number of moves
Whole number > 0

## Goal
Any number

**TODO:**
* Should the goal always be a whole number?

## Buttons

Note: all numbers in buttons are whole numbers

* `+X` / `-X` / `xX` / `/X` (dark gray) Add / subtract / multiply / divide by X
* `+/-` (orange) Switch number sign
* `x^P` (orange) Raise number to power P (**TODO:** what happens with dot and sign?)
* `X -> Y` (orange) Replace all occurrences of sequence X to sequence Y (**TODO:** what if these sequences can be overlapping?, can any sequence be negative? E.g. 11 in 111)
* `X` (purple) Concatenate **X** on the right (**TODO:** what happens with dots and signs?)
* `MIRROR` (orange) Concatenate on the right a mirrored version of the current numbers. If there is a minus sign, -x becomes -xx. If there is a dot, we get ERROR.
* `SUM` (orange) Sum of all numbers on the screen (**TODO:** what happens with minus sign?)
* `<<` (orange) Right decimal shift (if only one number remaining, becomes 0, **TODO:** what happens with dot?, what happens with minus sign?)
* `Reverse` (orange) Reverse all characters on the screen (**TODO:** how does it work with dot?, what happens with minus sign?)
* `Shift >` / `< Shift` (orange) Decimal rollover left/right shift (SLL/SRL), CAREFUL training zeroes on the right are eliminated by the shift (**TODO:** what happens with sign?) (10 -> 1, not 01)
* `[+] X` (orange) Add **X** to all "number buttons" (but not itself) (**TODO:** does it also work with 'substitution' button?, **TODO:** can we have negative increments?)
