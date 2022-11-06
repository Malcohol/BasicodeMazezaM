# BasicodeMazezaM

A port of the game [MazezaM](https://sites.google.com/site/malcolmsprojects/mazezam-home-page) to [BASICODE](https://en.wikipedia.org/wiki/BASICODE).

It is not intended to be a particularly playable version and it's certainly not readable.
Instead, it is optimized for size with the intention of supporting the widest possible set of BASICODE platforms.
The unexpanded [VIC-20](https://en.wikipedia.org/wiki/Commodore_VIC-20) has just 3.5K of RAM available to BASIC and the BASICODE loader uses up some of that space. I think that it must therefore be the most constrained platform which supports BASICODE. I've tried to implement a version of MazezaM that would load there.

The makefile creates the program listed below. The easiest way to use it is to paste it into Rob Hagermans' browser-based [basicode-interpreter](https://robhagemans.github.io/basicode/#listing).

```
