import re

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
    
    # Delete old results if this file was processed previously
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

code = code.replace(target, replace)

with open("webapp/app.py", "w", encoding="utf-8") as f:
    f.write(code)
