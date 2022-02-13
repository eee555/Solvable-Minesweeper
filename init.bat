mkdir .\src\ui
cd uiFiles
pyuic5 -o ui_gameSettings.py ui_gs.ui
pyuic5 -o ui_gameSettingShortcuts.py ui_gs_shortcuts.ui
pyuic5 -o ui_defined_parameter.py ui_defined_parameter.ui
pyuic5 -o ui_mine_num_bar.py ui_mine_num_bar.ui
for %%i in (*.py) do ( move %%i ../src/ui/%%i )

cd src
pyrcc5 src_help_pic.qrc -o src_help_pic_rc.py
cd ..