import re

with open("webapp/app.py", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update _run_pipeline signature and cmd
target_run_pipeline = """def _run_pipeline(job_id: str, pdf_path: str, use_colpali: bool,
                  model: str, top_k: int, backend: str):
    \"\"\"Run the pipeline in a background thread, streaming output to the job.\"\"\""""
replace_run_pipeline = """def _run_pipeline(job_id: str, pdf_path: str, use_colpali: bool,
                  model: str, top_k: int, backend: str, run_step: str = "all"):
    \"\"\"Run the pipeline in a background thread, streaming output to the job.\"\"\""""

code = code.replace(target_run_pipeline, replace_run_pipeline)

target_cmd = """    cmd = [
        str(VENV_PYTHON), str(PROJECT_ROOT / "run_pipeline.py"),
        "--pdf", pdf_path,
        "--backend", backend,
        "--model-extract", model,
        "--model-generate", model,
        "--output-dir", str(PIPELINE_OUTPUT),
    ]"""
replace_cmd = """    cmd = [
        str(VENV_PYTHON), str(PROJECT_ROOT / "run_pipeline.py"),
        "--pdf", pdf_path,
        "--backend", backend,
        "--model-extract", model,
        "--model-generate", model,
        "--output-dir", str(PIPELINE_OUTPUT),
        "--run-step", run_step,
        "--non-interactive"
    ]"""
code = code.replace(target_cmd, replace_cmd)

# 2. Update /api/run
target_run_route = """    use_colpali = data.get("use_colpali", True)
    model = data.get("model", "qwen3.8:latest")
    top_k = data.get("top_k", 5)
    backend = data.get("backend", "ollama")

    t = threading.Thread(
        target=_run_pipeline,
        args=(job_id, pdf_path, use_colpali, model, top_k, backend),
        daemon=True,
    )"""
replace_run_route = """    use_colpali = data.get("use_colpali", True)
    model = data.get("model", "qwen3.8:latest")
    top_k = data.get("top_k", 5)
    backend = data.get("backend", "ollama")
    run_step = data.get("run_step", "all")

    t = threading.Thread(
        target=_run_pipeline,
        args=(job_id, pdf_path, use_colpali, model, top_k, backend, run_step),
        daemon=True,
    )"""
code = code.replace(target_run_route, replace_run_route)

# 3. Add /api/save-params
save_params_code = """
@app.route("/api/save-params", methods=["POST"])
def save_params():
    \"\"\"Save edited parameters from UI.\"\"\"
    data = request.get_json(force=True)
    paper_name = data.get("paper_name")
    params = data.get("parameters")
    
    if not paper_name or not params:
        return jsonify({"error": "Missing paper_name or parameters"}), 400
        
    params_file = PIPELINE_OUTPUT / f"{paper_name}_params.json"
    
    try:
        with open(params_file, "w") as f:
            json.dump(params, f, indent=4)
        return jsonify({"message": "Parameters saved successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
"""

code = code.replace("@app.route(\"/api/status/<job_id>\")", save_params_code + "\n@app.route(\"/api/status/<job_id>\")")

with open("webapp/app.py", "w", encoding="utf-8") as f:
    f.write(code)
