# Live Wire

A mobile circuit puzzle game. Tap wires to rotate them, flip switches, and route
power from batteries to bulbs without tripping alarms. Built to be easy to learn,
satisfying to play, and fully offline.

## Current state
- `livewire.html` is a working single-file prototype (HTML, CSS, canvas, Web Audio).
- Boards 1, 2, 3, 15, 25, 35, 50, 70, 90 and 110 are hand-made teaching boards.
  Every other board is generated from its level number by a seeded generator,
  so the same level always produces the same board, with no server needed.
- Difficulty ramps slowly: tiny 4x4 boards early, full 9x11 boards from about
  level 250, and very hard boards by 200 to 500.
- Pieces: wires (rotate), bolted wires (fixed), switches, bridges, alarms,
  batteries (red, blue, green), bulbs (need an exact colour mix), swappers
  (change current colour).
- Sound is synthesised with Web Audio. Haptics go through one `haptic.go()` function.

## Goal
Turn the prototype into a real iOS and Android app using Capacitor.

## Rules for working on this project
- Keep the game fully playable offline.
- Keep level generation deterministic: never change the generator in a way that
  changes existing levels unless I ask, because players' saved progress depends on it.
- Replace `navigator.vibrate` with `@capacitor/haptics` (light impact for gear
  ticks, medium for connections, success notification for wins).
- Save progress with `@capacitor/preferences` instead of localStorage.
- Make one change at a time, explain what changed in plain words, and commit to git
  after each working step.
- I am new to app development: tell me exactly what to install and click when
  something has to happen outside the code.
