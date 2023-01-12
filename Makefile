
PYTHON = python3

all: MazezaM.bas MazezaM.wav README.md

levels.bas: mzm-tools/mzm-convert.py levels.mzm
	$(PYTHON) mzm-tools/mzm-convert.py -c -o levels.bas levels.mzm

MazezaM.bas: basicodify.py main.bas levels.bas
	$(PYTHON) basicodify.py -o MazezaM.bas main.bas levels.bas

MazezaM.wav: basicodeToWav.py MazezaM.bas
	$(PYTHON) basicodeToWav.py -o MazezaM.wav MazezaM.bas

README.md: readme_template.md MazezaM.bas
	sed -e '/LISTING/r MazezaM.bas' readme_template.md | sed -e '/LISTING/d' > README.md

clean:
	rm -f MazezaM.bas levels.bas MazezaM.wav
