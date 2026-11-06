# Live Wire

A mobile circuit puzzle game. Tap wires to rotate them, flip switches, and route
power from batteries to bulbs without tripping alarms. Built to be easy to learn,
satisfying to play, and fully offline.

## Current state
- `index.html` is the whole game in one file (HTML, CSS, canvas, Web Audio). No build step.
- Game logic lives between `/*CORE-START*/` and `/*CORE-END*/` and can run in Node for tests.
- Sectors are 10 boards. Board 5 is a mini-boss (one extra bulb), board 10 is a boss (extra bulb,
  extra trap, bigger board; the generator keeps the hardest of a few candidates).
- Levels 1-100 are the learning phase: boards stay modest (4x4 up to 7x10) and each sector adds one
  new part. Difficulty comes from the parts and where they sit, not from size. From 101 on, once every
  part is known, boards grow to 9x11 (around level 200).
- New parts by sector: 11 alarms and bolted pieces, 21 switches, 31 blue power, 41 purple mixing,
  51 bridges, 61 diodes, 71 green power, 81 relays, 91 swappers, 101 everything at once.
  Hand-made teaching boards open sectors 1, 11, 21, 31, 41, 51 and 101; 61, 71, 81 and 91 open with
  generated boards that are forced to include the new part.
- Difficulty is measured in real moves (`solutionPar`: pieces the solution uses, decoys excluded).
  Each board must land in a band around its target, rising through the sector.
- Alarms are placed beside the real path, where a careless turn feeds them. Boards start with no alarm
  ringing where possible (guard switches start open if they'd ring from the start).
- Pieces: wires (rotate), bolted wires (fixed), switches, bridges, alarms (buzzers), batteries
  (red, blue, green), bulbs (exact colour mix), swappers (change colour), diodes (one-way wires:
  `t.dio` is the output end; they rotate like wires and must point the way current flows), relays
  (switches with `t.relay=k` that close by themselves when coil `k` has power; not tappable) and coils
  (`t.t='coil'`, drawn as a converter box: a terminal on another circuit; any colour powers it). `compute` re-runs the flow until relays settle.
- Swappers take one colour at a time: if mixed current reaches a side, that side is blocked (`t.blk`, shown as a red
  stop mark) and `compute` re-runs the flow. From level 91 on (`distinct` in `genParams`, also every daily), each
  circuit gets its own bulb colour, so merging circuits never solves a board. Levels 1-90 are unaffected by both rules.
  Batteries, bulbs, alarms and coils connect only through their pins.
- Daily challenge: same board for everyone each UTC day, five challenge types. Steady Hands
  boards are verified with a solver so they can be beaten without a mistake.
- Par counts only the pieces the real solution uses (decoy wires excluded).
- Extras: undo, hints, tutorial pointer, ranks, streak freezes, board skins, sector colours,
  colour symbols, power-cut screen transitions, flow and surge animations.
- Timed mode is optional (`meta.timed`), off by default. Gold time = `round(par*1.4+4)` seconds; hints void gold.
  Best times in `meta.best`, gold boards in `meta.gold`. Normal play has no time pressure: keep it that way.
- Daily challenges are dense rather than big, tall and narrow (6-7 wide) so pieces stay large on phones, keep the hardest of 3 qualifying candidates, and can be shared
  as a text result card. Changing `CHALLENGES` or `buildDaily` changes the shared daily for everyone.
- Collection: world themes (`THEMES`: Swamp, Tide Pool, Firefly Meadow, First Snow, Blossom, Starlight) with their own
  palette, bulb charms (`charmUnder`/`charmOver`), empty-socket decorations (`decor`) and drifting ambience (`ambience`), string lights around the frame (`frameLights`),
  unlocked by boards, stars, streaks, bosses, chests and gold medals; plus board colours (`SKINS`) for the Circuit theme.
- Timed mode: bronze/silver/gold medals per board (`tiersFor`), a race bar with your best as a ghost marker; gold earns ⚡.
- Menu: daily challenge card with NEW badge and countdown; NEW tags on boards and pieces that introduce a part.
- Rewards: star chests every 30 stars, perfect streak (hint every 5), combos, confetti, pause menu, ambient music.
- Full-screen overlays (win, sheets, confetti, transitions) are `position:fixed` so they cover iPads and desktops.
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
- Portrait only, on phones and tablets. The web version covers the game with a "turn your device
  upright" screen when a touch device is held sideways, and pauses timed challenges meanwhile.
  In the native app, lock it properly:
  - iOS `Info.plist`: `UISupportedInterfaceOrientations` = portrait only;
    `UISupportedInterfaceOrientations~ipad` = portrait and portrait upside down; and
    `UIRequiresFullScreen` = YES (iPad apps must otherwise support every orientation).
  - Android `AndroidManifest.xml`: `android:screenOrientation="portrait"` on the main activity, and
    `android:appCategory="game"` on the application. Android 16 ignores orientation locks on tablets
    (smallest width 600dp or more) unless the app is marked as a game.
- iPad scaling: the interface scales with a `--s` factor (1 on phones, up to 1.6 on large iPads) and
  the board grows to match. Keep new UI inside the scaled containers.
- Replace `navigator.vibrate` with `@capacitor/haptics` (light impact for gear ticks,
  medium for connections, success notification for wins).
- Save progress with `@capacitor/preferences` instead of localStorage.
- Account saves: on claude.ai, progress syncs to the player's private `data/users/<id>/save` doc (`cloud` object).
  Saves are always merged (`mergeSave`: best stars, best times, daily results, latest streak), never overwritten.
  Backup codes (`LW1-` + base64 JSON) let players copy and restore progress anywhere. In the native app, replace
  the claude.ai sync with Game Center / Google Play Games saved games or a small backend, reusing `mergeSave`.
- Replace the claude.ai leaderboard with Game Center / Google Play Games or a small backend.
- Make one change at a time, explain what changed in plain words, and commit to git
  after each working step.
- I am new to app development: tell me exactly what to install and click when
  something has to happen outside the code.
