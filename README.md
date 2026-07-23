# Mario Bros

A small recreation of the classic 1983 arcade game **Mario Bros** (the conveyor-belt one, not the platformer), built in Python with [Pyxel](https://github.com/kitao/pyxel). Made as a university project for an Object-Oriented Programming course.

Mario and Luigi work opposite sides of a stack of conveyor belts, pushing packages down toward a delivery truck while trying not to let anything fall off the edge — and trying not to get caught by Bowser, who shows up now and then to mess with the belts.

## About this project

This was built as a coursework assignment, with the goal of applying OOP concepts (inheritance, encapsulation, composition) to something a bit more fun than a typical homework exercise. A full write-up of the design decisions, class structure, and development process is included in the repo as a PDF report (`Report_DiegoMadroñal_SoniaAndreea.pdf`), for anyone who wants the deeper explanation behind the code.

## Gameplay

- Packages spawn on the top belt and travel down through the stack of belts below it.
- Mario and Luigi each control one side of the belts and have to keep the packages moving so they reach the truck instead of piling up or falling off.
- Bowser occasionally appears and freezes the action for a bit — timing matters.
- Every package that's lost counts as a fail. Get 3 fails and it's game over.
- Successfully delivered packages add to your score.

## Controls

At launch you'll get a short menu to pick the game speed:

| Key | Speed |
|-----|-------|
| `1` | Slow |
| `2` | Normal |
| `3` | Fast |

Once you're in the game:

| Player | Move Up | Move Down |
|--------|---------|-----------|
| Mario (right side) | `↑` | `↓` |
| Luigi (left side) | `W` | `S` |

Other keys:

- `P` — pause / unpause
- `R` — restart (only works after a game over)

## Getting started

You'll need Python 3 and Pyxel installed.

```bash
pip install pyxel
```

Clone the repo and run the game from the project root:

```bash
git clone https://github.com/soniaspn/mariobros.git
cd mariobros
python main.py
```

Make sure the `assets/sprites.pyxres` file stays in place relative to `main.py` — that's where the sprite/tile data is loaded from.

## Project structure

```
mariobros/
├── main.py                 # Game loop, window setup, menu, and rendering
├── character.py             # Mario / Luigi player logic
├── conveyorbelt.py           # Base conveyor belt behavior
├── SpecialConveyorBelt.py    # Belt variant with extra movement range
├── Bowser.py                  # The "boss" character that pauses gameplay
├── PointSystem.py             # Score and fail tracking
├── truck.py                    # Delivery truck logic
└── Report_DiegoMadroñal_SoniaAndreea.pdf   # Written report for the course
```

Under the hood, the game is split into a handful of cooperating classes rather than one big script: belts know how to move and hold packages, characters know how to interact with belts, Bowser knows how to interrupt everything, and `PointSystem`/`Truck` just track state. `main.py` ties it all together in a fairly standard Pyxel `update()` / `draw()` loop.

## Authors

Diego Madroñal and Sonia Andreea — built as part of a university OOP course project.

## Notes

This was written for a class assignment rather than as a polished, production-ready game, so don't expect every edge case to be handled gracefully. It's meant to demonstrate class design more than to be a bulletproof game engine. Bug reports and suggestions are still welcome, though.
