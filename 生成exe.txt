@echo off
pyinstaller -i cat.ico main.py -p mineLabel.py -p minesweeper_master.py -p mineSweeperGui.py -p selfDefinedParameter.py -p statusLabel.py -p superGUI.py -p gameSettings.py -p gameAbout.py -p gameHelp.py -p gameTerms.py -p src_help_pic_rc.py -p gameScores.py -p gameSetMoreGUI.py -p mainWindowGUI -w
pause