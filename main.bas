# MazezaM in basicode

# This is optimized for program size with the intention of supporting the unexpanded VIC-20.

# Stardard Basicode routines

_cls_ = 100
_setCursor_ = 110
_getCursor_ = 120
_getKey_ = 210
_beep_ = 250

# Globals (>= H)

_levelWidth_ = M
_levelHeight_ = N
_levelStart_ = P
_levelExit_ = Q
_screenWidth_ = R
_screenHeight_ = S
_levelNum_ = T
_horizOffset_ = U
_vertOffset_ = V
_playerRow_ = W
_playerCol_ = X
_indexInDataString_ = Z
_sixBits_= W

_dataString_ = N$
_levelLines_ = R$
_offsets_ = Y

# Input parameters

_lineIndex_ = I
_lineString_ = J$


###########################################################
# INITIALIZATION
###########################################################

    A=_stringRequirements_
    GOTO 20
1010:
    DIM _levelLines_(_maxNumRows_)
    DIM _offsets_(_maxNumRows_)
    HO=14
    VE=14
_findWidth_:
    HO=HO+1
    _screenWidth_=HO
    GOSUB_setCursor_
    GOSUB _getCursor_
    IF _screenWidth_=HO THEN GOTO _findWidth_
_findHeight_:
    VE=VE+1
    _screenHeight_=VE:
    GOSUB_setCursor_
    GOSUB _getCursor_
    IF VE=_screenHeight_ THEN GOTO _findHeight_

###########################################################
# GAME START
###########################################################

_AttractScreen_:
    GOSUB _cls_
    VE=6
    HO=(_screenWidth_-7)/2
    GOSUB _setCursor_
    PRINT "MazezaM"
    VE=_screenHeight_-6
    HO=0
    GOSUB _setCursor_
    PRINT "MOVE  IJKL"
    PRINT "RETRY R"
    PRINT "SKIP  S"
    GOSUB _getKey_

    RESTORE
    _indexInDataString_ = 0
    _dataString_=""
    _levelNum_ = 0

###########################################################
# READ LEVEL DATA
###########################################################

# LOCALS: C, D, F, G, A$

_readLevel_:
    GOSUB _beep_
    _levelNum_=_levelNum_+1
    IF _levelNum_=_numLevelsPlusOne_ THEN GOTO _AttractScreen_
    GOSUB _getNextSixBits_
    _levelHeight_ = _sixBits_
    GOSUB _getNextSixBits_
    _levelWidth_ = _sixBits_
    GOSUB _getNextSixBits_
    _levelStart_=_sixBits_
    GOSUB _getNextSixBits_
    _levelExit_=_sixBits_
    F=0
    FOR C = 0 TO _levelHeight_-1
        _levelLines_(C)=""
        _offsets_(C)=0
        FOR D = 0 TO _levelWidth_-1
            A$="="
            IF F = 0 THEN GOSUB _getNextSixBits_: F=6
            F=F-1
            G=INT(_sixBits_/2)*2
            IF _sixBits_ = G THEN A$=" "
            _levelLines_(C)=_levelLines_(C)+A$
            _sixBits_=G/2
		NEXT D
	NEXT C
    _horizOffset_=INT((_screenWidth_-_levelWidth_)/2)
    _vertOffset_=INT((_screenHeight_-_levelHeight_)/2)

###########################################################
# DRAW LEVEL
###########################################################

# Locals: A$, B$

_drawLevel_:
    GOSUB _cls_
_resetLevel_:
    VE=_vertOffset_-1
    HO=_horizOffset_-1
    _playerRow_=_levelStart_
    _playerCol_=0
    GOSUB _drawHorizLine_

	FOR _lineIndex_ = 0 TO _levelHeight_-1
        _offsets_(_lineIndex_) = 0
        # Draw line
        VE=VE+1
        GOSUB _setCursor_
        A$="#"
        B$=A$
        IF _lineIndex_=_levelStart_ THEN A$="."
		IF _lineIndex_=_levelExit_ THEN B$="."
        PRINT A$;
        GOSUB _printLevelRow_
        PRINT B$
    NEXT _lineIndex_
    VE=VE+1
    GOSUB _drawHorizLine_
    HO=HO+1

###########################################################
# PLAY LEVEL
###########################################################

# Locals: D, E, F

_playLevel_:
    GOSUB _getKey_
    D=_playerRow_
    E=_playerCol_
    IF IN$="i" AND _playerRow_>0 THEN D=_playerRow_-1
    IF IN$="k" AND _playerRow_<_levelHeight_-1 THEN D=_playerRow_+1
    IF IN$="j" AND _playerCol_>0 THEN E=_playerCol_-1:F=1
    IF IN$="l" AND _playerCol_<_levelWidth_-1 THEN E=_playerCol_+1:F=_levelWidth_
    # Assume left precedence
    IF IN$="l" AND _playerRow_=_levelExit_ AND _playerCol_=_levelWidth_-1 OR IN$="s" THEN GOTO _readLevel_
    IF IN$="r" THEN GOTO _resetLevel_
    I=D
    GOSUB _getLevelRow_
    IF MID$(_lineString_,E+1,1)=" " THEN I=_playerRow_: _playerRow_=D: _playerCol_=E: GOSUB _drawLevelRow_:GOTO _drawNewRow_
    IF _playerCol_<>E AND MID$(_lineString_,F,1)=" " THEN _offsets_(_playerRow_)=_offsets_(_playerRow_)+E-_playerCol_: _playerCol_=E
_drawNewRow_:
    I=_playerRow_
    GOSUB _drawLevelRow_
    GOTO _playLevel_

###########################################################
# ROUTINES
###########################################################

_drawLevelRow_:
    VE=_vertOffset_+_lineIndex_
    GOSUB _setCursor_
_printLevelRow_:
    GOSUB _getLevelRow_
    IF _lineIndex_<>_playerRow_ THEN PRINT _lineString_;: RETURN
    IF _playerCol_>0 THEN PRINT LEFT$(_lineString_, _playerCol_);
    PRINT "@";
    IF _playerCol_<_levelWidth_-1 THEN PRINT RIGHT$(_lineString_, _levelWidth_-_playerCol_-1);    
    RETURN

# Locals B, C

_getLevelRow_:
    IF _offsets_(_lineIndex_)=0 THEN _lineString_=_levelLines_(_lineIndex_): RETURN
    IF _offsets_(_lineIndex_)>0 THEN B=_offsets_(_lineIndex_): C=_levelWidth_-B
    IF _offsets_(_lineIndex_)<0 THEN C=-_offsets_(_lineIndex_): B=_levelWidth_-C
    _lineString_=RIGHT$(_levelLines_(_lineIndex_),B)+LEFT$(_levelLines_(_lineIndex_),C)
    RETURN

_drawHorizLine_:
    GOSUB _setCursor_
    PRINT LEFT$("#################",_levelWidth_+2)
    RETURN

# Locals: B, A, G, H

_getNextSixBits_:
    _indexInDataString_ = _indexInDataString_ + 1
    IF _indexInDataString_ = LEN(_dataString_)+1 THEN READ _dataString_: _indexInDataString_ = 1
    B=ASC(MID$(_dataString_,_indexInDataString_,1))
    A=ASC("A")
    G=ASC("a")
    H=ASC("0")
    _sixBits_ = 63
    IF B >= A AND B < A+26 THEN _sixBits_ = B - A
    IF B >= G AND B < G+26 THEN _sixBits_ = B - G + 26
    IF B >= H AND B < H+10 THEN _sixBits_ = B - H + 52
    IF B = ASC("+") THEN _sixBits_ = 62
    RETURN

###########################################################
# LEVEL DATA GOES HERE
###########################################################
