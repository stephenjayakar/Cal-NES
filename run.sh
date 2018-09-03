python3 main.py nestest.nes -d > mine.dat
wdiff mine.dat theirs.dat > diff.diff
open -a Emacs.app diff.diff
