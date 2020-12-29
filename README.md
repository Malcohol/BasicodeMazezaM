# BasicodeMazezaM

A port of [MazezaM](https://sites.google.com/site/malcolmsprojects/mazezam-home-page) to [BASICODE](https://en.wikipedia.org/wiki/BASICODE).

It is optimized for size with the intention of supporting the widest possible set of BASICODE platforms.
I believe the unexpanded [VIC-20](https://en.wikipedia.org/wiki/Commodore_VIC-20) is the most memory constrained platform which has a BASICODE loader, so I've tried to implement a version that should work there.

The makefile creates a file called "MazezaM.bas". The easiest way to use this is to paste it into Rob Hagermans' browser-based [basicode-interpreter](https://robhagemans.github.io/basicode/#listing).