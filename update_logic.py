import re
from pathlib import Path

# 1. FIX APP.PY
with open("webapp/app.py", "r", encoding="utf-8") as f:
    code = f.read()

target = """    save_path = PAPERS_DIR / f.filename
    f.save(str(save_path))
    return jsonify({
        "message": f"Uploaded {f.filename}",
        "filename": f.filename,
        "paper_name": Path(f.filename).stem,
    })"""
replace = """    save_path = PAPERS_DIR / f.filename
    f.save(str(save_path))
    
    paper_name = Path(f.filename).stem
    for ext in ["_params.json", "_cleaned.md", "_pbpk_model.R"]:
        old_file = PIPELINE_OUTPUT / f"{paper_name}{ext}"
        if old_file.exists():
            old_file.unlink()

    return jsonify({
        "message": f"Uploaded {f.filename}",
        "filename": f.filename,
        "paper_name": paper_name,
    })"""
if target in code:
    code = code.replace(target, replace)
with open("webapp/app.py", "w", encoding="utf-8") as f:
    f.write(code)

# 2. FIX INDEX.HTML (Remove Previous Papers)
with open("webapp/templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(r'<!-- Previously uploaded papers -->.*?</ul>\s*</div>', '', html, flags=re.DOTALL)
with open("webapp/templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)

# 3. FIX APP.JS (Remove loadPaperList)
with open("webapp/static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

js = js.replace("loadPaperList();", "")
with open("webapp/static/app.js", "w", encoding="utf-8") as f:
    f.write(js)

