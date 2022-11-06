
PYTHON = python

all: MazezaM.bas README.md

levels.bas: levels.mzm
	$(PYTHON) mzm-tools/mzm-convert.py -c levels.mzm > levels.bas

MazezaM.bas: main.bas levels.bas
	$(PYTHON) basicodify.py main.bas levels.bas > MazezaM.bas

README.md: readme_header.md readme_footer.md MazezaM.bas
	cat readme_header.md MazezaM.bas readme_footer.md > README.md 

clean:
	rm -f MazezaM.bas levels.bas 
