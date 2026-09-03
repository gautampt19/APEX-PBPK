import re

with open("webapp/templates/index.html", "r", encoding="utf-8") as f:
    code = f.read()

target = '<script src="/static/app.js"></script>'
replace = '<script src="/static/app.js?v=1.2"></script>'

code = code.replace(target, replace)

with open("webapp/templates/index.html", "w", encoding="utf-8") as f:
    f.write(code)
