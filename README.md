# BasicodeMazezaM

A port of the game [MazezaM](https://sites.google.com/site/malcolmsprojects/mazezam-home-page) to [BASICODE](https://en.wikipedia.org/wiki/BASICODE).

It is not intended to be a particularly playable version and it's certainly not readable.
Instead, it is optimized for size with the intention of supporting the widest possible set of BASICODE platforms.
The unexpanded [VIC-20](https://en.wikipedia.org/wiki/Commodore_VIC-20) has just 3.5K of RAM available to BASIC and the BASICODE loader uses up some of that space. I think that it must therefore be the most constrained platform which supports BASICODE. I've tried to implement a version of MazezaM that would load there.

The makefile creates the program listed below. The easiest way to use it is to paste it into Rob Hagermans' browser-based [basicode-interpreter](https://robhagemans.github.io/basicode/#listing).

```
1000A=194:GOTO20
1010DIMR$(11):DIMY(11):HO=14:VE=14
1310HO=HO+1:R=HO:GOSUB110:GOSUB120:IFR=HO THEN1310
1610VE=VE+1:S=VE::GOSUB110:GOSUB120:IFVE=S THEN1610
1910GOSUB100:VE=6:HO=(R-7)/2:GOSUB110:PRINT"MazezaM":VE=S-6
1920HO=0:GOSUB110:PRINT"MOVE  IJKL":PRINT"RETRY R"
1930PRINT"SKIP  S":GOSUB210:RESTORE:Z=0:N$="":T=0
2210GOSUB250:T=T+1:IFT=31THEN1910
2220GOSUB4910:N=W:GOSUB4910:M=W:GOSUB4910:P=W:GOSUB4910:Q=W
2230F=0:FORC=0TON-1:R$(C)="":Y(C)=0:FORD=0TOM-1:A$="="
2240IFF=0THENGOSUB4910:F=6
2250F=F-1:G=INT(W/2)*2:IFW=G THENA$=" "
2260R$(C)=R$(C)+A$:W=G/2:NEXTD:NEXTC:U=INT((R-M)/2)
2270V=INT((S-N)/2)
2510GOSUB100
2810VE=V-1:HO=U-1:W=P:X=0:GOSUB4610:FORI=0TON-1:Y(I)=0
2820VE=VE+1:GOSUB110:A$="#":B$=A$:IFI=P THENA$="."
2830IFI=Q THENB$="."
2840PRINTA$;:GOSUB4010:PRINTB$:NEXTI:VE=VE+1:GOSUB4610
2850HO=HO+1
3110GOSUB210:D=W:E=X:IFIN$="i"ANDW>0THEND=W-1
3120IFIN$="k"ANDW<N-1THEND=W+1
3130IFIN$="j"ANDX>0THENE=X-1:F=1
3140IFIN$="l"ANDX<M-1THENE=X+1:F=M
3150IFIN$="l"ANDW=Q ANDX=M-1ORIN$="s"THEN2210
3160IFIN$="r"THEN2810
3170I=D:GOSUB4310
3180IFMID$(J$,E+1,1)=" "THENI=W:W=D:X=E:GOSUB3710:GOTO3410
3190IFX<>E ANDMID$(J$,F,1)=" "THENY(W)=Y(W)+E-X:X=E
3410I=W:GOSUB3710:GOTO3110
3710VE=V+I:GOSUB110
4010GOSUB4310:IFI<>W THENPRINTJ$;:RETURN
4020IFX>0THENPRINTLEFT$(J$,X);
4030PRINT"@";:IFX<M-1THENPRINTRIGHT$(J$,M-X-1);
4040RETURN
4310IFY(I)=0THENJ$=R$(I):RETURN
4320IFY(I)>0THENB=Y(I):C=M-B
4330IFY(I)<0THENC=-Y(I):B=M-C
4340J$=RIGHT$(R$(I),B)+LEFT$(R$(I),C):RETURN
4610GOSUB110:PRINTLEFT$("#################",M+2):RETURN
4910Z=Z+1:IFZ=LEN(N$)+1THENREADN$:Z=1
4920B=ASC(MID$(N$,Z,1)):A=ASC("A"):G=ASC("a"):H=ASC("0")
4930W=63:IFB>=A ANDB<A+26THENW=B-A
4940IFB>=G ANDB<G+26THENW=B-G+26
4950IFB>=H ANDB<H+10THENW=B-H+52
4960IFB=ASC("+")THENW=62
4970RETURN
4980DATA"CFBAKBCHABykADHABmVZBDICBkTlKEFDDCtSCEHADq6oWCFHAE"
4990DATA"cpQvKJDICCFQtdEHBCUspqDEOBD/2gZ20O4fCEHBB2UpDDGNAA"
5000DATA"4D6zp7p8nLmqJFGDBCmW6EEICDcwOXKAGGAFUVUNN0EKACsy1Y"
5010DATA"q7CEHADWk2hELFKAEtpocFlqJAEHCDKsRVOEPCAeeWbNavRzTF"
5020DATA"ICC1sGq9gCELACuBzaerBAFIDBkjpuqJNEJDAiYP3QBHJGCyTa"
5030DATA"6tJE3PEAGHAAy08CdPAKNHAAg8f6AT+l7MFZ63Ux5+DAAHJBEy"
5040DATA"wq1w+0rJ6AKLAJAg+39oWA9/GuNYu+HAAHKAAaRdTF2OVZd0F"
```

The makefile also generates an audio file called `MazezaM.wav`. This can be loaded on many old paltforms using a BASICODE loader (or "Bascoder"). I have tested the program by loading the audio on several emulated platforms, including C64 and ZX Spectrum. Unfortunately, I have not managed to get BASICODE working on any Vic-20 emulator, so I'm not 100% sure if it works on that platform. If you have an actual Vic-20, I love to know if it works. 
