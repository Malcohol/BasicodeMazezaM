# BasicodeMazezaM

A port of the game [MazezaM](https://sites.google.com/site/malcolmsprojects/mazezam-home-page) to [BASICODE](https://en.wikipedia.org/wiki/BASICODE).

It is optimized for size with the intention of supporting the widest possible set of BASICODE platforms.
In particular, it loads on the unexpanded [VIC-20](https://en.wikipedia.org/wiki/Commodore_VIC-20), which has less than 2.4K available for code when the BASICODE loader and routines are present.

The makefile creates the program listed below. The easiest way to use it is to paste it into Rob Hagermans' browser-based [basicode-interpreter](https://robhagemans.github.io/basicode/#listing).

```
LISTING
```

The makefile also generates an audio file called `MazezaM.wav`. This can be loaded on many old platforms using a BASICODE loader (or "Bascoder"). I have tested the program on several emulated platforms, including Vic20[*](https://sourceforge.net/p/vice-emu/patches/438), C64 and ZX Spectrum. 

