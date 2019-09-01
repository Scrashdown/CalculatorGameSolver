# CalculatorGameSolver
Solver for _Calculator: The Game_, just for fun.

## Usage

_Coming when I have time..._ meanwhile please use the `test.py` file and try to understand the code.

### Level parameters
TODO

### Button patterns
TODO

## Game description and rules (partly reverse-engineered / guessed)
The game is made of a multitude of levels. In each level you have a number
on the screen of a calculator, some buttons, a goal number to be reached,
and the maximum allowed number of moves required for passing the level.

### Screen
Can contain any positive, negative decimal number, with or without decimal point
as long as its exact representation fits on the screen. Can also display `ERROR`
if it can't display a number.

#### TODO:
* Check if this is true
* Check the maximum numbers of symbols (appears to be 6, check thoroughly)
* Check if the minus sign and decimal point are counted in the number of displayed symbols

### Maximum number of moves
Whole number > 0

### Goal
Any whole number. _All levels encountered had a whole number goal._

### Buttons
<!-- Thanks https://www.tablesgenerator.com/markdown_tables# for the pretty awesome Markdown table generator. -->

| Button pattern(s)         | Colour        | Description                                                                                                                                                                                                                  | TODO / unclear behaviour / notes                                                                                                                               |
|---------------------------|---------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `+X` / `-X` / `xX` / `/X` | (dark gray)   | Add / subtract / multiply / divide by `X`.                                                                                                                                                                                   |                                                                                                                                                                |
| `+/-`                     | (orange)      | Switch number sign.                                                                                                                                                                                                          |                                                                                                                                                                |
| `x^P`                     | (orange)      | Raise number to power `P`.                                                                                                                                                                                                   | What happens with dot and sign?                                                                                                                                |
| `X -> Y`                  | (orange)      | Replace all occurrences of sequence `X` to sequence `Y`. Trailing zeroes (i.e `00`) can be part of `X` or `Y`. If the screen number is not an integer, yields ERROR.                                                         | Can `X` and `Y` overlap? Can they be negative?                                                                                                                 |
| `X`                       | (purple)      | Concatenate `X` on the right, if the number is not whole, yields ERROR.                                                                                                                                                      | Can `X` be negative or not an integer?                                                                                                                         |
| `MIRROR`                  | (orange)      | Concatenate on the right a mirrored version of the current number. `-X` -> `-XX`. A float yields ERROR.                                                                                                                      |                                                                                                                                                                |
| `SUM`                     | (orange)      | Replaces the number of the screen with the sum of its digits. If the number is not whole, yields ERROR. If negative, `SUM(-X) = -SUM(X)`.                                                                                    |                                                                                                                                                                |
| `<<`                      | (orange)      | Decimal shift to the right. `XY` -> `X`, `X` -> `0`. Negative number yields ERROR.                                                                                                                                           |                                                                                                                                                                |
| `Reverse`                 | (orange)      | Reverse digits of the number on the screen. Float numbers yield ERROR. If the number is negative `REV(-XY) = -REV(XY) = -YX`.                                                                                                |                                                                                                                                                                |
| `Shift <` / `Shift >`     | (orange)      | Decimal left/right circular shift. Trailing zeroes are eliminated. If the number is negative, `SHIFT(-X) = -SHIFT(X)`.                                                                                                       | What happens with float numbers? Verify statement about trailing zeroes.                                                                                       |
| `[+] X`                   | (orange)      | Increment all numbers in buttons by `X` (except this one). Negative numbers are decremented (i.e. `-1` -> `-1-X`).                                                                                                           | What happens with buttons containing floats? Does the substitution button also get incremented? Can `X` be negative?                                           |
| `STORE` (`RCL X`)         | (deep purple) | Two modes. _Long press_ stores the screen value in the button. _Short press_ concatenates the stored number `X` on the screen, on the right, _if any_. Can store a negative or float number. Recalling a float yields ERROR. | Is `X` incremented by the increment button? Weird behaviour with a negative stored number, moves count goes < 0, changes by itself, inconsistent, maybe a bug? |
| `Inv10`                   | (orange)      | For each digit `d` in the screen number, replaces it with `10 - d`. `0` -> `0`. `-` -> `-`.                                                                                                                                  | What happens with float numbers?                                                                                                                               |

### Portal

The screen may contain a portal. It consists of 2 positions on the screen. One is the entrance, and the other is the exit. _"Numbers go in a portal, then come out and added to the other end."_ (whatever that means). Operates in a loop until there is no digit left to suck. The portal's entrance is always comes first, starting from the left of the number.

If the portal acts on a number that is not whole, the game either freezes or gives seemingly non-sensical output -> `ERROR` in that case for lack of a better option.

## Other TODOs
* Check levels 84, 85, 153, 155, 173, 174, 177, 178, 188, 192, 196, 198, because they appear to have many solutions
* Load levels from a text file or stdin, output results to a file or stdout
* Better terminal interface and feedback (help, etc.)
* Optimize solver to reduce the number of tested solutions (for example, impossible, or 'dummy' solutions that are not feasible because they contain a prefix which is already a solution). Could also use some sort of a tree to avoid pressing buttons that change nothing, at a given time 🤔
* Maybe switch to an all-int representation. This would be cleaner, and so far I haven't seen any solution involving floats (check that thoroughly!)
