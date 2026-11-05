# Live Wire

A mobile circuit puzzle game. Tap wires to rotate them, flip switches, and route
power from batteries to bulbs without tripping alarms. Built to be easy to learn,
satisfying to play, and fully offline.

## Current state
- `index.html` is the whole game in one file (HTML, CSS, canvas, Web Audio). No build step.
- Game logic lives between `/*CORE-START*/` and `/*CORE-END*/` and can run in Node for tests.
- Boards 1, 2, 3, 15, 25, 35, 50, 70, 90 and 110 are hand-made teaching boards. Every other
  board is generated from its level number by a seeded generator.
- Difficulty: tiny 4x4 boards early, full 9x11 boards from about level 110, hardest from
  200 to 500. Each sector of 10 uses sawtooth pacing and ends with a boss board.
- Pieces: wires (rotate), bolted wires (fixed), switches, bridges, alarms (buzzers),
  batteries (red, blue, green), bulbs (need an exact colour mix), swappers (change colour).
  Batteries, bulbs and alarms connect only through their pins.
- Daily challenge: same board for everyone each UTC day, five challenge types. Steady Hands
  boards are verified with a solver so they can be beaten without a mistake.
- Par counts only the pieces the real solution uses (decoy wires excluded).
- Extras: undo, hints, tutorial pointer, ranks, streak freezes, board skins, sector colours,
  colour symbols, power-cut screen transitions, flow and surge animations.
- Sound is synthesised with Web Audio. Haptics go through one `haptic.go()` function.
- The leaderboard uses the claude.ai artifact database (`window.claude`) and switches itself
  off anywhere else.

## Goal
Turn the prototype into a real iOS and Android app using Capacitor.

## Rules for working on this project
- Keep the game fully playable offline.
- Keep level generation deterministic: never change the generator, `compute`, `scramble` or
  `assignPins` in a way that changes existing levels unless I ask, because players' saved
  progress and the shared daily challenge depend on it. Before and after any change to the
  core, fingerprint all 500 levels and confirm they are identical.
- After any core change, check that all 500 levels are solvable and a year of daily
  challenges is beatable under its rules.
- Replace `navigator.vibrate` with `@capacitor/haptics` (light impact for gear ticks,
  medium for connections, success notification for wins).
- Save progress with `@capacitor/preferences` instead of localStorage.
- Replace the claude.ai leaderboard with Game Center / Google Play Games or a small backend.
- Make one change at a time, explain what changed in plain words, and commit to git
  after each working step.
- I am new to app development: tell me exactly what to install and click when
  something has to happen outside the code.
