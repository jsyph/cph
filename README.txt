cph: Competetive Programming Helper

pyinstaller build command:
pyinstaller -D -F --add-data src/sources.toml:. --add-data src/template.jinja.cpp:. --hidden-import colorama -n cph src/main.py

