#!/bin/zsh
export PATH="/opt/homebrew/opt/tcl-tk@8/bin:$PATH"
export TK_LIBRARY="/opt/homebrew/opt/tcl-tk@8/lib/tk8.6"
export TCL_LIBRARY="/opt/homebrew/opt/tcl-tk@8/lib/tcl8.6"
python3 "$@"
