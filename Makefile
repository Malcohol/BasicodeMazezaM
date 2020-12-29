
PYTHON = python

all: MazezaM.bas

levels.bas: levels.mzm
	$(PYTHON) mzm-tools/mzm-convert -c levels.mzm > levels.bas

MazezaM.bas: main.bas levels.bas
	$(PYTHON) basicodify.py main.bas levels.bas > MazezaM.bas

clean:
	rm -f MazezaM.bas levels.bas 
