Wesnoth Console Colorizer (WesCoco)
===================================

This is a simple console output colorizer for [The Battle for Wesnoth](https://www.wesnoth.org/), intended primarily as an aid for modders and developers.

WesCoco only requires a base install of Python 3.9 or later.


Why
---

Because I was sick of trying to parse copious amounts of debug output produced via `[wml_message]`. As it turns out, color is a pretty effective way of making indistinct spans of text more readable to human eyes 💜


How
---

Just pipe Wesnoth's console output directly into WesCoco, the Unix Way™:

```
wesnoth --no-log-to-file 2>&1 | python3 wescoco.py
```

(Note that WesCoco's own output stream is stderr. This is not currently configurable.)


Settings
--------

Maybe at some point in the future.

I'm lazy~ 🙃


FAQ
---

### Foreign messages from libraries are not highlighted

Addressing this might be a bit annoying as WesCoco would have to take into account how all the different libraries that Wesnoth uses format their own log output.

With that said, on my end I don't experience this normally, beyond some macOS-specific output showing up every now and then; thus, I don't consider this a priority issue.

### Multi-line messages are not highlighted properly

**Short answer:** This is by design. Sorry 💔

**Full answer:** Since Wesnoth does not use any kind of markers for continued lines, it's impossible for WesCoco to figure out where the message is supposed to end past the first line. The best it can do is assume that if a line does not start with the standard logging information, then it's probably not a "proper" log message, i.e. not produced by the `log.cpp` log facilities.

I considered storing some state and using the presence of previous log messages to determine whether the current line might be a continuation of one such, but immediately ran into a big problem:

```
Battle for Wesnoth v1.18.4+dev arm64
Started on Sun Mar  9 09:45:17 2025

Automatically found a possible data directory at: /Users/USER/Library/Developer/Xcode/DerivedData/The_Battle_for_Wesnoth-ccwewrqgctzmpzgdhkubgdndcxli/Build/Products/Release/The Battle for Wesnoth.app/Contents/Resources
Starting with directory: '/Users/USER/Projects/wesnoth-1.18'
Now have with directory: '/Users/USER/Projects/wesnoth-1.18'
Overriding data directory with '/Users/USER/Projects/wesnoth-1.18'
20250309 09:45:17 error filesystem: Apple developer's userdata migration: Problem! Old (non-containerized) directory /Users/USER/Library/Application Support/Wesnoth_1.18 is not a symlink. Your savegames are scattered around 2 locations.

Data directory:               /Users/USER/Projects/wesnoth-1.18
User configuration directory: /Users/USER/Library/Application Support/Wesnoth_1.18
User data directory:          /Users/USER/Library/Application Support/Wesnoth_1.18
Cache directory:              /Users/USER/Library/Application Support/Wesnoth_1.18/cache


Setting mode to 1496x935
2025-03-09 09:45:18.231 The Battle for Wesnoth[61251:6957786] +[IMKClient subclass]: chose IMKClient_Modern
2025-03-09 09:45:18.231 The Battle for Wesnoth[61251:6957786] +[IMKInputSession subclass]: chose IMKInputSession_Modern
20250309 09:45:18 warning config: add-on 'Sea_of_Silence' has no _info.cfg; cannot read version info
Checking lua scripts... ok
```

Especially during early initialization of the game engine, messages produced via the log facilities can be found mixed in between the early banner messages. In order to tell the latter apart, I'd need to give WesCoco knowledge of what counts as an early banner message and what doesn't... which is bound to change any time a dev decides to change how or where or when these messages are produced.

Since this is all bound to become obsolete information at any point during any dev cycle, I'd rather save myself the hassle and just assume proper log messages will only ever be single lines. My apologies to anyone who was expecting to see WML dumps in the logs be highlighted properly 💔

### I want to change the way log messages are highlighted

I wrote WesCoco in Python so it should be easy for the user to modify it according to their own preferences.

### Why not implement this into the game engine itself?

This is the kind of feature that's bound to be subject to extensive [bikeshedding](https://en.wikipedia.org/wiki/Bikeshedding) the moment a whole group of people get their eyes on it. These days I simply do not have the energy to attempt to engineer a solution that's guaranteed to please a multitude of people who may not even exist, but whose existence will be inevitably postulated by various members of the team in the interest of ensuring they have nominally participated in the development of the feature.

Still, I'd be happy to take a look at their pull request if someone else decided to implement this into the game in my stead. Beware that unlike WesCoco, Wesnoth cannot make assumptions on the nature of the device on the other end of stdout/stderr, so some platform-dependent code may be required to guarantee that console output continues to look good on operating systems or output devices (e.g. files) that do not natively support ANSI escape codes.
