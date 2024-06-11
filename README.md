# cph: Competetive Programming Helper

pyinstaller build command:
```sh
pyinstaller -D -F --add-data src/sources.toml:. --add-data src/template.jinja.cpp:. --hidden-import jinja2 --hidden-import colorama -n cph src/main.py
```
