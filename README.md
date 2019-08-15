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
* Check levels 84, 85, many solutions

## Buttons

Note: all numbers in buttons are whole numbers

* `+X` / `-X` / `xX` / `/X` (dark gray) Add / subtract / multiply / divide by X
* `+/-` (orange) Switch number sign
* `x^P` (orange) Raise number to power P (**TODO:** what happens with dot and sign?)
* `X -> Y` (orange) Replace all occurrences of sequence X to sequence Y, if the screen number is not whole, this yields error (**TODO:** what if these sequences can be overlapping?, can any sequence be negative? E.g. 11 in 111)
* `X` (purple) Concatenate **X** on the right, if the number has a dot, yields ERROR. (**TODO:** can X have minus sign or a dot?)
* `MIRROR` (orange) Concatenate on the right a mirrored version of the current numbers. If there is a minus sign, -x becomes -xx. If there is a dot, we get ERROR.
* `SUM` (orange) Sum of all numbers on the screen. If the number is not whole, yields error. If the number is negative, yields - the sum of the digits (-12 -> -3).
* `<<` (orange) Right decimal shift (if only one number remaining, positive or negative, becomes 0. If the number is negative, yields error.)
* `Reverse` (orange) Reverse all characters on the screen. If the number is not whole, yields error. If the number is negative, reverse is executed on the absolute value and the sign remains (-xy -> -yx)
* `Shift <` / `Shift >` (orange) Decimal rollover left/right shift (SLL/SRL), CAREFUL training zeroes on the right are eliminated by the shift. If the number is negative, shift is performed only on the digits and sign is kept. (**TODO:** what happens with dot?) (10 -> 1, not 01)
* `[+] X` (orange) Add **X** to all "number buttons" (but not itself). **WARNING:** incrementing a negative number actually **decrements** it. (**TODO:** does it also work with 'substitution' button?, **TODO:** can we have negative increments?)
* `STORE` / `RCL X` (deep purple) Can be pressed in two ways. LONG-PRESS stores the screen value in the button, SHORT-PRESS concatenates the stored number (**if any**) on the screen (**TODO:** what happens with sign and dot?, Is the stored number incremented by the increment button?).

### TODO

Add a system of "actions" per button. Each button provides a list of all the actions it supports (such as short press, long press, etc.). The solver then uses it to find all possible combinations of actions, and executes them. A way to describe and execute an action is therefore also needed. Maybe replace the Button.press() method by a call to Action()? This is useful to implement buttons who have different press modes.
